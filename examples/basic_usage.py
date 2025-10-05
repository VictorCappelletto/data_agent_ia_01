#!/usr/bin/env python3
"""
DPL Agent v3.0 - Basic Usage

Demonstrates all 7 specialist tools with minimal code.
No external dependencies required (no API key needed).
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data_pipeline_agent_lib.specialists import (
    troubleshoot_hdl_error,
    analyze_pipeline_health,
    resolve_hdl_bug,
    optimize_hdl_pipeline,
    validate_hdl_data_quality,
    execute_hdl_workflow,
    get_workflow_status,
    explain_hdl_component,
    get_hdl_best_practices,
    coordinate_hdl_reprocessing,
)


def print_section(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"{title}")
    print("=" * 70)


def main():
    """Run all specialist demonstrations."""
    print("DPL AGENT V3.0 - BASIC USAGE")
    print("Demonstrating all 7 specialist tools")
    
    # 1. Troubleshooter
    print_section("1. TROUBLESHOOTER - Error Diagnosis")
    result = troubleshoot_hdl_error(
        "Sessions streaming pipeline timed out after 90 minutes"
    )
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # 2. Bug Resolver
    print_section("2. BUG RESOLVER - Known Solutions")
    result = resolve_hdl_bug(
        "SCD2 is_current flag broken after data update"
    )
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # 3. Performance Advisor
    print_section("3. PERFORMANCE ADVISOR - Optimization")
    result = optimize_hdl_pipeline(
        "hdl-batch-tasks taking 2 hours instead of usual 30 minutes"
    )
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # 4. Quality Assistant
    print_section("4. QUALITY ASSISTANT - Data Validation")
    result = validate_hdl_data_quality(
        "Check completeness and consistency for visits entity"
    )
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # 5. DPL Commander
    print_section("5. DPL COMMANDER - Workflow Execution")
    result = execute_hdl_workflow(
        "Execute dpl-stream-visits workflow in PRD environment"
    )
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # 6. Ecosystem Assistant
    print_section("6. ECOSYSTEM ASSISTANT - Documentation")
    result = explain_hdl_component(
        "Explain SCD2 (Slowly Changing Dimension Type 2)"
    )
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # 7. DPL Coordinator
    print_section("7. DPL COORDINATOR - Reprocessing")
    result = coordinate_hdl_reprocessing(
        "TASKS entity for October 4th. Client waiting. Notify KPI team."
    )
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Summary
    print_section("SUMMARY")
    print("All 7 specialist tools demonstrated successfully.")
    print("\nNext steps:")
    print("- Try agent_conversation.py for full agent features")
    print("- See databricks_deployment.py for production patterns")
    print("- Run local_chat.py for interactive testing")


if __name__ == "__main__":
    main()

