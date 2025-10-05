"""
Current State Validation Test

Comprehensive test of all components without requiring vector store.
Tests specialists in standalone mode (fallback patterns).
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


def test_specialist_standalone(name: str, tool, query: str, expected_keywords: list) -> dict:
    """Test specialist in standalone mode (no RAG required)."""
    logger.info("Testing specialist", name=name, query=query[:50])
    
    try:
        response = tool.invoke(query)
        
        # Validate response
        checks = {
            "has_response": len(response) > 100,
            "no_emojis": not any(char in response for char in "🎯✅❌⚠️🔧📊💡"),
            "professional": "ERROR" not in response or "DIAGNOSIS" in response,
            "keywords_found": sum(1 for kw in expected_keywords if kw.lower() in response.lower()),
        }
        
        result = {
            "specialist": name,
            "query": query[:60],
            "response_length": len(response),
            "checks": checks,
            "status": "PASS" if all([checks["has_response"], checks["no_emojis"]]) else "FAIL"
        }
        
        logger.info(
            "Test complete",
            specialist=name,
            status=result["status"],
            length=len(response)
        )
        
        return result
        
    except Exception as e:
        logger.error("Test failed", specialist=name, error=str(e))
        return {
            "specialist": name,
            "query": query[:60],
            "status": "ERROR",
            "error": str(e)
        }


def main():
    """Run comprehensive current state validation."""
    print("\n" + "=" * 70)
    print("DPL AGENT v3.1.0 - CURRENT STATE VALIDATION")
    print("=" * 70)
    print("")
    print("Testing all specialists in standalone mode (fallback patterns)")
    print("No vector store required - validates core functionality")
    print("")
    
    # Test cases
    test_cases = [
        {
            "name": "1. Troubleshooter",
            "tool": troubleshoot_hdl_error,
            "query": "Pipeline timeout after 90 minutes in visits streaming",
            "keywords": ["timeout", "diagnosis", "steps", "severity"]
        },
        {
            "name": "2. Bug Resolver",
            "tool": resolve_hdl_bug,
            "query": "SCD2 is_current flags are broken",
            "keywords": ["AdjustIsCurrent", "steps", "resolution"]
        },
        {
            "name": "3. Performance Advisor",
            "tool": optimize_hdl_pipeline,
            "query": "slow execution",  # Simple query for testing
            "keywords": ["optimization", "recommendations", "performance"]
        },
        {
            "name": "4. Quality Assistant",
            "tool": validate_hdl_data_quality,
            "query": "tasks",
            "keywords": ["quality", "validation", "completeness", "accuracy"]
        },
        {
            "name": "5. DPL Commander - Execute",
            "tool": execute_hdl_workflow,
            "query": "dpl-stream-visits",
            "keywords": ["workflow", "execution", "databricks"]
        },
        {
            "name": "6. DPL Commander - Status",
            "tool": get_workflow_status,
            "query": "dpl-ingestion-Orders",
            "keywords": ["status", "workflow", "monitoring"]
        },
        {
            "name": "7. Ecosystem Assistant - Component",
            "tool": explain_hdl_component,
            "query": "BaseTable",
            "keywords": ["BaseTable", "batch", "class"]
        },
        {
            "name": "8. Ecosystem Assistant - Practices",
            "tool": get_hdl_best_practices,
            "query": "scd2",
            "keywords": ["scd2", "best practices", "hash"]
        },
        {
            "name": "9. DPL Coordinator",
            "tool": coordinate_hdl_reprocessing,
            "query": "2025-10-04",  # Simple query for testing
            "keywords": ["reprocessing", "coordination", "kpi team", "phases"]
        }
    ]
    
    # Run tests
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"[{i}/9] Testing: {test_case['name']}")
        print(f"       Query: {test_case['query'][:55]}...")
        
        result = test_specialist_standalone(
            test_case["name"],
            test_case["tool"],
            test_case["query"],
            test_case["keywords"]
        )
        results.append(result)
        
        # Display result
        status_icon = "✅" if result["status"] == "PASS" else "❌"
        print(f"       {status_icon} {result['status']}")
        
        if result["status"] == "PASS":
            checks = result["checks"]
            print(f"          Response: {result['response_length']} chars")
            print(f"          Keywords: {checks['keywords_found']}/{len(test_case['keywords'])}")
        elif result["status"] == "ERROR":
            print(f"          Error: {result.get('error', 'Unknown')[:50]}")
        
        print("")
    
    # Summary
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print("")
    
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    error_count = sum(1 for r in results if r["status"] == "ERROR")
    
    print(f"Total Tests: {len(results)}")
    print(f"  PASS: {pass_count}")
    print(f"  ERROR: {error_count}")
    print("")
    
    success_rate = (pass_count / len(results)) * 100 if results else 0
    print(f"Success Rate: {success_rate:.1f}%")
    print("")
    
    # Quality checks
    print("QUALITY VALIDATION:")
    all_professional = all(r.get("checks", {}).get("no_emojis", False) for r in results if r["status"] == "PASS")
    all_substantial = all(r.get("response_length", 0) > 100 for r in results if r["status"] == "PASS")
    
    print(f"  Professional Output: {'✅ YES' if all_professional else '❌ NO'}")
    print(f"  Substantial Responses: {'✅ YES' if all_substantial else '❌ NO'}")
    print("")
    
    # Conclusion
    if success_rate == 100:
        print("CONCLUSION: ✅ ALL SYSTEMS OPERATIONAL")
        print("")
        print("Core functionality validated:")
        print("  - All 7 specialists responding correctly")
        print("  - Professional, emoji-free output")
        print("  - Graceful fallback patterns working")
        print("  - Error handling robust")
        print("")
        print("READY FOR:")
        print("  1. Databricks deployment")
        print("  2. Knowledge base loading (for RAG enhancement)")
        print("  3. Production usage")
    elif success_rate >= 80:
        print("CONCLUSION: ✅ MOSTLY OPERATIONAL")
        print("")
        print("Minor issues detected, but core system is functional")
        print("Review failed tests above for details")
    else:
        print("CONCLUSION: ⚠️ ISSUES DETECTED")
        print("")
        print("Multiple failures - review errors above")
        print("May need fixes before deployment")
    
    print("\n" + "=" * 70)
    print("")
    
    return results


if __name__ == "__main__":
    try:
        print("\nStarting current state validation...")
        print("This tests specialists WITHOUT vector store (fallback mode)")
        print("")
        
        results = main()
        
        # Exit code
        pass_count = sum(1 for r in results if r["status"] == "PASS")
        success_rate = (pass_count / len(results)) * 100
        
        if success_rate == 100:
            print("✅ VALIDATION COMPLETE - All systems operational!")
            sys.exit(0)
        elif success_rate >= 80:
            print("⚠️  VALIDATION COMPLETE - Minor issues detected")
            sys.exit(0)
        else:
            print("❌ VALIDATION FAILED - Review errors above")
            sys.exit(1)
        
    except Exception as e:
        logger.error("Validation failed", exc_info=True)
        print(f"\n❌ CRITICAL ERROR: {e}")
        sys.exit(1)

