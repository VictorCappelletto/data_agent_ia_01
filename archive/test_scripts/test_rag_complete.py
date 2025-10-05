"""
RAG Integration Complete Test

Tests all specialists with complete knowledge base (66 files)
to verify they return DPL-specific knowledge, not generic responses.
"""

import sys
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from data_pipeline_agent_lib.utils import get_logger
from data_pipeline_agent_lib.specialists import (
    troubleshoot_hdl_error,
    resolve_hdl_bug,
    optimize_hdl_pipeline,
    validate_hdl_data_quality,
    execute_hdl_workflow,
    get_workflow_status,
    explain_hdl_component,
    get_hdl_best_practices,
    coordinate_hdl_reprocessing,
)

logger = get_logger(__name__)


def test_specialist(specialist_name: str, tool_func, test_query: str) -> dict:
    """Test a specialist with a specific query."""
    logger.info("Testing specialist", name=specialist_name, query=test_query[:50])
    
    try:
        response = tool_func.invoke(test_query)
        
        # Check for knowledge sources
        has_sources = "KNOWLEDGE SOURCES" in response
        has_specific_workflow = any(wf in response for wf in [
            "dpl-stream-", "dpl-ingestion-", "sharedtables"
        ])
        response_length = len(response)
        
        result = {
            "specialist": specialist_name,
            "query": test_query[:60],
            "response_length": response_length,
            "has_sources": has_sources,
            "has_specific_workflow": has_specific_workflow,
            "status": "PASS" if (has_sources or has_specific_workflow) else "GENERIC"
        }
        
        logger.info(
            "Test complete",
            specialist=specialist_name,
            status=result["status"],
            has_sources=has_sources
        )
        
        return result
        
    except Exception as e:
        logger.error("Test failed", specialist=specialist_name, error=str(e))
        return {
            "specialist": specialist_name,
            "query": test_query[:60],
            "status": "ERROR",
            "error": str(e)
        }


def main():
    """Run comprehensive RAG integration tests."""
    print("\n" + "=" * 70)
    print("DPL AGENT - RAG INTEGRATION COMPLETE TEST")
    print("=" * 70)
    print("")
    print("Testing all 7 specialists with complete knowledge base (66 files)")
    print("")
    
    # Test cases for each specialist
    test_cases = [
        {
            "specialist": "Troubleshooter",
            "tool": troubleshoot_hdl_error,
            "queries": [
                "Timeout in dpl-stream-visits after 90 minutes",
                "dpl-ingestion-Orders batch job failing",
                "SCD2 issues in vendorgroups workflow"
            ]
        },
        {
            "specialist": "Bug Resolver",
            "tool": resolve_hdl_bug,
            "queries": [
                "SCD2 is_current broken in Orders entity",
                "Streaming checkpoint corrupt in visits",
                "CosmosDB connection timeout in batch ingestion"
            ]
        },
        {
            "specialist": "Performance Advisor",
            "tool": optimize_hdl_pipeline,
            "queries": [
                "dpl-stream-tasks slow execution",
                "dpl-ingestion-OnTapUserSessions slow execution",
                "sharedtables-ingestion slow execution"
            ]
        },
        {
            "specialist": "Quality Assistant",
            "tool": validate_hdl_data_quality,
            "queries": [
                "tasks data quality validation",
                "visits completeness check",
                "vendorgroups accuracy validation"
            ]
        },
        {
            "specialist": "DPL Commander",
            "tool": execute_hdl_workflow,
            "queries": [
                "dpl-stream-visits",
                "dpl-ingestion-Orders",
                "sharedtables-ingestion"
            ]
        },
        {
            "specialist": "Ecosystem Assistant",
            "tool": explain_hdl_component,
            "queries": [
                "BaseTable",
                "IngestionControl",
                "SCD2"
            ]
        },
        {
            "specialist": "DPL Coordinator",
            "tool": coordinate_hdl_reprocessing,
            "queries": [
                "tasks | 2025-10-04",
                "visits | 2025-10-01",
                "vendorgroups | 2025-09-30"
            ]
        }
    ]
    
    # Run all tests
    all_results = []
    total_tests = sum(len(tc["queries"]) for tc in test_cases)
    current_test = 0
    
    for test_case in test_cases:
        print(f"\n{'=' * 70}")
        print(f"TESTING: {test_case['specialist']}")
        print(f"{'=' * 70}\n")
        
        for query in test_case["queries"]:
            current_test += 1
            print(f"[{current_test}/{total_tests}] {query[:50]}...")
            
            result = test_specialist(
                test_case["specialist"],
                test_case["tool"],
                query
            )
            all_results.append(result)
            
            # Display result
            status_icon = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "GENERIC" else "❌"
            print(f"    {status_icon} {result['status']}")
            if result.get("has_sources"):
                print(f"       Knowledge sources found")
            if result.get("has_specific_workflow"):
                print(f"       Specific workflow mentioned")
            print("")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print("")
    
    pass_count = sum(1 for r in all_results if r["status"] == "PASS")
    generic_count = sum(1 for r in all_results if r["status"] == "GENERIC")
    error_count = sum(1 for r in all_results if r["status"] == "ERROR")
    
    print(f"Total Tests: {len(all_results)}")
    print(f"  PASS (DPL-specific): {pass_count}")
    print(f"  GENERIC (fallback): {generic_count}")
    print(f"  ERROR: {error_count}")
    print("")
    
    success_rate = (pass_count / len(all_results)) * 100 if all_results else 0
    print(f"DPL-Specific Response Rate: {success_rate:.1f}%")
    print("")
    
    if success_rate >= 80:
        print("CONCLUSION: RAG integration EXCELLENT")
        print("Specialists are successfully using knowledge base!")
    elif success_rate >= 50:
        print("CONCLUSION: RAG integration GOOD")
        print("Most specialists using knowledge base, some fallback")
    elif success_rate >= 20:
        print("CONCLUSION: RAG integration PARTIAL")
        print("Knowledge base may need embedding refresh")
    else:
        print("CONCLUSION: RAG not working optimally")
        print("Knowledge base may not be loaded in vector store")
        print("")
        print("ACTION REQUIRED:")
        print("  1. Configure OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        print("  2. Run: python scripts/load_knowledge_base.py")
        print("  3. Re-run this test")
    
    print("\n" + "=" * 70)
    print("")
    
    return all_results


if __name__ == "__main__":
    try:
        results = main()
        print("Test completed successfully!")
        print(f"Tested {len(results)} specialist queries")
        print("")
        
        # Check if we need to load KB
        kb_needs_loading = all(r["status"] != "PASS" for r in results)
        if kb_needs_loading:
            print("NEXT STEP: Load knowledge base with embeddings")
            print("Command: python scripts/load_knowledge_base.py")
        else:
            print("NEXT STEP: Rebuild .whl package v3.1.0")
            print("Command: python setup.py bdist_wheel")
        
    except Exception as e:
        logger.error("Test failed", exc_info=True)
        print(f"\nERROR: {e}")
        sys.exit(1)

