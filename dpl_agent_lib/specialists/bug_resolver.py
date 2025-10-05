"""
DPL Agent v3.0 - Bug Resolver Specialist

Specializes in resolving DPL bugs and providing fix strategies.
Enhanced with RAG for historical bug patterns and solutions.
"""

from typing import List, Dict, Any, Optional
from langchain.tools import tool

from ..utils import get_logger, ResponseFormatter
from ..application.services import get_hdl_retriever_service

# Initialize logger
logger = get_logger(__name__)


class BugResolver:
    """
    DPL Bug Resolution Specialist.
    
    Enhanced with RAG for accessing historical bug solutions
    and DPL-specific troubleshooting knowledge.
    """
    
    # RAG service (lazy-loaded)
    _rag_service = None
    
    # Known bug solutions (fallback patterns)
    BUG_SOLUTIONS = {
        "scd2_is_current_broken": {
            "solution": "Run AdjustIsCurrent.py tool",
            "steps": [
                "Navigate to hdl/tests/",
                "Execute: python AdjustIsCurrent.py --entity {entity} --date {date}",
                "Verify is_current flags after execution",
                "Monitor next pipeline run"
            ]
        },
        "streaming_checkpoint_corrupt": {
            "solution": "Reset checkpoint location",
            "steps": [
                "Stop streaming pipeline",
                "Delete checkpoint directory in DBFS",
                "Restart pipeline with clean checkpoint",
                "Monitor for recovery"
            ]
        },
        "batch_document_storedb_connection": {
            "solution": "Refresh connection credentials",
            "steps": [
                "Verify CosmosDB connection string",
                "Check credential expiration",
                "Test connection with DatabaseConnection.py",
                "Restart pipeline after validation"
            ]
        }
    }
    
    @classmethod
    def _get_rag_service(cls):
        """Lazy initialization of RAG service."""
        if cls._rag_service is None:
            try:
                cls._rag_service = get_hdl_retriever_service()
                logger.debug("RAG service initialized for Bug Resolver")
            except Exception as e:
                logger.warning("RAG service initialization failed", error=str(e))
                cls._rag_service = None
        return cls._rag_service


@tool
def resolve_hdl_bug(
    bug_description: str,
    entity_name: Optional[str] = None
) -> str:
    """
    Provide bug resolution steps for DPL issues.
    
    Enhanced with RAG to search historical bug solutions and
    DPL-specific troubleshooting documentation.
    
    Args:
        bug_description: Description of the bug
        entity_name: Optional entity name
        
    Returns:
        Resolution steps and recommendations with knowledge sources
    """
    # Log operation
    logger.info("Resolving DPL bug", bug_description=bug_description, entity_name=entity_name)
    
    bug_lower = bug_description.lower()
    
    # Try RAG search for historical solutions
    rag_service = BugResolver._get_rag_service()
    knowledge_context = ""
    sources = []
    
    if rag_service:
        try:
            # Search for similar bug patterns
            search_query = f"{bug_description}"
            if entity_name:
                search_query += f" entity: {entity_name}"
            
            results = rag_service.search_error_patterns(search_query, k=3)
            
            if results:
                logger.debug("RAG found historical bug solutions", count=len(results))
                
                # Extract knowledge
                for doc in results:
                    knowledge_context += f"\n{doc.page_content}\n"
                    sources.append(doc.metadata.get("source", "Unknown"))
                
                # Enhance context
                knowledge_context = rag_service.enhance_context(
                    base_context=bug_description,
                    retrieved_docs=results
                )
                
        except Exception as e:
            logger.warning("RAG search failed, using fallback", error=str(e))
    
    # Match known bugs (with or without RAG enhancement)
    for bug_type, solution_data in BugResolver.BUG_SOLUTIONS.items():
        if bug_type.replace("_", " ") in bug_lower:
            logger.debug("Matched known bug", bug_type=bug_type)
            
            # Add additional notes
            additional_steps = [
                "Test in UAT environment first if possible",
                "Document the fix in JIRA",
                "Monitor for 24 hours after fix"
            ]
            
            all_steps = solution_data["steps"] + additional_steps
            
            response = ResponseFormatter.format_bug_resolution(
                bug_type=bug_type.replace("_", " ").title(),
                resolution_steps=all_steps,
                related_tools=["DebugIngestion.py", "AdjustIsCurrent.py"],
                estimated_time="30-60 minutes"
            )
            
            # Add knowledge context if available
            if knowledge_context:
                response += f"\n\nHISTORICAL CONTEXT:\n{knowledge_context[:500]}"
            
            # Add sources
            if sources:
                response += f"\n\nKNOWLEDGE SOURCES:\n"
                for source in set(sources):
                    response += f"- {source}\n"
            
            logger.info("Bug resolution guidance provided", bug_type=bug_type, rag_enhanced=bool(knowledge_context))
            return response
    
    # Generic resolution guidance (enhanced with RAG if available)
    logger.debug("Providing generic bug resolution guidance")
    
    investigation_steps = [
        "Reproduce the bug in controlled environment",
        "Isolate the affected component",
        "Review recent code changes",
        "Check for similar historical issues"
    ]
    
    resolution_steps = [
        "Implement targeted fix",
        "Add validation to prevent recurrence",
        "Test thoroughly in UAT",
        "Deploy to production with monitoring"
    ]
    
    post_resolution = [
        "Document root cause and fix",
        "Update monitoring/alerts if needed",
        "Share learnings with team"
    ]
    
    # If RAG found context, prioritize it
    if knowledge_context:
        all_steps = [
            "Review historical solutions from knowledge base",
            "Apply relevant patterns to current bug"
        ] + investigation_steps + resolution_steps + post_resolution
    else:
        all_steps = investigation_steps + resolution_steps + post_resolution
    
    response = ResponseFormatter.format_bug_resolution(
        bug_type="DPL Bug" if entity_name else "Generic Bug",
        resolution_steps=all_steps,
        related_tools=["DebugIngestion.py", "Databricks Workflows", "DPL Documentation"],
        estimated_time="Variable"
    )
    
    # Add knowledge context if available
    if knowledge_context:
        response += f"\n\nHISTORICAL SOLUTIONS FOUND:\n{knowledge_context[:500]}"
    
    # Add sources
    if sources:
        response += f"\n\nKNOWLEDGE SOURCES:\n"
        for source in set(sources):
            response += f"- {source}\n"
    
    logger.info("Generic bug resolution provided", rag_enhanced=bool(knowledge_context))
    return response


__all__ = ["BugResolver", "resolve_hdl_bug"]

