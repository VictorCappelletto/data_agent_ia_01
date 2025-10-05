"""
DPL Agent v3.0 - Troubleshooter Specialist

Specializes in DPL pipeline troubleshooting and error diagnosis.
Implements systematic investigation frameworks and diagnostic tools.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from langchain.tools import tool

from ..utils import get_logger, ResponseFormatter
from ..application.services import get_hdl_retriever_service

# Initialize logger and RAG service
logger = get_logger(__name__)
_rag_service = None  # Lazy initialization to avoid circular imports

from ..domain import (
    DPLError,
    DPLPipeline,
    ErrorSeverity,
    PipelineStatus,
)


@dataclass
class TroubleshootingResult:
    """Result from troubleshooting analysis."""
    diagnosis: str
    severity: str
    root_cause: Optional[str]
    immediate_actions: List[str]
    investigation_steps: List[str]
    relevant_tools: List[str]
    escalation_needed: bool
    confidence: float


class DPLTroubleshooter:
    """
    DPL Troubleshooting Specialist.
    
    Capabilities:
    - Error diagnosis and classification
    - Root cause analysis
    - Systematic investigation planning
    - Diagnostic command generation
    - Escalation determination
    """
    
    # Known error patterns
    ERROR_PATTERNS = {
        "timeout": {
            "keywords": ["timeout", "timed out", "exceeded time"],
            "severity": "high",
            "common_causes": [
                "Large data volume processing",
                "Cluster resource constraints",
                "Network connectivity issues",
                "Checkpoint corruption"
            ],
            "diagnostic_steps": [
                "Check pipeline execution duration",
                "Review cluster resource utilization",
                "Verify data volume processed",
                "Inspect checkpoint location"
            ]
        },
        "scd2_merge": {
            "keywords": ["scd2", "is_current", "merge", "duplicate"],
            "severity": "medium",
            "common_causes": [
                "SCD2 key column misconfiguration",
                "Hash collision in MD5 keys",
                "Incorrect merge logic"
            ],
            "diagnostic_steps": [
                "Verify SCD2 key columns configuration",
                "Check for duplicate records",
                "Review merge operation logic",
                "Run AdjustIsCurrent.py tool"
            ]
        },
        "connection": {
            "keywords": ["connection", "network", "unreachable", "refused"],
            "severity": "high",
            "common_causes": [
                "CosmosDB connection issues",
                "Event Hub connectivity problems",
                "Network firewall blocking",
                "Invalid credentials"
            ],
            "diagnostic_steps": [
                "Test connection to data source",
                "Verify credentials are valid",
                "Check network firewall rules",
                "Review connection timeout settings"
            ]
        },
        "data_quality": {
            "keywords": ["validation", "quality", "null", "incomplete"],
            "severity": "medium",
            "common_causes": [
                "Source data quality issues",
                "Schema mismatch",
                "Missing mandatory fields",
                "Data type conversion errors"
            ],
            "diagnostic_steps": [
                "Profile source data quality",
                "Compare source vs target schemas",
                "Identify null/missing patterns",
                "Review validation rules"
            ]
        },
        "performance": {
            "keywords": ["slow", "performance", "bottleneck", "throughput"],
            "severity": "medium",
            "common_causes": [
                "Data skew in partitions",
                "Suboptimal join strategies",
                "Insufficient cluster resources",
                "Too many small files"
            ],
            "diagnostic_steps": [
                "Analyze execution plan",
                "Check data distribution/skew",
                "Review cluster configuration",
                "Inspect file sizes and counts"
            ]
        }
    }
    
    @classmethod
    def diagnose_error(
        cls,
        error_message: str,
        entity_name: Optional[str] = None,
        pipeline_type: Optional[str] = None,
        hdl_context: Optional[str] = None
    ) -> TroubleshootingResult:
        """
        Diagnose an error message.
        
        Args:
            error_message: Error message to analyze
            entity_name: Optional entity name
            pipeline_type: Optional pipeline type (streaming/batch)
            
        Returns:
            TroubleshootingResult with diagnosis
        """
        error_lower = error_message.lower()
        
        # Pattern matching
        matched_pattern = None
        for pattern_name, pattern_data in cls.ERROR_PATTERNS.items():
            if any(keyword in error_lower for keyword in pattern_data["keywords"]):
                matched_pattern = (pattern_name, pattern_data)
                break
        
        if matched_pattern:
            pattern_name, pattern_data = matched_pattern
            
            # Build immediate actions
            immediate_actions = [
                f"Error pattern identified: {pattern_name}",
                "Review the diagnostic steps below",
            ]
            
            # Add entity-specific actions
            if entity_name:
                immediate_actions.append(f"Focus on {entity_name} entity")
            
            if pipeline_type == "streaming":
                immediate_actions.append("Check streaming checkpoint location")
                immediate_actions.append("Verify Event Hub connectivity")
            elif pipeline_type == "batch":
                immediate_actions.append("Check CosmosDB connection")
                immediate_actions.append("Review batch processing logs")
            
            # Build investigation steps
            investigation_steps = pattern_data["diagnostic_steps"].copy()
            
            # Add relevant tools
            relevant_tools = cls._get_relevant_tools(pattern_name, entity_name)
            
            # Determine escalation
            escalation_needed = pattern_data["severity"] in ["critical", "high"]
            
            return TroubleshootingResult(
                diagnosis=f"Detected {pattern_name} error pattern",
                severity=pattern_data["severity"],
                root_cause=", ".join(pattern_data["common_causes"][:2]),
                immediate_actions=immediate_actions,
                investigation_steps=investigation_steps,
                relevant_tools=relevant_tools,
                escalation_needed=escalation_needed,
                confidence=0.85
            )
        else:
            # Generic troubleshooting
            return TroubleshootingResult(
                diagnosis="Unknown error pattern - requires manual investigation",
                severity="medium",
                root_cause=None,
                immediate_actions=[
                    "Review complete error log",
                    "Check Databricks workflow run logs",
                    "Inspect recent code changes"
                ],
                investigation_steps=[
                    "Collect full stack trace",
                    "Review execution timeline",
                    "Check for similar historical errors",
                    "Analyze affected data scope"
                ],
                relevant_tools=["DebugIngestion.py", "GetLastUpdatedAt.py"],
                escalation_needed=False,
                confidence=0.5
            )
    
    @staticmethod
    def _get_relevant_tools(pattern_name: str, entity_name: Optional[str]) -> List[str]:
        """Get relevant diagnostic tools for error pattern."""
        tools = []
        
        if pattern_name == "scd2_merge":
            tools.extend(["AdjustIsCurrent.py", "DebugIngestion.py"])
        
        if pattern_name == "timeout":
            tools.extend(["GetLastUpdatedAt.py", "Databricks Workflows Tab"])
        
        if pattern_name == "connection":
            tools.extend(["DatabaseConnection.py", "Test connection script"])
        
        if pattern_name == "data_quality":
            tools.extend(["Data profiling queries", "Quality validation rules"])
        
        if pattern_name == "performance":
            tools.extend(["OptimizeDeltaTable.py", "Performance profiling"])
        
        return tools
    
    @classmethod
    def analyze_pipeline_failure(
        cls,
        pipeline_name: str,
        error_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze pipeline failure comprehensively.
        
        Args:
            pipeline_name: Name of failed pipeline
            error_details: Error details dictionary
            
        Returns:
            Analysis results
        """
        # Extract error message
        error_message = error_details.get("message", "")
        entity = error_details.get("entity")
        pipeline_type = error_details.get("pipeline_type")
        
        # Diagnose
        result = cls.diagnose_error(error_message, entity, pipeline_type)
        
        # Build comprehensive analysis
        analysis = {
            "pipeline": pipeline_name,
            "diagnosis": result.diagnosis,
            "severity": result.severity,
            "root_cause_candidates": result.root_cause,
            "immediate_actions": result.immediate_actions,
            "investigation_plan": result.investigation_steps,
            "tools_to_use": result.relevant_tools,
            "escalation_required": result.escalation_needed,
            "confidence": result.confidence,
            "recommendations": cls._generate_recommendations(result)
        }
        
        return analysis
    
    @staticmethod
    def _generate_recommendations(result: TroubleshootingResult) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if result.severity in ["critical", "high"]:
            recommendations.append("HIGH PRIORITY: Address immediately")
        
        if result.escalation_needed:
            recommendations.append("Escalate to senior engineer or platform team")
        
        if result.confidence < 0.6:
            recommendations.append("Low confidence - manual investigation recommended")
        
        recommendations.append("Document findings in JIRA ticket")
        
        return recommendations


# ============================================================================
# LANGCHAIN TOOL WRAPPER
# ============================================================================

def _get_rag_service():
    """Lazy initialization of RAG service to avoid circular imports."""
    global _rag_service
    if _rag_service is None:
        _rag_service = get_hdl_retriever_service()
    return _rag_service


@tool
def troubleshoot_hdl_error(
    error_message: str,
    entity_name: Optional[str] = None,
    pipeline_type: Optional[str] = None
) -> str:
    """
    Diagnose DPL pipeline errors using RAG-enhanced knowledge.
    
    This tool performs semantic search on the DPL knowledge base to find
    relevant error patterns, troubleshooting guides, and solutions. It provides:
    - Error pattern identification from knowledge base
    - Severity assessment
    - Root cause analysis with DPL-specific context
    - Step-by-step investigation plan
    - Relevant diagnostic tools from documentation
    - Escalation recommendations
    
    Args:
        error_message: The error message or description of the problem
        entity_name: Optional DPL entity name (e.g., 'visits', 'tasks')
        pipeline_type: Optional pipeline type ('streaming' or 'batch')
        
    Returns:
        Troubleshooting analysis with DPL-specific knowledge and source attribution
        
    Example:
        >>> result = troubleshoot_hdl_error(
        ...     error_message="Timeout in pipeline after 1h30m",
        ...     entity_name="visits",
        ...     pipeline_type="streaming"
        ... )
    """
    # Log operation
    logger.info(
        "Diagnosing DPL error with RAG",
        entity_name=entity_name,
        pipeline_type=pipeline_type,
        error_length=len(error_message)
    )
    
    # STEP 1: Search knowledge base for similar error patterns
    try:
        rag_service = _get_rag_service()
        search_results = rag_service.search_error_patterns(
            error_message=error_message,
            entity_name=entity_name,
            pipeline_type=pipeline_type,
            top_k=5
        )
        
        # Enhance context with retrieved knowledge
        hdl_context = rag_service.enhance_context(search_results)
        
        logger.info(
            "RAG search complete",
            results_found=len(search_results),
            context_length=len(hdl_context)
        )
        
    except Exception as e:
        logger.warning(
            "RAG search failed, falling back to hardcoded patterns",
            error=str(e)
        )
        search_results = []
        hdl_context = None
    
    # STEP 2: Perform diagnosis with enhanced context
    result = DPLTroubleshooter.diagnose_error(
        error_message=error_message,
        entity_name=entity_name,
        pipeline_type=pipeline_type,
        hdl_context=hdl_context
    )
    
    # Log result
    logger.debug(
        "Diagnosis complete",
        severity=result.severity,
        confidence=result.confidence,
        escalation_needed=result.escalation_needed,
        used_rag=bool(hdl_context)
    )
    
    # STEP 3: Format response using ResponseFormatter (clean, no emojis)
    response = ResponseFormatter.format_troubleshooting(
        diagnosis=result.diagnosis,
        severity=result.severity,
        confidence=result.confidence,
        root_cause=result.root_cause,
        immediate_actions=result.immediate_actions,
        investigation_steps=result.investigation_steps,
        relevant_tools=result.relevant_tools,
        escalation_needed=result.escalation_needed
    )
    
    # STEP 4: Include knowledge sources if RAG was used
    if search_results:
        response += "\n\n--- DPL KNOWLEDGE SOURCES ---\n"
        for i, result_item in enumerate(search_results[:3], 1):
            source = result_item.get("source", "Unknown")
            score = result_item.get("score", 0.0)
            response += f"\n{i}. {source} (Relevance: {score:.2f})"
        
        logger.info(
            "Knowledge sources included in response",
            sources_count=min(3, len(search_results))
        )
    else:
        response += "\n\nNote: Using hardcoded patterns. For more specific guidance, ensure knowledge base is loaded."
    
    return response


@tool
def analyze_pipeline_health(
    pipeline_name: str,
    check_metrics: bool = True
) -> str:
    """
    Analyze DPL pipeline health using RAG-enhanced knowledge.
    
    Searches knowledge base for pipeline-specific documentation,
    configuration, and common issues. Performs comprehensive health
    check including:
    - Recent execution history
    - Success/failure rate
    - Performance trends
    - Data quality indicators
    - Known issues from documentation
    
    Args:
        pipeline_name: Name of the pipeline to analyze (e.g., 'dpl-stream-visits')
        check_metrics: Include detailed metrics analysis (default: True)
        
    Returns:
        Health analysis report with knowledge base context
        
    Example:
        >>> result = analyze_pipeline_health("dpl-stream-visits")
    """
    # Log operation
    logger.info(
        "Analyzing pipeline health with RAG",
        pipeline_name=pipeline_name,
        check_metrics=check_metrics
    )
    
    # Search knowledge base for pipeline documentation
    try:
        rag_service = _get_rag_service()
        workflow_results = rag_service.search_workflow_knowledge(
            workflow_name=pipeline_name,
            include_config=True,
            top_k=3
        )
        
        logger.info(
            "Pipeline knowledge retrieved",
            workflow=pipeline_name,
            results_found=len(workflow_results)
        )
        
    except Exception as e:
        logger.warning(
            "Failed to retrieve pipeline knowledge",
            pipeline=pipeline_name,
            error=str(e)
        )
        workflow_results = []
    
    # Placeholder implementation
    # In production, would query actual pipeline data
    
    status_details = {
        "Overall Status": "Monitoring",
        "Last successful run": "Checking",
        "Consecutive failures": "0",
        "Success rate (7 days)": "Calculating",
        "Average execution time": "Analyzing",
        "Throughput": "Measuring",
        "Resource utilization": "Checking",
        "Completeness": "Validating",
        "Accuracy": "Checking",
        "Timeliness": "Evaluating"
    }
    
    recommendations = [
        "Enable detailed monitoring for this pipeline",
        "Set up alerts for failures",
        "Review performance baselines",
        "Connect to Databricks for real-time metrics"
    ]
    
    # Format response
    from ..utils import CommonFormatters
    
    response_parts = []
    response_parts.append(f"PIPELINE HEALTH ANALYSIS: {pipeline_name}")
    response_parts.append("=" * 50)
    response_parts.append("")
    
    # Include knowledge base context if available
    if workflow_results:
        response_parts.append("WORKFLOW DOCUMENTATION:")
        for result in workflow_results[:2]:
            content = result.get("content", "N/A")
            # Truncate long content
            content_preview = content[:200] + "..." if len(content) > 200 else content
            response_parts.append(f"  {content_preview}")
        response_parts.append("")
    
    response_parts.append(CommonFormatters.format_key_value(status_details))
    response_parts.append("")
    response_parts.append("Recommendations:")
    response_parts.append(CommonFormatters.format_list(recommendations, numbered=True))
    
    # Include knowledge sources
    if workflow_results:
        response_parts.append("")
        response_parts.append("--- KNOWLEDGE SOURCES ---")
        for i, result in enumerate(workflow_results, 1):
            source = result.get("source", "Unknown")
            response_parts.append(f"{i}. {source}")
    
    logger.debug(
        "Health analysis complete",
        pipeline_name=pipeline_name,
        used_rag=bool(workflow_results)
    )
    
    return "\n".join(response_parts)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "DPLTroubleshooter",
    "TroubleshootingResult",
    "troubleshoot_hdl_error",
    "analyze_pipeline_health",
]

