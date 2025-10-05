"""
DPL Agent v3.0 - Domain Value Objects

Value Objects are immutable objects that represent domain concepts
without a distinct identity. They are defined by their attributes.
"""

from enum import Enum
from typing import Optional
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# ENUMERATIONS
# ============================================================================

class Environment(str, Enum):
    """DPL environment types."""
    DEV = "DEV"
    SIT = "SIT"
    UAT = "UAT"
    PRD = "PRD"
    PROD = "PROD"  # Alias for PRD
    
    @property
    def catalog_suffix(self) -> str:
        """Get catalog suffix for environment."""
        if self == Environment.PRD or self == Environment.PROD:
            return ""  # Production has no suffix
        elif self == Environment.UAT:
            return "_uat"
        elif self == Environment.SIT:
            return "_sit"
        else:
            return "_dev"


class PipelineType(str, Enum):
    """DPL pipeline processing types."""
    STREAMING = "streaming"
    BATCH = "batch"
    HYBRID = "hybrid"  # Can run both modes


class DPLLayer(str, Enum):
    """DPL data layer types."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"  # For future KPI integration


class ErrorSeverity(str, Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PipelineStatus(str, Enum):
    """Pipeline execution status."""
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    PENDING = "pending"
    CANCELLED = "cancelled"


class WorkflowTriggerType(str, Enum):
    """Databricks workflow trigger types."""
    FILE_ARRIVAL = "file_arrival"  # Event Hub detection
    CRON = "cron"  # Scheduled
    MANUAL = "manual"  # Manual execution
    DEPENDENCY = "dependency"  # After another workflow


class SCD2Status(str, Enum):
    """SCD2 (Slowly Changing Dimension Type 2) status."""
    CURRENT = "current"  # is_current = true
    HISTORICAL = "historical"  # is_current = false


# ============================================================================
# VALUE OBJECTS
# ============================================================================

@dataclass(frozen=True)
class EntityName:
    """DPL entity name with validation."""
    name: str
    
    def __post_init__(self):
        """Validate entity name."""
        if not self.name:
            raise ValueError("Entity name cannot be empty")
        if not self.name.islower():
            raise ValueError(f"Entity name must be lowercase: {self.name}")
    
    @property
    def table_name(self) -> str:
        """Get table name format."""
        return self.name.replace("_", "").lower()
    
    @property
    def stream_collection_name(self) -> str:
        """Get streaming collection name format."""
        return f"{self.name}_stream"
    
    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class CatalogName:
    """DPL catalog name with environment suffix."""
    base_name: str
    environment: Environment
    
    @property
    def full_name(self) -> str:
        """Get full catalog name with environment suffix."""
        return f"{self.base_name}{self.environment.catalog_suffix}"
    
    def __str__(self) -> str:
        return self.full_name


@dataclass(frozen=True)
class TablePath:
    """Complete table path in Unity Catalog format."""
    catalog: CatalogName
    schema: str
    table: str
    
    @property
    def full_path(self) -> str:
        """Get full table path: catalog.schema.table"""
        return f"{self.catalog.full_name}.{self.schema}.{self.table}"
    
    @property
    def bronze_path(self) -> str:
        """Get bronze layer path."""
        return f"{self.catalog.full_name}.bronze.{self.table}"
    
    @property
    def silver_path(self) -> str:
        """Get silver layer path."""
        return f"{self.catalog.full_name}.silver.{self.table}_harmonized"
    
    def __str__(self) -> str:
        return self.full_path


@dataclass(frozen=True)
class WorkflowConfig:
    """Databricks workflow configuration."""
    name: str
    trigger_type: WorkflowTriggerType
    schedule: Optional[str] = None  # CRON expression
    timeout_seconds: Optional[int] = None
    max_concurrent_runs: int = 1
    retry_on_timeout: bool = False
    
    def __post_init__(self):
        """Validate workflow configuration."""
        if self.trigger_type == WorkflowTriggerType.CRON and not self.schedule:
            raise ValueError("CRON trigger requires schedule expression")


@dataclass(frozen=True)
class ErrorContext:
    """Context information for an error."""
    message: str
    severity: ErrorSeverity
    timestamp: datetime
    stack_trace: Optional[str] = None
    affected_records: Optional[int] = None
    recovery_suggestion: Optional[str] = None
    
    @property
    def is_critical(self) -> bool:
        """Check if error is critical."""
        return self.severity == ErrorSeverity.CRITICAL
    
    @property
    def requires_immediate_action(self) -> bool:
        """Check if error requires immediate action."""
        return self.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]


@dataclass(frozen=True)
class PipelineMetrics:
    """Pipeline execution metrics."""
    execution_time_seconds: float
    records_processed: int
    records_failed: int
    throughput_records_per_second: float
    memory_peak_mb: Optional[float] = None
    cpu_usage_percent: Optional[float] = None
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        total = self.records_processed + self.records_failed
        if total == 0:
            return 0.0
        return (self.records_processed / total) * 100
    
    @property
    def is_healthy(self) -> bool:
        """Check if pipeline metrics are healthy."""
        return (
            self.success_rate >= 95.0 and
            self.throughput_records_per_second > 0
        )


@dataclass(frozen=True)
class SCD2Metadata:
    """SCD2 metadata for tracking historical changes."""
    start_date: datetime
    end_date: Optional[datetime]
    is_current: bool
    version: int
    hash_key: Optional[str] = None  # MD5 hash for change detection
    
    @property
    def status(self) -> SCD2Status:
        """Get SCD2 status."""
        return SCD2Status.CURRENT if self.is_current else SCD2Status.HISTORICAL
    
    @property
    def is_active(self) -> bool:
        """Check if record is currently active."""
        return self.is_current and self.end_date is None


@dataclass(frozen=True)
class NotebookPath:
    """Databricks notebook path."""
    workspace_path: str
    notebook_name: str
    
    @property
    def full_path(self) -> str:
        """Get full notebook path."""
        return f"{self.workspace_path}/{self.notebook_name}"
    
    def __str__(self) -> str:
        return self.full_path


@dataclass(frozen=True)
class StreamingCheckpoint:
    """Streaming checkpoint configuration."""
    location: str
    schema_location: Optional[str] = None
    
    @property
    def checkpoint_path(self) -> str:
        """Get checkpoint path."""
        return self.location
    
    @property
    def schema_path(self) -> str:
        """Get schema location path."""
        return self.schema_location or f"{self.location}/_schema"


@dataclass(frozen=True)
class TriggerConfig:
    """Streaming trigger configuration."""
    mode: str  # "availableNow", "processingTime", "continuous"
    interval: Optional[str] = None  # For processingTime mode
    min_time_between_triggers_seconds: Optional[int] = None
    
    def __post_init__(self):
        """Validate trigger configuration."""
        valid_modes = ["availableNow", "processingTime", "continuous"]
        if self.mode not in valid_modes:
            raise ValueError(f"Invalid trigger mode: {self.mode}. Must be one of {valid_modes}")
        
        if self.mode == "processingTime" and not self.interval:
            raise ValueError("processingTime mode requires interval")


@dataclass(frozen=True)
class QualityMetrics:
    """Data quality metrics."""
    completeness_percent: float
    accuracy_percent: float
    consistency_percent: float
    timeliness_score: float
    total_records: int
    null_records: int
    duplicate_records: int
    
    @property
    def overall_quality_score(self) -> float:
        """Calculate overall quality score (0-100)."""
        return (
            self.completeness_percent * 0.3 +
            self.accuracy_percent * 0.3 +
            self.consistency_percent * 0.2 +
            self.timeliness_score * 0.2
        )
    
    @property
    def is_acceptable(self) -> bool:
        """Check if quality is acceptable (>= 90%)."""
        return self.overall_quality_score >= 90.0
    
    @property
    def null_rate(self) -> float:
        """Calculate null rate."""
        if self.total_records == 0:
            return 0.0
        return (self.null_records / self.total_records) * 100
    
    @property
    def duplicate_rate(self) -> float:
        """Calculate duplicate rate."""
        if self.total_records == 0:
            return 0.0
        return (self.duplicate_records / self.total_records) * 100


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_table_path(
    catalog_name: str,
    environment: Environment,
    schema: str,
    table: str
) -> TablePath:
    """
    Factory function to create TablePath.
    
    Args:
        catalog_name: Base catalog name
        environment: Environment (DEV, UAT, PRD)
        schema: Schema name (bronze, silver, gold)
        table: Table name
        
    Returns:
        TablePath instance
    """
    catalog = CatalogName(base_name=catalog_name, environment=environment)
    return TablePath(catalog=catalog, schema=schema, table=table)


def create_error_context(
    message: str,
    severity: ErrorSeverity,
    stack_trace: Optional[str] = None,
    recovery_suggestion: Optional[str] = None
) -> ErrorContext:
    """
    Factory function to create ErrorContext.
    
    Args:
        message: Error message
        severity: Error severity level
        stack_trace: Optional stack trace
        recovery_suggestion: Optional recovery suggestion
        
    Returns:
        ErrorContext instance
    """
    return ErrorContext(
        message=message,
        severity=severity,
        timestamp=datetime.utcnow(),
        stack_trace=stack_trace,
        recovery_suggestion=recovery_suggestion
    )

