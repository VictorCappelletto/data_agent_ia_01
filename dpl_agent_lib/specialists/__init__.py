"""
DPL Agent v3.0 - Specialist Tools

LangChain tools for DPL-specific operations.
Each specialist focuses on a specific domain of DPL operations.
"""

from .troubleshooter import (
    DPLTroubleshooter,
    troubleshoot_hdl_error,
    analyze_pipeline_health,
)
from .bug_resolver import (
    BugResolver,
    resolve_hdl_bug,
)
from .performance_advisor import (
    PerformanceAdvisor,
    optimize_hdl_pipeline,
)
from .quality_assistant import (
    QualityAssistant,
    validate_hdl_data_quality,
)
from .hdl_commander import (
    execute_hdl_workflow,
    get_workflow_status,
)
from .ecosystem_assistant import (
    explain_hdl_component,
    get_hdl_best_practices,
)
from .hdl_coordinator import (
    coordinate_hdl_reprocessing,
)


# ============================================================================
# TOOL REGISTRY
# ============================================================================

# All DPL specialist tools
ALL_DPL_TOOLS = [
    # Troubleshooter
    troubleshoot_hdl_error,
    analyze_pipeline_health,
    
    # Bug Resolver
    resolve_hdl_bug,
    
    # Performance Advisor
    optimize_hdl_pipeline,
    
    # Quality Assistant
    validate_hdl_data_quality,
    
    # DPL Commander
    execute_hdl_workflow,
    get_workflow_status,
    
    # Ecosystem Assistant
    explain_hdl_component,
    get_hdl_best_practices,
    
    # DPL Coordinator
    coordinate_hdl_reprocessing,
]


# Categorized tool sets
TROUBLESHOOTING_TOOLS = [
    troubleshoot_hdl_error,
    analyze_pipeline_health,
    resolve_hdl_bug,
]

OPTIMIZATION_TOOLS = [
    optimize_hdl_pipeline,
    validate_hdl_data_quality,
]

OPERATIONAL_TOOLS = [
    execute_hdl_workflow,
    get_workflow_status,
    coordinate_hdl_reprocessing,
]

DOCUMENTATION_TOOLS = [
    explain_hdl_component,
    get_hdl_best_practices,
]


def get_tools_for_intent(intent: str) -> list:
    """
    Get relevant tools based on user intent.
    
    Args:
        intent: User intent (troubleshooting, optimization, etc.)
        
    Returns:
        List of relevant tools
    """
    intent_tool_map = {
        "troubleshooting": TROUBLESHOOTING_TOOLS,
        "optimization": OPTIMIZATION_TOOLS,
        "workflow_management": OPERATIONAL_TOOLS,
        "architecture": DOCUMENTATION_TOOLS,
        "best_practices": DOCUMENTATION_TOOLS,
        "data_quality": OPTIMIZATION_TOOLS,
    }
    
    return intent_tool_map.get(intent, ALL_DPL_TOOLS)


def get_tool_descriptions() -> dict:
    """
    Get descriptions of all available tools.
    
    Returns:
        Dictionary of tool name to description
    """
    return {
        tool.name: tool.description
        for tool in ALL_DPL_TOOLS
    }


__all__ = [
    # Classes
    "DPLTroubleshooter",
    "BugResolver",
    "PerformanceAdvisor",
    "QualityAssistant",
    
    # Tools
    "troubleshoot_hdl_error",
    "analyze_pipeline_health",
    "resolve_hdl_bug",
    "optimize_hdl_pipeline",
    "validate_hdl_data_quality",
    "execute_hdl_workflow",
    "get_workflow_status",
    "explain_hdl_component",
    "get_hdl_best_practices",
    "coordinate_hdl_reprocessing",
    
    # Tool Collections
    "ALL_DPL_TOOLS",
    "TROUBLESHOOTING_TOOLS",
    "OPTIMIZATION_TOOLS",
    "OPERATIONAL_TOOLS",
    "DOCUMENTATION_TOOLS",
    
    # Utilities
    "get_tools_for_intent",
    "get_tool_descriptions",
]

