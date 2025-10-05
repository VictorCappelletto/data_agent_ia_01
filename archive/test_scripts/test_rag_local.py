"""
Local RAG Integration Test

Tests the Troubleshooter specialist with RAG integration using
real workflow JSONs to validate improvement over generic responses.

This test runs locally without requiring API keys.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any

# Setup paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from data_pipeline_agent_lib.utils import get_logger

logger = get_logger(__name__)


def load_workflow_jsons() -> Dict[str, Any]:
    """
    Load all workflow JSONs from workflow_hdl/ directory.
    
    Returns:
        Dictionary mapping workflow names to their configurations
    """
    workflow_dir = project_root / "workflow_hdl"
    workflows = {}
    
    logger.info("Loading workflow JSONs", directory=str(workflow_dir))
    
    if not workflow_dir.exists():
        logger.warning("workflow_hdl/ directory not found")
        return workflows
    
    for json_file in workflow_dir.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                workflow_data = json.load(f)
                workflow_name = workflow_data.get("name", json_file.stem)
                workflows[workflow_name] = workflow_data
                
        except Exception as e:
            logger.error(
                "Failed to load workflow JSON",
                file=json_file.name,
                error=str(e)
            )
    
    logger.info("Workflow JSONs loaded", count=len(workflows))
    return workflows


def create_workflow_knowledge_summary(workflows: Dict[str, Any]) -> str:
    """
    Create a summary of loaded workflows for testing.
    
    Args:
        workflows: Dictionary of workflow configurations
        
    Returns:
        Formatted summary string
    """
    streaming = [name for name in workflows.keys() if "stream" in name]
    batch = [name for name in workflows.keys() if "ingestion" in name or "sharedtables" in name]
    
    summary_parts = []
    summary_parts.append("=" * 70)
    summary_parts.append("WORKFLOW KNOWLEDGE BASE LOADED")
    summary_parts.append("=" * 70)
    summary_parts.append("")
    summary_parts.append(f"Total Workflows: {len(workflows)}")
    summary_parts.append(f"Streaming: {len(streaming)}")
    summary_parts.append(f"Batch: {len(batch)}")
    summary_parts.append("")
    
    summary_parts.append("STREAMING WORKFLOWS:")
    for name in sorted(streaming)[:5]:
        summary_parts.append(f"  - {name}")
    if len(streaming) > 5:
        summary_parts.append(f"  ... and {len(streaming) - 5} more")
    
    summary_parts.append("")
    summary_parts.append("BATCH WORKFLOWS:")
    for name in sorted(batch)[:5]:
        summary_parts.append(f"  - {name}")
    if len(batch) > 5:
        summary_parts.append(f"  ... and {len(batch) - 5} more")
    
    summary_parts.append("")
    summary_parts.append("=" * 70)
    
    return "\n".join(summary_parts)


def test_troubleshooter_without_rag():
    """
    Test Troubleshooter using only hardcoded patterns (fallback mode).
    
    This simulates the old behavior where specialists provided
    generic responses without knowledge base context.
    """
    from data_pipeline_agent_lib.specialists.troubleshooter import DPLTroubleshooter
    
    logger.info("Testing Troubleshooter WITHOUT RAG (fallback mode)")
    
    test_cases = [
        {
            "error": "Timeout error in dpl-stream-visits after 1h30m",
            "entity": "visits",
            "pipeline_type": "streaming"
        },
        {
            "error": "SCD2 merge issue in Orders entity",
            "entity": "tasks",
            "pipeline_type": "batch"
        },
        {
            "error": "Connection timeout to CosmosDB",
            "entity": None,
            "pipeline_type": "batch"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"Test case {i}", error=test_case["error"][:50])
        
        result = DPLTroubleshooter.diagnose_error(
            error_message=test_case["error"],
            entity_name=test_case["entity"],
            pipeline_type=test_case["pipeline_type"],
            hdl_context=None  # No RAG context
        )
        
        results.append({
            "test_case": i,
            "error": test_case["error"],
            "diagnosis": result.diagnosis,
            "severity": result.severity,
            "confidence": result.confidence,
            "mode": "FALLBACK (No RAG)"
        })
    
    return results


def test_troubleshooter_with_rag():
    """
    Test Troubleshooter with RAG integration enabled.
    
    This uses the new RAG service to search the knowledge base
    and provide DPL-specific context.
    """
    from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error
    
    logger.info("Testing Troubleshooter WITH RAG (enhanced mode)")
    
    test_cases = [
        {
            "error": "Timeout error in dpl-stream-visits after 1h30m",
            "entity": "visits",
            "pipeline_type": "streaming"
        },
        {
            "error": "SCD2 merge issue in Orders entity",
            "entity": "tasks",
            "pipeline_type": "batch"
        },
        {
            "error": "Connection timeout to CosmosDB",
            "entity": None,
            "pipeline_type": "batch"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"Test case {i} with RAG", error=test_case["error"][:50])
        
        try:
            # LangChain tools prefer .invoke() method with single string input
            query = test_case["error"]
            if test_case["entity"]:
                query += f" | entity: {test_case['entity']}"
            if test_case["pipeline_type"]:
                query += f" | type: {test_case['pipeline_type']}"
            
            response = troubleshoot_hdl_error.invoke(query)
            
            results.append({
                "test_case": i,
                "error": test_case["error"],
                "response": response[:500],  # Truncate for display
                "has_sources": "KNOWLEDGE SOURCES" in response,
                "mode": "RAG-ENHANCED"
            })
            
        except Exception as e:
            logger.error(f"Test case {i} failed", error=str(e))
            results.append({
                "test_case": i,
                "error": test_case["error"],
                "response": f"ERROR: {e}",
                "has_sources": False,
                "mode": "FAILED"
            })
    
    return results


def compare_results(
    fallback_results: List[Dict],
    rag_results: List[Dict]
):
    """
    Compare results from fallback vs RAG-enhanced modes.
    
    Args:
        fallback_results: Results from tests without RAG
        rag_results: Results from tests with RAG enabled
    """
    print("\n" + "=" * 70)
    print("COMPARISON: FALLBACK vs RAG-ENHANCED")
    print("=" * 70)
    
    for i in range(len(fallback_results)):
        fallback = fallback_results[i]
        rag = rag_results[i]
        
        print(f"\n--- TEST CASE {i+1} ---")
        print(f"Error: {fallback['error'][:60]}...")
        print("")
        
        print("FALLBACK MODE (No RAG):")
        print(f"  Diagnosis: {fallback['diagnosis'][:80]}...")
        print(f"  Severity: {fallback['severity']}")
        print(f"  Confidence: {fallback['confidence']}")
        print(f"  Knowledge Sources: None")
        print("")
        
        print("RAG-ENHANCED MODE:")
        print(f"  Response Length: {len(rag['response'])} chars")
        print(f"  Has Knowledge Sources: {rag['has_sources']}")
        print(f"  Mode: {rag['mode']}")
        
        if rag['has_sources']:
            print("  Improvement: Uses DPL-specific knowledge")
        else:
            print("  Note: Fallback used (KB may need loading)")
    
    print("\n" + "=" * 70)


def main():
    """
    Main test execution.
    
    Runs comprehensive local test of RAG integration without
    requiring external API keys or services.
    """
    print("\n" + "=" * 70)
    print("DPL AGENT - LOCAL RAG INTEGRATION TEST")
    print("=" * 70)
    print("")
    print("Purpose: Validate RAG integration improves specialist responses")
    print("Mode: Local (no API keys required)")
    print("Status: Testing Phase 1 + Phase 2 implementation")
    print("")
    
    # Step 1: Load workflow JSONs
    print("STEP 1: Loading workflow JSONs...")
    workflows = load_workflow_jsons()
    print(create_workflow_knowledge_summary(workflows))
    
    if not workflows:
        print("\nWARNING: No workflow JSONs loaded!")
        print("Expected location: workflow_hdl/*.json")
        print("Cannot proceed with workflow validation.")
        return
    
    # Step 2: Test without RAG (fallback)
    print("\nSTEP 2: Testing Troubleshooter WITHOUT RAG (fallback mode)...")
    fallback_results = test_troubleshooter_without_rag()
    print(f"Completed: {len(fallback_results)} test cases")
    
    # Step 3: Test with RAG
    print("\nSTEP 3: Testing Troubleshooter WITH RAG (enhanced mode)...")
    rag_results = test_troubleshooter_with_rag()
    print(f"Completed: {len(rag_results)} test cases")
    
    # Step 4: Compare results
    print("\nSTEP 4: Comparing results...")
    compare_results(fallback_results, rag_results)
    
    # Step 5: Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print("")
    print(f"Workflows Available: {len(workflows)}")
    print(f"Test Cases Run: {len(fallback_results)}")
    print("")
    
    rag_with_sources = sum(1 for r in rag_results if r.get("has_sources", False))
    print(f"RAG-Enhanced Tests with Knowledge Sources: {rag_with_sources}/{len(rag_results)}")
    
    if rag_with_sources > 0:
        print("")
        print("CONCLUSION: RAG integration is working!")
        print("Specialists are using knowledge base successfully.")
    else:
        print("")
        print("CONCLUSION: RAG search not finding results.")
        print("Possible causes:")
        print("  1. Knowledge base not loaded into vector store")
        print("  2. Vector store not initialized")
        print("  3. Workflow documentation needs to be created")
        print("")
        print("NEXT STEP: Document workflows from JSONs into knowledge base")
    
    print("\n" + "=" * 70)
    print("")
    
    return workflows, fallback_results, rag_results


if __name__ == "__main__":
    try:
        workflows, fallback, rag = main()
        
        print("\nTest completed successfully!")
        print(f"Total workflows available: {len(workflows)}")
        print("")
        print("Next steps:")
        print("  1. Review comparison results above")
        print("  2. If RAG not working: document workflows in knowledge base")
        print("  3. If RAG working: continue with remaining specialists")
        
    except Exception as e:
        logger.error("Test failed", exc_info=True)
        print(f"\nERROR: {e}")
        print("See logs above for details")
        sys.exit(1)

