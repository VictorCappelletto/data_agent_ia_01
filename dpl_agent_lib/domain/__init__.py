"""
DPL Agent v3.0 - Domain Layer

The Domain Layer contains the core business logic and rules.
It is the heart of the application and is independent of external concerns.

Components:
- Entities: Core business objects with identity
- Value Objects: Immutable objects defined by attributes
- Ports: Interfaces for external dependencies (Dependency Inversion)
- Services: Business logic that spans multiple entities
"""

from .entities.hdl_entities import (
    DPLTable,
    DPLPipeline,
    DPLWorkflow,
    DPLError,
    create_hdl_table,
    create_hdl_pipeline,
    create_hdl_workflow,
    create_hdl_error,
)

from .value_objects import (
    # Enums
    Environment,
    PipelineType,
    DPLLayer,
    ErrorSeverity,
    PipelineStatus,
    WorkflowTriggerType,
    SCD2Status,
    
    # Value Objects
    EntityName,
    CatalogName,
    TablePath,
    WorkflowConfig,
    ErrorContext,
    PipelineMetrics,
    SCD2Metadata,
    NotebookPath,
    StreamingCheckpoint,
    TriggerConfig,
    QualityMetrics,
    
    # Factory Functions
    create_table_path,
    create_error_context,
)

from .ports.hdl_repository_port import (
    # Repository Ports
    DPLTableRepository,
    DPLPipelineRepository,
    DPLWorkflowRepository,
    DPLErrorRepository,
    
    # Service Ports
    DatabricksServicePort,
    VectorStorePort,
    LLMServicePort,
    NotificationServicePort,
    
    # Unit of Work
    UnitOfWork,
)

from .services.hdl_domain_service import (
    DPLPipelineService,
    DPLWorkflowService,
    DPLDataQualityService,
    DPLErrorService,
    DPLDomainService,
)

__all__ = [
    # Entities
    "DPLTable",
    "DPLPipeline",
    "DPLWorkflow",
    "DPLError",
    "create_hdl_table",
    "create_hdl_pipeline",
    "create_hdl_workflow",
    "create_hdl_error",
    
    # Enums
    "Environment",
    "PipelineType",
    "DPLLayer",
    "ErrorSeverity",
    "PipelineStatus",
    "WorkflowTriggerType",
    "SCD2Status",
    
    # Value Objects
    "EntityName",
    "CatalogName",
    "TablePath",
    "WorkflowConfig",
    "ErrorContext",
    "PipelineMetrics",
    "SCD2Metadata",
    "NotebookPath",
    "StreamingCheckpoint",
    "TriggerConfig",
    "QualityMetrics",
    "create_table_path",
    "create_error_context",
    
    # Ports
    "DPLTableRepository",
    "DPLPipelineRepository",
    "DPLWorkflowRepository",
    "DPLErrorRepository",
    "DatabricksServicePort",
    "VectorStorePort",
    "LLMServicePort",
    "NotificationServicePort",
    "UnitOfWork",
    
    # Services
    "DPLPipelineService",
    "DPLWorkflowService",
    "DPLDataQualityService",
    "DPLErrorService",
    "DPLDomainService",
]

