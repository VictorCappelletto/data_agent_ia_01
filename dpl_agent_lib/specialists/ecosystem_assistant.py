"""
DPL Agent v3.0 - Ecosystem Assistant Specialist

Specializes in DPL documentation, architecture guidance, and best practices.
Enhanced with RAG for component documentation and best practices.
"""

from typing import List, Dict, Any, Optional
from langchain.tools import tool

from ..utils import get_logger, CommonFormatters
from ..application.services import get_hdl_retriever_service

# Initialize logger
logger = get_logger(__name__)

# RAG service (lazy-loaded)
_rag_service = None

def _get_rag_service():
    """Lazy initialization of RAG service."""
    global _rag_service
    if _rag_service is None:
        try:
            _rag_service = get_hdl_retriever_service()
            logger.debug("RAG service initialized for Ecosystem Assistant")
        except Exception as e:
            logger.warning("RAG service initialization failed", error=str(e))
            _rag_service = None
    return _rag_service


@tool
def explain_hdl_component(component_name: str) -> str:
    """
    Explain an DPL component or concept.
    
    Args:
        component_name: Name of the component (e.g., 'BaseTable', 'IngestionControl', 'SCD2')
        
    Returns:
        Component explanation
    """
    # Common DPL components
    explanations = {
        "basetable": """
**BaseTable** is the abstract parent class for all DPL batch entities.

**Purpose**: Provides common functionality for batch ingestion pipelines.

**Key Features**:
- Schema definition and validation
- CosmosDB connection management
- Bronze and Silver layer processing
- SCD2 merge logic
- Standardized error handling

**Usage**: All batch entities (Orders, Sessions, PartnerGroups, etc.) inherit from BaseTable.
""",
        "scd2": """
**SCD2 (Slowly Changing Dimension Type 2)** is a data warehousing technique.

**Purpose**: Track historical changes to data over time.

**Key Fields**:
- is_current: Boolean flag for current version
- start_date: When record became effective
- end_date: When record was superseded (null for current)
- hash_key: MD5 hash for change detection

**In DPL**: Used in silver layer for tracking entity changes over time.
""",
        "ingestioncontrol": """
**IngestionControl** is the execution logging utility.

**Purpose**: Track pipeline execution metadata and status.

**Logged Information**:
- Execution start/end times
- Records processed
- Success/failure status
- Error messages
- Environment details

**Location**: hdl/utils/IngestionControl.py
""",
    }
    
    # Log operation
    logger.info("Explaining DPL component", component_name=component_name)
    
    # Try RAG search for component documentation
    rag_service = _get_rag_service()
    if rag_service:
        try:
            results = rag_service.search_component_documentation(f"DPL component {component_name}", k=2)
            if results:
                logger.debug("RAG found component documentation", count=len(results))
                rag_explanation = "\n".join([doc.page_content[:500] for doc in results])
                if rag_explanation:
                    explanations[component_name.lower().replace(" ", "")] = rag_explanation
        except Exception as e:
            logger.warning("RAG search failed for component", error=str(e))
    
    component_key = component_name.lower().replace(" ", "")
    explanation = explanations.get(
        component_key,
        f"Component '{component_name}' - See DPL documentation for details."
    )
    
    # Format response
    response_parts = []
    response_parts.append(f"DPL COMPONENT: {component_name}")
    response_parts.append("=" * 50)
    response_parts.append("")
    response_parts.append(explanation.strip())
    
    logger.debug("Component explanation provided", component_name=component_name)
    
    return "\n".join(response_parts)


@tool
def get_hdl_best_practices(topic: str) -> str:
    """
    Get DPL best practices for a specific topic.
    
    Args:
        topic: Topic for best practices (e.g., 'scd2', 'streaming', 'performance')
        
    Returns:
        Best practices guidance
    """
    best_practices = {
        "scd2": [
            "Always define proper SCD2 key columns",
            "Use MD5 hash for efficient change detection",
            "Validate is_current flags regularly",
            "Keep history for compliance requirements",
            "Use AdjustIsCurrent.py tool for corrections"
        ],
        "streaming": [
            "Use structured streaming with checkpoints",
            "Set appropriate trigger intervals",
            "Monitor checkpoint location health",
            "Implement idempotent operations",
            "Handle late-arriving data properly"
        ],
        "performance": [
            "Partition tables appropriately",
            "Use Delta Lake optimization features",
            "Monitor and tune cluster resources",
            "Implement incremental processing",
            "Use broadcast joins for small dimensions"
        ]
    }
    
    # Log operation
    logger.info("Getting DPL best practices", topic=topic)
    
    practices = best_practices.get(
        topic.lower(),
        ["Consult DPL documentation for topic-specific best practices"]
    )
    
    # Format response
    response_parts = []
    response_parts.append(f"DPL BEST PRACTICES: {topic.upper()}")
    response_parts.append("=" * 50)
    response_parts.append("")
    response_parts.append(CommonFormatters.format_list(practices, numbered=True, indent=0))
    response_parts.append("")
    response_parts.append("Additional Resources:")
    response_parts.append("  - DPL documentation in knowledge base")
    response_parts.append("  - Code examples in reference implementations")
    response_parts.append("  - Team knowledge sharing sessions")
    
    logger.debug("Best practices provided", topic=topic, count=len(practices))
    
    return "\n".join(response_parts)


__all__ = ["explain_hdl_component", "get_hdl_best_practices"]

