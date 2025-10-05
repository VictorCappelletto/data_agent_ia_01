"""
DPL Agent v3.0 - Domain Services

Domain Services implement business logic that doesn't naturally fit
within a single entity. They orchestrate operations across entities
and enPlatform domain rules.
"""

from typing import List, Optional, Dict, Tuple
from datetime import datetime, timedelta

from ..entities.hdl_entities import (
    DPLTable,
    DPLPipeline,
    DPLWorkflow,
    DPLError,
)
from ..value_objects import (
    Environment,
    PipelineType,
    DPLLayer,
    PipelineStatus,
    ErrorSeverity,
    ErrorContext,
    PipelineMetrics,
    QualityMetrics,
)


# ============================================================================
# DOMAIN SERVICES
# ============================================================================

class DPLPipelineService:
    """
    Service for DPL pipeline business logic.
    
    Implements domain rules for pipeline operations,
    error handling, and performance analysis.
    """
    
    @staticmethod
    def should_retry_pipeline(pipeline: DPLPipeline) -> bool:
        """
        Determine if a failed pipeline should be retried.
        
        Business Rules:
        - Can retry if under max retry limit
        - Don't retry if has critical errors
        - Don't retry if consecutive failures >= 3
        """
        if not pipeline.can_retry():
            return False
        
        if pipeline.has_critical_errors:
            return False
        
        if pipeline.consecutive_failures >= 3:
            return False
        
        return True
    
    @staticmethod
    def calculate_pipeline_health_score(pipeline: DPLPipeline) -> float:
        """
        Calculate pipeline health score (0-100).
        
        Factors:
        - Success rate (40%)
        - Performance metrics (30%)
        - Error severity (20%)
        - Execution frequency (10%)
        """
        score = 0.0
        
        # Success rate component
        if pipeline.consecutive_failures == 0:
            score += 40.0
        else:
            # Deduct based on consecutive failures
            failure_penalty = min(pipeline.consecutive_failures * 10, 40)
            score += max(0, 40 - failure_penalty)
        
        # Performance metrics component
        if pipeline.metrics and pipeline.metrics.is_healthy:
            score += 30.0
        elif pipeline.metrics:
            # Partial score based on success rate
            score += pipeline.metrics.success_rate * 0.3
        
        # Error severity component
        if not pipeline.has_critical_errors:
            score += 20.0
        elif pipeline.errors:
            # Deduct based on error severity
            critical_count = sum(1 for e in pipeline.errors if e.is_critical)
            score += max(0, 20 - (critical_count * 5))
        else:
            score += 20.0
        
        # Execution frequency component
        if pipeline.last_successful_run:
            hours_since_success = (datetime.utcnow() - pipeline.last_successful_run).total_seconds() / 3600
            if hours_since_success < 24:
                score += 10.0
            elif hours_since_success < 48:
                score += 5.0
        
        return round(score, 2)
    
    @staticmethod
    def recommend_optimization(pipeline: DPLPipeline) -> List[str]:
        """
        Generate optimization recommendations for pipeline.
        
        Returns:
            List of actionable recommendations
        """
        recommendations = []
        
        if not pipeline.metrics:
            recommendations.append("Enable metrics collection for performance insights")
            return recommendations
        
        # Throughput recommendations
        if pipeline.metrics.throughput_records_per_second < 100:
            recommendations.append(
                "Low throughput detected. Consider: "
                "1) Increase cluster resources "
                "2) Optimize transformations "
                "3) Review data skew"
            )
        
        # Success rate recommendations
        if pipeline.metrics.success_rate < 95.0:
            recommendations.append(
                f"Success rate is {pipeline.metrics.success_rate:.1f}%. "
                "Investigate data quality issues and add validation logic"
            )
        
        # Execution time recommendations
        if pipeline.metrics.execution_time_seconds > 3600:  # > 1 hour
            recommendations.append(
                "Pipeline execution exceeds 1 hour. Consider: "
                "1) Partition optimization "
                "2) Incremental processing "
                "3) Resource scaling"
            )
        
        # Memory recommendations
        if pipeline.metrics.memory_peak_mb and pipeline.metrics.memory_peak_mb > 50000:  # > 50GB
            recommendations.append(
                "High memory usage detected. Consider: "
                "1) Reduce broadcast joins "
                "2) Implement spill to disk "
                "3) Process in smaller batches"
            )
        
        return recommendations
    
    @staticmethod
    def detect_anomaly(
        pipeline: DPLPipeline,
        historical_metrics: List[PipelineMetrics]
    ) -> Optional[str]:
        """
        Detect anomalies in pipeline performance.
        
        Compares current metrics against historical baseline.
        """
        if not pipeline.metrics or not historical_metrics:
            return None
        
        # Calculate baseline averages
        avg_throughput = sum(m.throughput_records_per_second for m in historical_metrics) / len(historical_metrics)
        avg_execution_time = sum(m.execution_time_seconds for m in historical_metrics) / len(historical_metrics)
        
        current = pipeline.metrics
        
        # Detect throughput anomaly (>50% deviation)
        if abs(current.throughput_records_per_second - avg_throughput) / avg_throughput > 0.5:
            if current.throughput_records_per_second < avg_throughput:
                return f"Throughput degradation detected: {current.throughput_records_per_second:.1f} vs avg {avg_throughput:.1f} records/sec"
            else:
                return f"Unusual throughput spike: {current.throughput_records_per_second:.1f} vs avg {avg_throughput:.1f} records/sec"
        
        # Detect execution time anomaly (>50% deviation)
        if abs(current.execution_time_seconds - avg_execution_time) / avg_execution_time > 0.5:
            if current.execution_time_seconds > avg_execution_time:
                return f"Execution time anomaly: {current.execution_time_seconds:.0f}s vs avg {avg_execution_time:.0f}s"
        
        return None


class DPLWorkflowService:
    """
    Service for DPL workflow business logic.
    
    Implements domain rules for workflow orchestration,
    dependency management, and status monitoring.
    """
    
    @staticmethod
    def can_execute_workflow(workflow: DPLWorkflow, all_workflows: List[DPLWorkflow]) -> Tuple[bool, Optional[str]]:
        """
        Check if workflow can be executed based on dependencies.
        
        Returns:
            (can_execute: bool, reason: Optional[str])
        """
        # Check if workflow has dependencies
        if not workflow.has_dependencies:
            return True, None
        
        # Check status of dependent workflows
        for dep_name in workflow.depends_on:
            dep_workflow = next((w for w in all_workflows if w.name == dep_name), None)
            
            if not dep_workflow:
                return False, f"Dependency '{dep_name}' not found"
            
            if dep_workflow.status != PipelineStatus.SUCCESS:
                return False, f"Dependency '{dep_name}' has status: {dep_workflow.status.value}"
        
        return True, None
    
    @staticmethod
    def calculate_workflow_sla_compliance(
        workflow: DPLWorkflow,
        sla_duration_seconds: int
    ) -> Tuple[bool, Optional[float]]:
        """
        Calculate SLA compliance for workflow.
        
        Returns:
            (is_compliant: bool, actual_duration_seconds: Optional[float])
        """
        if not workflow.start_time or not workflow.end_time:
            return True, None  # Can't determine if not completed
        
        actual_duration = (workflow.end_time - workflow.start_time).total_seconds()
        is_compliant = actual_duration <= sla_duration_seconds
        
        return is_compliant, actual_duration
    
    @staticmethod
    def identify_bottleneck_pipelines(workflow: DPLWorkflow) -> List[Tuple[DPLPipeline, str]]:
        """
        Identify pipeline bottlenecks in workflow.
        
        Returns:
            List of (pipeline, reason) tuples
        """
        bottlenecks = []
        
        if not workflow.pipelines:
            return bottlenecks
        
        # Calculate average execution time
        completed_pipelines = [p for p in workflow.pipelines if p.execution_duration_seconds]
        if not completed_pipelines:
            return bottlenecks
        
        avg_duration = sum(p.execution_duration_seconds for p in completed_pipelines) / len(completed_pipelines)
        
        # Identify slow pipelines (>2x average)
        for pipeline in completed_pipelines:
            if pipeline.execution_duration_seconds > avg_duration * 2:
                bottlenecks.append((
                    pipeline,
                    f"Execution time {pipeline.execution_duration_seconds:.0f}s is {(pipeline.execution_duration_seconds/avg_duration):.1f}x average"
                ))
        
        # Identify failed pipelines
        for pipeline in workflow.pipelines:
            if pipeline.is_failed:
                bottlenecks.append((pipeline, f"Pipeline failed with status: {pipeline.status.value}"))
        
        return bottlenecks
    
    @staticmethod
    def recommend_workflow_optimization(workflow: DPLWorkflow) -> List[str]:
        """Generate optimization recommendations for workflow."""
        recommendations = []
        
        # Check success rate
        if workflow.success_rate < 95.0:
            recommendations.append(
                f"Workflow success rate is {workflow.success_rate:.1f}%. "
                "Review pipeline error handling and add retry logic"
            )
        
        # Check for failed pipelines
        failed = workflow.failed_pipelines
        if failed:
            recommendations.append(
                f"{len(failed)} pipeline(s) failing consistently. "
                f"Priority: {', '.join(p.name for p in failed[:3])}"
            )
        
        # Check for bottlenecks
        if workflow.pipelines:
            bottlenecks = DPLWorkflowService.identify_bottleneck_pipelines(workflow)
            if bottlenecks:
                recommendations.append(
                    f"{len(bottlenecks)} bottleneck(s) detected. "
                    "Consider parallelization or resource optimization"
                )
        
        return recommendations


class DPLDataQualityService:
    """
    Service for DPL data quality business logic.
    
    Implements domain rules for data quality validation,
    SCD2 validation, and quality scoring.
    """
    
    @staticmethod
    def validate_scd2_integrity(table: DPLTable) -> List[str]:
        """
        Validate SCD2 integrity for a table.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not table.scd2_enabled:
            return errors
        
        if not table.scd2_key_columns:
            errors.append("SCD2 enabled but no key columns defined")
        
        # Additional SCD2 validations would go here
        # (requires actual data access, so this is a placeholder)
        
        return errors
    
    @staticmethod
    def calculate_data_freshness_score(table: DPLTable) -> float:
        """
        Calculate data freshness score (0-100).
        
        Based on time since last processing.
        """
        if not table.last_processed_at:
            return 0.0
        
        hours_since_update = (datetime.utcnow() - table.last_processed_at).total_seconds() / 3600
        
        # Scoring based on pipeline type expectations
        if table.is_streaming:
            # Streaming should update every few minutes
            if hours_since_update < 0.5:  # < 30 minutes
                return 100.0
            elif hours_since_update < 2:
                return 80.0
            elif hours_since_update < 6:
                return 50.0
            else:
                return 20.0
        else:
            # Batch typically runs every 30 minutes to 1 hour
            if hours_since_update < 1:
                return 100.0
            elif hours_since_update < 4:
                return 80.0
            elif hours_since_update < 12:
                return 50.0
            else:
                return 20.0
    
    @staticmethod
    def should_trigger_quality_check(table: DPLTable) -> bool:
        """
        Determine if a quality check should be triggered.
        
        Business Rules:
        - Check if quality metrics are stale (>24 hours)
        - Check if table was recently updated
        - Check if previous quality was poor
        """
        # No quality metrics yet
        if not table.quality_metrics:
            return True
        
        # Quality metrics are stale (>24 hours)
        hours_since_update = (datetime.utcnow() - table.updated_at).total_seconds() / 3600
        if hours_since_update > 24:
            return True
        
        # Table was recently processed
        if table.last_processed_at:
            hours_since_process = (datetime.utcnow() - table.last_processed_at).total_seconds() / 3600
            if hours_since_process < 1:
                return True
        
        # Previous quality was poor
        if not table.has_good_quality:
            return True
        
        return False


class DPLErrorService:
    """
    Service for DPL error business logic.
    
    Implements domain rules for error classification,
    prioritization, and resolution strategies.
    """
    
    @staticmethod
    def classify_error_urgency(error: DPLError) -> str:
        """
        Classify error urgency level.
        
        Returns:
            "immediate", "high", "medium", or "low"
        """
        if error.context.severity == ErrorSeverity.CRITICAL:
            return "immediate"
        
        if error.is_recurring and error.occurrence_count > 3:
            return "immediate"
        
        if error.context.severity == ErrorSeverity.HIGH:
            return "high"
        
        if error.is_recurring:
            return "high"
        
        if error.context.severity == ErrorSeverity.MEDIUM:
            return "medium"
        
        return "low"
    
    @staticmethod
    def suggest_resolution_strategy(error: DPLError) -> List[str]:
        """
        Suggest resolution strategies for error.
        
        Returns:
            List of suggested actions
        """
        strategies = []
        
        # Use recovery suggestion from error context if available
        if error.context.recovery_suggestion:
            strategies.append(error.context.recovery_suggestion)
        
        # Error type specific strategies
        if "timeout" in error.error_type.lower():
            strategies.extend([
                "Increase timeout configuration",
                "Optimize query performance",
                "Scale cluster resources",
                "Check for data skew"
            ])
        
        elif "connection" in error.error_type.lower():
            strategies.extend([
                "Verify network connectivity",
                "Check credential validity",
                "Review firewall rules",
                "Implement retry logic"
            ])
        
        elif "validation" in error.error_type.lower():
            strategies.extend([
                "Review data quality at source",
                "Add data cleaning step",
                "Update validation rules",
                "Implement data profiling"
            ])
        
        elif "scd2" in error.error_type.lower():
            strategies.extend([
                "Run AdjustIsCurrent.py tool",
                "Verify key column configuration",
                "Check for duplicate records",
                "Review merge logic"
            ])
        
        else:
            strategies.append("Review error logs and stack trace for root cause")
        
        return strategies
    
    @staticmethod
    def should_escalate_error(error: DPLError) -> Tuple[bool, Optional[str]]:
        """
        Determine if error should be escalated.
        
        Returns:
            (should_escalate: bool, reason: Optional[str])
        """
        # Critical errors should always escalate
        if error.is_critical:
            return True, "Critical error severity"
        
        # Recurring errors (>5 occurrences) should escalate
        if error.occurrence_count > 5:
            return True, f"Error recurring {error.occurrence_count} times"
        
        # Unresolved for >24 hours
        if not error.is_resolved:
            hours_unresolved = (datetime.utcnow() - error.created_at).total_seconds() / 3600
            if hours_unresolved > 24:
                return True, f"Unresolved for {hours_unresolved:.1f} hours"
        
        return False, None


# ============================================================================
# DOMAIN SERVICE FACADE
# ============================================================================

class DPLDomainService:
    """
    Facade for all DPL domain services.
    
    Provides a unified interface to all domain business logic.
    """
    
    def __init__(self):
        self.pipeline = DPLPipelineService()
        self.workflow = DPLWorkflowService()
        self.quality = DPLDataQualityService()
        self.error = DPLErrorService()

