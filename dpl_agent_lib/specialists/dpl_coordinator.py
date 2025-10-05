"""
DPL Agent v3.0 - DPL Coordinator Specialist

Specializes in coordinating multiple DPL operations and workflows.
"""

from typing import List, Dict, Any, Optional
from langchain.tools import tool

from ..utils import get_logger, ResponseFormatter

# Initialize logger
logger = get_logger(__name__)


@tool
def coordinate_hdl_reprocessing(
    entity_name: str,
    date_range: str,
    notify_kpi_team: bool = True
) -> str:
    """
    Coordinate DPL data reprocessing for a specific entity and date range.
    
    Based on real-world scenario: Manual reprocessing when data doesn't reach silver layer.
    
    Args:
        entity_name: Entity to reprocess (e.g., 'tasks', 'visits')
        date_range: Date range to reprocess (e.g., '2025-10-04')
        notify_kpi_team: Whether to notify KPI team after completion
        
    Returns:
        Reprocessing coordination plan
    """
    # Log operation
    logger.info(
        "Coordinating DPL reprocessing",
        entity_name=entity_name,
        date_range=date_range,
        notify_kpi_team=notify_kpi_team
    )
    
    # Build coordination steps
    preparation_steps = [
        "Verify data didn't reach silver layer",
        "Identify scope (specific date vs full history)",
        "Check dependencies (other entities affected)",
        "Notify stakeholders of planned reprocessing"
    ]
    
    execution_steps = [
        f"Trigger manual reprocessing for {entity_name}",
        f"Scope: {date_range} (targeted, not full history)",
        "Monitor execution in Databricks",
        "Verify data reaches silver layer"
    ]
    
    validation_steps = [
        "Check record counts (source vs bronze vs silver)",
        "Validate data quality metrics",
        "Verify SCD2 is_current flags",
        "Confirm completeness"
    ]
    
    if notify_kpi_team:
        coordination_steps = [
            "Notify KPI team to run gold + sharing pipelines",
            "Wait for DPL completion before KPI execution",
            "Monitor downstream dependencies"
        ]
    else:
        coordination_steps = [
            "Document reprocessing results"
        ]
    
    # Build complete plan
    all_steps = []
    all_steps.append("PHASE 1 - Preparation:")
    all_steps.extend(f"  {i+1}. {step}" for i, step in enumerate(preparation_steps))
    all_steps.append("")
    all_steps.append("PHASE 2 - Execution:")
    all_steps.extend(f"  {i+1}. {step}" for i, step in enumerate(execution_steps))
    all_steps.append("")
    all_steps.append("PHASE 3 - Validation:")
    all_steps.extend(f"  {i+1}. {step}" for i, step in enumerate(validation_steps))
    all_steps.append("")
    all_steps.append("PHASE 4 - Coordination:")
    all_steps.extend(f"  {i+1}. {step}" for i, step in enumerate(coordination_steps))
    all_steps.append("")
    all_steps.append("BASED ON REAL CASE:")
    all_steps.append("  - Client urgency = immediate action (not investigation)")
    all_steps.append("  - Targeted reprocessing (specific date, not full history)")
    all_steps.append("  - DPL -> KPI coordination essential")
    all_steps.append("  - Fast resolution prioritized")
    all_steps.append("")
    all_steps.append("ESTIMATED TIMELINE: 30-60 minutes")
    
    # Notify teams
    notify_teams = ["KPI Team"] if notify_kpi_team else []
    
    # Format response
    response = ResponseFormatter.format_reprocessing_plan(
        entity_name=entity_name,
        date_range=date_range,
        urgency="high" if notify_kpi_team else "normal",
        steps=all_steps,
        notify_teams=notify_teams
    )
    
    logger.info("Reprocessing plan created", entity_name=entity_name, phases=4)
    
    return response


__all__ = ["coordinate_hdl_reprocessing"]

