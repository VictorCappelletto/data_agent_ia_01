"""
DPL Agent v3.0 - Domain Entities

Entities are objects with a distinct identity that runs through time and different states.
They represent core business objects in the DPL domain.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4

from ..value_objects import (
    Environment,
    PipelineType,
    DPLLayer,
    ErrorSeverity,
    PipelineStatus,
    WorkflowTriggerType,
    EntityName,
    TablePath,
    WorkflowConfig,
    ErrorContext,
    PipelineMetrics,
    SCD2Metadata,
    NotebookPath,
    StreamingCheckpoint,
    TriggerConfig,
    QualityMetrics,
)


# ============================================================================
# DOMAIN ENTITIES
# ============================================================================

@dataclass
class DPLTable:
    """
    Represents an DPL table in the data platform.
    
    Tables can exist in bronze or silver layers and can be
    processed via batch or streaming pipelines.
    """
    
    # Identity
    id: UUID = field(default_factory=uuid4)
    entity_name: EntityName = field(default=None)
    table_path: TablePath = field(default=None)
    
    # Properties
    layer: DPLLayer = DPLLayer.BRONZE
    pipeline_type: PipelineType = PipelineType.BATCH
    is_active: bool = True
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_processed_at: Optional[datetime] = None
    
    # SCD2 Configuration
    scd2_enabled: bool = True
    scd2_key_columns: List[str] = field(default_factory=list)
    
    # Schema
    schema_version: str = "1.0"
    column_count: Optional[int] = None
    estimated_size_gb: Optional[float] = None
    
    # Quality
    quality_metrics: Optional[QualityMetrics] = None
    
    def __post_init__(self):
        """Validate table after initialization."""
        if not self.entity_name:
            raise ValueError("Entity name is required")
        if not self.table_path:
            raise ValueError("Table path is required")
    
    @property
    def full_table_name(self) -> str:
        """Get full qualified table name."""
        return str(self.table_path)
    
    @property
    def is_bronze(self) -> bool:
        """Check if table is in bronze layer."""
        return self.layer == DPLLayer.BRONZE
    
    @property
    def is_silver(self) -> bool:
        """Check if table is in silver layer."""
        return self.layer == DPLLayer.SILVER
    
    @property
    def is_streaming(self) -> bool:
        """Check if table uses streaming pipeline."""
        return self.pipeline_type in [PipelineType.STREAMING, PipelineType.HYBRID]
    
    @property
    def is_batch(self) -> bool:
        """Check if table uses batch pipeline."""
        return self.pipeline_type in [PipelineType.BATCH, PipelineType.HYBRID]
    
    @property
    def has_good_quality(self) -> bool:
        """Check if table has acceptable quality."""
        if not self.quality_metrics:
            return False
        return self.quality_metrics.is_acceptable
    
    def update_quality_metrics(self, metrics: QualityMetrics) -> None:
        """Update table quality metrics."""
        self.quality_metrics = metrics
        self.updated_at = datetime.utcnow()
    
    def mark_processed(self) -> None:
        """Mark table as processed."""
        self.last_processed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def __str__(self) -> str:
        return f"DPLTable({self.entity_name}, {self.layer.value}, {self.pipeline_type.value})"


@dataclass
class DPLPipeline:
    """
    Represents an DPL data pipeline (batch or streaming).
    
    Pipelines process data from source to bronze/silver layers.
    """
    
    # Identity
    id: UUID = field(default_factory=uuid4)
    name: str = field(default="")
    pipeline_type: PipelineType = PipelineType.BATCH
    
    # Configuration
    source_entity: EntityName = field(default=None)
    target_table: DPLTable = field(default=None)
    notebook_path: NotebookPath = field(default=None)
    
    # Execution State
    status: PipelineStatus = PipelineStatus.PENDING
    current_run_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Performance
    metrics: Optional[PipelineMetrics] = None
    last_successful_run: Optional[datetime] = None
    consecutive_failures: int = 0
    
    # Streaming Specific
    checkpoint: Optional[StreamingCheckpoint] = None
    trigger_config: Optional[TriggerConfig] = None
    
    # Error Handling
    errors: List[ErrorContext] = field(default_factory=list)
    max_retries: int = 3
    retry_count: int = 0
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate pipeline after initialization."""
        if not self.name:
            raise ValueError("Pipeline name is required")
        if not self.source_entity:
            raise ValueError("Source entity is required")
    
    @property
    def is_running(self) -> bool:
        """Check if pipeline is currently running."""
        return self.status == PipelineStatus.RUNNING
    
    @property
    def is_failed(self) -> bool:
        """Check if pipeline has failed."""
        return self.status == PipelineStatus.FAILED
    
    @property
    def is_successful(self) -> bool:
        """Check if pipeline completed successfully."""
        return self.status == PipelineStatus.SUCCESS
    
    @property
    def has_critical_errors(self) -> bool:
        """Check if pipeline has critical errors."""
        return any(error.is_critical for error in self.errors)
    
    @property
    def requires_attention(self) -> bool:
        """Check if pipeline requires attention."""
        return (
            self.is_failed or
            self.has_critical_errors or
            self.consecutive_failures >= 2
        )
    
    @property
    def execution_duration_seconds(self) -> Optional[float]:
        """Calculate execution duration."""
        if not self.start_time or not self.end_time:
            return None
        return (self.end_time - self.start_time).total_seconds()
    
    @property
    def is_healthy(self) -> bool:
        """Check if pipeline is healthy."""
        return (
            self.consecutive_failures == 0 and
            not self.has_critical_errors and
            (self.metrics is None or self.metrics.is_healthy)
        )
    
    def start(self, run_id: str) -> None:
        """Start pipeline execution."""
        self.status = PipelineStatus.RUNNING
        self.current_run_id = run_id
        self.start_time = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def complete_success(self, metrics: PipelineMetrics) -> None:
        """Mark pipeline as successfully completed."""
        self.status = PipelineStatus.SUCCESS
        self.end_time = datetime.utcnow()
        self.metrics = metrics
        self.last_successful_run = self.end_time
        self.consecutive_failures = 0
        self.retry_count = 0
        self.updated_at = datetime.utcnow()
    
    def complete_failure(self, error: ErrorContext) -> None:
        """Mark pipeline as failed."""
        self.status = PipelineStatus.FAILED
        self.end_time = datetime.utcnow()
        self.errors.append(error)
        self.consecutive_failures += 1
        self.updated_at = datetime.utcnow()
    
    def can_retry(self) -> bool:
        """Check if pipeline can be retried."""
        return self.retry_count < self.max_retries
    
    def retry(self) -> None:
        """Retry pipeline execution."""
        if not self.can_retry():
            raise ValueError(f"Max retries ({self.max_retries}) exceeded")
        self.retry_count += 1
        self.status = PipelineStatus.PENDING
        self.updated_at = datetime.utcnow()
    
    def __str__(self) -> str:
        return f"DPLPipeline({self.name}, {self.pipeline_type.value}, {self.status.value})"


@dataclass
class DPLWorkflow:
    """
    Represents a Databricks workflow that orchestrates DPL pipelines.
    
    Workflows can contain multiple tasks and have complex dependencies.
    """
    
    # Identity
    id: UUID = field(default_factory=uuid4)
    workflow_id: str = field(default="")  # Databricks workflow ID
    name: str = field(default="")
    
    # Configuration
    config: WorkflowConfig = field(default=None)
    environment: Environment = Environment.PRD
    
    # Pipelines
    pipelines: List[DPLPipeline] = field(default_factory=list)
    
    # Execution State
    status: PipelineStatus = PipelineStatus.PENDING
    current_run_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Dependencies
    depends_on: List[str] = field(default_factory=list)  # Other workflow names
    triggers: List[str] = field(default_factory=list)  # Workflows triggered by this
    
    # Monitoring
    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    last_execution_time: Optional[datetime] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate workflow after initialization."""
        if not self.name:
            raise ValueError("Workflow name is required")
        if not self.config:
            raise ValueError("Workflow configuration is required")
    
    @property
    def is_streaming_workflow(self) -> bool:
        """Check if workflow handles streaming pipelines."""
        return any(p.pipeline_type == PipelineType.STREAMING for p in self.pipelines)
    
    @property
    def is_batch_workflow(self) -> bool:
        """Check if workflow handles batch pipelines."""
        return any(p.pipeline_type == PipelineType.BATCH for p in self.pipelines)
    
    @property
    def has_dependencies(self) -> bool:
        """Check if workflow has dependencies."""
        return len(self.depends_on) > 0
    
    @property
    def success_rate(self) -> float:
        """Calculate workflow success rate."""
        if self.execution_count == 0:
            return 0.0
        return (self.success_count / self.execution_count) * 100
    
    @property
    def is_healthy(self) -> bool:
        """Check if workflow is healthy."""
        return (
            self.success_rate >= 95.0 and
            self.failure_count == 0 and
            all(p.is_healthy for p in self.pipelines)
        )
    
    @property
    def failed_pipelines(self) -> List[DPLPipeline]:
        """Get list of failed pipelines."""
        return [p for p in self.pipelines if p.is_failed]
    
    @property
    def running_pipelines(self) -> List[DPLPipeline]:
        """Get list of running pipelines."""
        return [p for p in self.pipelines if p.is_running]
    
    def add_pipeline(self, pipeline: DPLPipeline) -> None:
        """Add pipeline to workflow."""
        self.pipelines.append(pipeline)
        self.updated_at = datetime.utcnow()
    
    def start_execution(self, run_id: str) -> None:
        """Start workflow execution."""
        self.status = PipelineStatus.RUNNING
        self.current_run_id = run_id
        self.start_time = datetime.utcnow()
        self.execution_count += 1
        self.last_execution_time = self.start_time
        self.updated_at = datetime.utcnow()
    
    def complete_execution(self, success: bool) -> None:
        """Complete workflow execution."""
        self.status = PipelineStatus.SUCCESS if success else PipelineStatus.FAILED
        self.end_time = datetime.utcnow()
        
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        self.updated_at = datetime.utcnow()
    
    def __str__(self) -> str:
        return f"DPLWorkflow({self.name}, {len(self.pipelines)} pipelines, {self.status.value})"


@dataclass
class DPLError:
    """
    Represents an error that occurred in DPL processing.
    
    Errors can be at table, pipeline, or workflow level.
    """
    
    # Identity
    id: UUID = field(default_factory=uuid4)
    
    # Error Details
    context: ErrorContext = field(default=None)
    error_type: str = ""  # TimeoutError, ValidationError, ConnectionError, etc.
    error_code: Optional[str] = None
    
    # Source
    source_pipeline: Optional[str] = None
    source_workflow: Optional[str] = None
    source_table: Optional[str] = None
    source_notebook: Optional[str] = None
    
    # Resolution
    is_resolved: bool = False
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    
    # Recurrence
    occurrence_count: int = 1
    first_occurrence: datetime = field(default_factory=datetime.utcnow)
    last_occurrence: datetime = field(default_factory=datetime.utcnow)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate error after initialization."""
        if not self.context:
            raise ValueError("Error context is required")
        if not self.error_type:
            raise ValueError("Error type is required")
    
    @property
    def is_critical(self) -> bool:
        """Check if error is critical."""
        return self.context.is_critical
    
    @property
    def requires_immediate_action(self) -> bool:
        """Check if error requires immediate action."""
        return self.context.requires_immediate_action and not self.is_resolved
    
    @property
    def is_recurring(self) -> bool:
        """Check if error is recurring."""
        return self.occurrence_count > 1
    
    @property
    def time_to_resolution_seconds(self) -> Optional[float]:
        """Calculate time to resolution."""
        if not self.is_resolved or not self.resolved_at:
            return None
        return (self.resolved_at - self.created_at).total_seconds()
    
    def mark_occurrence(self) -> None:
        """Mark another occurrence of this error."""
        self.occurrence_count += 1
        self.last_occurrence = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def resolve(self, notes: str, resolved_by: str) -> None:
        """Resolve the error."""
        self.is_resolved = True
        self.resolution_notes = notes
        self.resolved_at = datetime.utcnow()
        self.resolved_by = resolved_by
        self.updated_at = datetime.utcnow()
    
    def reopen(self) -> None:
        """Reopen a resolved error."""
        self.is_resolved = False
        self.resolution_notes = None
        self.resolved_at = None
        self.resolved_by = None
        self.mark_occurrence()
    
    def __str__(self) -> str:
        return f"DPLError({self.error_type}, {self.context.severity.value}, resolved={self.is_resolved})"


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_hdl_table(
    entity_name: str,
    table_path: TablePath,
    layer: DPLLayer,
    pipeline_type: PipelineType
) -> DPLTable:
    """Factory function to create DPLTable."""
    return DPLTable(
        entity_name=EntityName(entity_name),
        table_path=table_path,
        layer=layer,
        pipeline_type=pipeline_type
    )


def create_hdl_pipeline(
    name: str,
    source_entity: str,
    pipeline_type: PipelineType,
    target_table: Optional[DPLTable] = None
) -> DPLPipeline:
    """Factory function to create DPLPipeline."""
    return DPLPipeline(
        name=name,
        source_entity=EntityName(source_entity),
        pipeline_type=pipeline_type,
        target_table=target_table
    )


def create_hdl_workflow(
    name: str,
    workflow_id: str,
    config: WorkflowConfig,
    environment: Environment = Environment.PRD
) -> DPLWorkflow:
    """Factory function to create DPLWorkflow."""
    return DPLWorkflow(
        name=name,
        workflow_id=workflow_id,
        config=config,
        environment=environment
    )


def create_hdl_error(
    error_type: str,
    context: ErrorContext,
    source_pipeline: Optional[str] = None,
    source_workflow: Optional[str] = None
) -> DPLError:
    """Factory function to create DPLError."""
    return DPLError(
        error_type=error_type,
        context=context,
        source_pipeline=source_pipeline,
        source_workflow=source_workflow
    )

