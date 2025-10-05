"""
DPL Agent v3.0 - Quality Assistant Specialist

Specializes in DPL data quality validation and monitoring.
Enhanced with RAG for quality validation rules and best practices.
"""

from typing import List, Dict, Any, Optional
from langchain.tools import tool

from ..utils import get_logger, ResponseFormatter, CommonFormatters
from ..application.services import get_hdl_retriever_service

# Initialize logger
logger = get_logger(__name__)


class QualityAssistant:
    """
    DPL Data Quality Specialist.
    
    Enhanced with RAG for accessing quality validation rules,
    data quality best practices, and entity-specific quality checks.
    """
    
    # RAG service (lazy-loaded)
    _rag_service = None
    
    @classmethod
    def _get_rag_service(cls):
        """Lazy initialization of RAG service."""
        if cls._rag_service is None:
            try:
                cls._rag_service = get_hdl_retriever_service()
                logger.debug("RAG service initialized for Quality Assistant")
            except Exception as e:
                logger.warning("RAG service initialization failed", error=str(e))
                cls._rag_service = None
        return cls._rag_service
    
    QUALITY_CHECKS = {
        "completeness": [
            "Check for null values in mandatory fields",
            "Verify all expected records are present",
            "Compare source vs target record counts",
            "Validate completeness SLAs"
        ],
        "accuracy": [
            "Validate data type conversions",
            "Check business rule compliance",
            "Verify calculated fields",
            "Cross-reference with source data"
        ],
        "consistency": [
            "Validate referential integrity",
            "Check for duplicate records",
            "Verify SCD2 is_current flags",
            "Validate cross-table relationships"
        ],
        "timeliness": [
            "Check data freshness",
            "Verify processing SLAs",
            "Monitor ingestion lag",
            "Validate event time vs processing time"
        ]
    }


@tool
def validate_hdl_data_quality(
    entity_name: str,
    quality_dimension: str = "all"
) -> str:
    """
    Validate data quality for DPL entity.
    
    Enhanced with RAG to search quality validation rules and
    entity-specific quality requirements from knowledge base.
    
    Args:
        entity_name: DPL entity to validate (e.g., 'visits', 'tasks')
        quality_dimension: Specific dimension ('completeness', 'accuracy', 'consistency', 'timeliness', 'all')
        
    Returns:
        Quality validation checklist and recommendations with knowledge sources
    """
    # Log operation
    logger.info("Validating data quality", entity_name=entity_name, dimension=quality_dimension)
    
    # Try RAG search for quality rules
    rag_service = QualityAssistant._get_rag_service()
    knowledge_context = ""
    sources = []
    
    if rag_service:
        try:
            # Search for quality validation rules
            search_query = f"data quality validation {entity_name} {quality_dimension}"
            results = rag_service.search_quality_validation_rules(search_query, k=3)
            
            if results:
                logger.debug("RAG found quality validation rules", count=len(results))
                for doc in results:
                    knowledge_context += f"\n{doc.page_content}\n"
                    sources.append(doc.metadata.get("source", "Unknown"))
        except Exception as e:
            logger.warning("RAG search failed, using fallback", error=str(e))
    
    # Collect quality checks
    all_findings = []
    
    if quality_dimension == "all":
        for dimension, dimension_checks in QualityAssistant.QUALITY_CHECKS.items():
            all_findings.append(f"{dimension.upper()}:")
            all_findings.extend(f"  - {check}" for check in dimension_checks)
    else:
        dimension_checks = QualityAssistant.QUALITY_CHECKS.get(
            quality_dimension,
            ["No specific checks defined"]
        )
        all_findings.extend(dimension_checks)
    
    # Add DPL-specific validations
    all_findings.extend([
        "",
        "DPL-SPECIFIC VALIDATIONS:",
        "  - Verify SCD2 integrity (is_current, start_date, end_date)",
        "  - Check MD5 hash uniqueness for deduplication",
        "  - Validate traceability fields (process_timestamp, batchId)",
        "  - Verify partition alignment",
        "",
        "RECOMMENDED TOOLS:",
        "  - Data profiling queries in hdl/monitoring/",
        "  - Quality metrics dashboards",
        "  - CompletenessRemoteJobTrigger for automated checks",
        "",
        "ACTION ITEMS:",
        "  1. Run quality checks on latest data",
        "  2. Set up automated quality monitoring",
        "  3. Define quality SLAs and alerts",
        "  4. Document quality baselines"
    ])
    
    # Format response
    response = ResponseFormatter.format_quality_report(
        entity_name=entity_name,
        dimension=quality_dimension,
        findings=all_findings,
        status="Ready for validation"
    )
    
    # Add knowledge context if available
    if knowledge_context:
        response += f"\n\nQUALITY KNOWLEDGE FROM KB:\n{knowledge_context[:500]}"
    
    # Add sources
    if sources:
        response += f"\n\nKNOWLEDGE SOURCES:\n"
        for source in set(sources):
            response += f"- {source}\n"
    
    logger.info("Quality validation checklist provided", entity_name=entity_name, rag_enhanced=bool(knowledge_context))
    
    return response


__all__ = ["QualityAssistant", "validate_hdl_data_quality"]

