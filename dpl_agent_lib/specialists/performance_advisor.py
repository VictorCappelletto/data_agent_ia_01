"""
DPL Agent v3.0 - Performance Advisor Specialist

Specializes in DPL pipeline performance optimization.
Enhanced with RAG for optimization strategies and best practices.
"""

from typing import List, Dict, Any, Optional
from langchain.tools import tool

from ..utils import get_logger, ResponseFormatter
from ..application.services import get_hdl_retriever_service

# Initialize logger
logger = get_logger(__name__)


class PerformanceAdvisor:
    """
    DPL Performance Optimization Specialist.
    
    Enhanced with RAG to access optimization strategies,
    performance tuning guides, and DPL-specific best practices.
    """
    
    # RAG service (lazy-loaded)
    _rag_service = None
    
    @classmethod
    def _get_rag_service(cls):
        """Lazy initialization of RAG service."""
        if cls._rag_service is None:
            try:
                cls._rag_service = get_hdl_retriever_service()
                logger.debug("RAG service initialized for Performance Advisor")
            except Exception as e:
                logger.warning("RAG service initialization failed", error=str(e))
                cls._rag_service = None
        return cls._rag_service
    
    OPTIMIZATION_STRATEGIES = {
        "slow_execution": [
            "Increase cluster resources (workers, memory)",
            "Optimize partition strategy",
            "Review and optimize transformations",
            "Use broadcast joins for small tables",
            "Enable adaptive query execution"
        ],
        "low_throughput": [
            "Check for data skew in partitions",
            "Optimize shuffle operations",
            "Increase parallelism settings",
            "Review I/O bottlenecks",
            "Use Delta Lake optimization features"
        ],
        "high_memory_usage": [
            "Reduce broadcast join thresholds",
            "Process data in smaller batches",
            "Use spill to disk configuration",
            "Clear cache between operations",
            "Optimize dataframe operations"
        ],
        "many_small_files": [
            "Run OPTIMIZE command on Delta tables",
            "Configure auto-compaction",
            "Adjust file size targets",
            "Schedule regular optimization jobs"
        ]
    }


@tool
def optimize_hdl_pipeline(
    pipeline_name: str,
    performance_issue: str
) -> str:
    """
    Get performance optimization recommendations for DPL pipeline.
    
    Enhanced with RAG to search optimization strategies and
    performance tuning best practices from knowledge base.
    
    Args:
        pipeline_name: Name of the pipeline
        performance_issue: Description of performance issue
        
    Returns:
        Optimization recommendations with knowledge sources
    """
    # Log operation
    logger.info("Optimizing pipeline performance", pipeline_name=pipeline_name)
    
    issue_lower = performance_issue.lower()
    
    # Try RAG search for optimization strategies
    rag_service = PerformanceAdvisor._get_rag_service()
    knowledge_context = ""
    sources = []
    
    if rag_service:
        try:
            # Search for optimization strategies
            search_query = f"performance optimization {performance_issue} {pipeline_name}"
            results = rag_service.search_optimization_strategies(search_query, k=3)
            
            if results:
                logger.debug("RAG found optimization strategies", count=len(results))
                
                # Extract knowledge
                for doc in results:
                    knowledge_context += f"\n{doc.page_content}\n"
                    sources.append(doc.metadata.get("source", "Unknown"))
                
                # Enhance context
                knowledge_context = rag_service.enhance_context(
                    base_context=f"Pipeline: {pipeline_name}, Issue: {performance_issue}",
                    retrieved_docs=results
                )
                
        except Exception as e:
            logger.warning("RAG search failed, using fallback", error=str(e))
    
    # Match optimization strategy (with or without RAG)
    recommendations = []
    for issue_type, strategies in PerformanceAdvisor.OPTIMIZATION_STRATEGIES.items():
        if issue_type.replace("_", " ") in issue_lower:
            recommendations.extend(strategies)
            logger.debug("Matched performance issue", issue_type=issue_type)
            break
    
    if not recommendations:
        logger.debug("Using generic performance recommendations")
        recommendations = [
            "Enable detailed performance metrics",
            "Profile pipeline execution",
            "Analyze Spark UI for bottlenecks",
            "Review cluster configuration"
        ]
    
    # Add general best practices
    recommendations.extend([
        "Monitor execution metrics regularly",
        "Set performance baselines",
        "Use OptimizeDeltaTable.py for Delta optimization",
        "Review and tune cluster autoscaling"
    ])
    
    # Add DPL-specific recommendations
    if "stream" in pipeline_name.lower():
        recommendations.extend([
            "Check checkpoint efficiency and location",
            "Verify Event Hub configuration",
            "Review memory_optimized cluster sizing"
        ])
    elif "batch" in pipeline_name.lower() or "ingestion" in pipeline_name.lower():
        recommendations.extend([
            "Optimize CosmosDB query patterns",
            "Review SCD2 merge performance",
            "Check general_purpose cluster sizing"
        ])
    
    # Format response
    response = ResponseFormatter.format_performance_optimization(
        issue=performance_issue,
        recommendations=recommendations,
        expected_improvement="20-50% faster execution time"
    )
    
    # Add knowledge context if available
    if knowledge_context:
        response += f"\n\nOPTIMIZATION KNOWLEDGE:\n{knowledge_context[:500]}"
    
    # Add sources
    if sources:
        response += f"\n\nKNOWLEDGE SOURCES:\n"
        for source in set(sources):
            response += f"- {source}\n"
    
    logger.info("Performance optimization provided", count=len(recommendations), rag_enhanced=bool(knowledge_context))
    
    return response


__all__ = ["PerformanceAdvisor", "optimize_hdl_pipeline"]

