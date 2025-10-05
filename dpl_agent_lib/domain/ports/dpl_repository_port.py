"""
DPL Agent v3.0 - Repository Ports (Interfaces)

Ports define interfaces for external dependencies using Dependency Inversion Principle.
They allow the domain layer to remain independent of infrastructure implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

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
    EntityName,
)


# ============================================================================
# REPOSITORY PORTS
# ============================================================================

class DPLTableRepository(ABC):
    """
    Port for DPL table data access.
    
    Infrastructure layer will implement this interface
    to provide actual table data operations.
    """
    
    @abstractmethod
    async def find_by_id(self, table_id: UUID) -> Optional[DPLTable]:
        """Find table by ID."""
        pass
    
    @abstractmethod
    async def find_by_entity_name(self, entity_name: EntityName) -> Optional[DPLTable]:
        """Find table by entity name."""
        pass
    
    @abstractmethod
    async def find_by_layer(self, layer: DPLLayer) -> List[DPLTable]:
        """Find all tables in a specific layer."""
        pass
    
    @abstractmethod
    async def find_by_pipeline_type(self, pipeline_type: PipelineType) -> List[DPLTable]:
        """Find all tables by pipeline type."""
        pass
    
    @abstractmethod
    async def find_all_active(self) -> List[DPLTable]:
        """Find all active tables."""
        pass
    
    @abstractmethod
    async def save(self, table: DPLTable) -> DPLTable:
        """Save or update table."""
        pass
    
    @abstractmethod
    async def delete(self, table_id: UUID) -> bool:
        """Delete table by ID."""
        pass


class DPLPipelineRepository(ABC):
    """
    Port for DPL pipeline data access.
    
    Infrastructure layer will implement this interface
    to provide actual pipeline data operations.
    """
    
    @abstractmethod
    async def find_by_id(self, pipeline_id: UUID) -> Optional[DPLPipeline]:
        """Find pipeline by ID."""
        pass
    
    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[DPLPipeline]:
        """Find pipeline by name."""
        pass
    
    @abstractmethod
    async def find_by_status(self, status: PipelineStatus) -> List[DPLPipeline]:
        """Find all pipelines with specific status."""
        pass
    
    @abstractmethod
    async def find_by_entity(self, entity_name: EntityName) -> List[DPLPipeline]:
        """Find all pipelines for an entity."""
        pass
    
    @abstractmethod
    async def find_running(self) -> List[DPLPipeline]:
        """Find all currently running pipelines."""
        pass
    
    @abstractmethod
    async def find_failed(self) -> List[DPLPipeline]:
        """Find all failed pipelines."""
        pass
    
    @abstractmethod
    async def find_requiring_attention(self) -> List[DPLPipeline]:
        """Find all pipelines requiring attention."""
        pass
    
    @abstractmethod
    async def save(self, pipeline: DPLPipeline) -> DPLPipeline:
        """Save or update pipeline."""
        pass
    
    @abstractmethod
    async def delete(self, pipeline_id: UUID) -> bool:
        """Delete pipeline by ID."""
        pass


class DPLWorkflowRepository(ABC):
    """
    Port for DPL workflow data access.
    
    Infrastructure layer will implement this interface
    to provide actual workflow data operations.
    """
    
    @abstractmethod
    async def find_by_id(self, workflow_id: UUID) -> Optional[DPLWorkflow]:
        """Find workflow by ID."""
        pass
    
    @abstractmethod
    async def find_by_databricks_id(self, workflow_id: str) -> Optional[DPLWorkflow]:
        """Find workflow by Databricks workflow ID."""
        pass
    
    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[DPLWorkflow]:
        """Find workflow by name."""
        pass
    
    @abstractmethod
    async def find_by_environment(self, environment: Environment) -> List[DPLWorkflow]:
        """Find all workflows in specific environment."""
        pass
    
    @abstractmethod
    async def find_by_status(self, status: PipelineStatus) -> List[DPLWorkflow]:
        """Find all workflows with specific status."""
        pass
    
    @abstractmethod
    async def find_streaming_workflows(self) -> List[DPLWorkflow]:
        """Find all streaming workflows."""
        pass
    
    @abstractmethod
    async def find_batch_workflows(self) -> List[DPLWorkflow]:
        """Find all batch workflows."""
        pass
    
    @abstractmethod
    async def find_unhealthy(self) -> List[DPLWorkflow]:
        """Find all unhealthy workflows."""
        pass
    
    @abstractmethod
    async def save(self, workflow: DPLWorkflow) -> DPLWorkflow:
        """Save or update workflow."""
        pass
    
    @abstractmethod
    async def delete(self, workflow_id: UUID) -> bool:
        """Delete workflow by ID."""
        pass


class DPLErrorRepository(ABC):
    """
    Port for DPL error data access.
    
    Infrastructure layer will implement this interface
    to provide actual error data operations.
    """
    
    @abstractmethod
    async def find_by_id(self, error_id: UUID) -> Optional[DPLError]:
        """Find error by ID."""
        pass
    
    @abstractmethod
    async def find_by_pipeline(self, pipeline_name: str) -> List[DPLError]:
        """Find all errors for a pipeline."""
        pass
    
    @abstractmethod
    async def find_by_workflow(self, workflow_name: str) -> List[DPLError]:
        """Find all errors for a workflow."""
        pass
    
    @abstractmethod
    async def find_unresolved(self) -> List[DPLError]:
        """Find all unresolved errors."""
        pass
    
    @abstractmethod
    async def find_critical(self) -> List[DPLError]:
        """Find all critical errors."""
        pass
    
    @abstractmethod
    async def find_requiring_immediate_action(self) -> List[DPLError]:
        """Find all errors requiring immediate action."""
        pass
    
    @abstractmethod
    async def find_recurring(self) -> List[DPLError]:
        """Find all recurring errors."""
        pass
    
    @abstractmethod
    async def find_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[DPLError]:
        """Find errors within date range."""
        pass
    
    @abstractmethod
    async def save(self, error: DPLError) -> DPLError:
        """Save or update error."""
        pass
    
    @abstractmethod
    async def delete(self, error_id: UUID) -> bool:
        """Delete error by ID."""
        pass


# ============================================================================
# EXTERNAL SERVICE PORTS
# ============================================================================

class DatabricksServicePort(ABC):
    """
    Port for Databricks API operations.
    
    Infrastructure layer will implement this interface
    to provide actual Databricks API integration.
    """
    
    @abstractmethod
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow status from Databricks."""
        pass
    
    @abstractmethod
    async def list_workflows(self, environment: Environment) -> List[Dict[str, Any]]:
        """List all workflows in environment."""
        pass
    
    @abstractmethod
    async def trigger_workflow(self, workflow_id: str, parameters: Optional[Dict] = None) -> str:
        """Trigger workflow execution and return run ID."""
        pass
    
    @abstractmethod
    async def get_run_status(self, run_id: str) -> Dict[str, Any]:
        """Get run status."""
        pass
    
    @abstractmethod
    async def cancel_run(self, run_id: str) -> bool:
        """Cancel a running workflow."""
        pass
    
    @abstractmethod
    async def get_run_logs(self, run_id: str) -> str:
        """Get logs for a run."""
        pass
    
    @abstractmethod
    async def list_tables(self, catalog: str, schema: str) -> List[Dict[str, Any]]:
        """List tables in catalog.schema."""
        pass
    
    @abstractmethod
    async def get_table_details(self, full_table_name: str) -> Dict[str, Any]:
        """Get detailed table information."""
        pass
    
    @abstractmethod
    async def query_table(self, sql: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results."""
        pass


class VectorStorePort(ABC):
    """
    Port for vector store operations (RAG system).
    
    Infrastructure layer will implement this interface
    to provide actual vector store integration (Chroma, Qdrant, etc).
    """
    
    @abstractmethod
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        pass
    
    @abstractmethod
    async def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """Add documents to vector store and return IDs."""
        pass
    
    @abstractmethod
    async def update_document(self, document_id: str, content: str) -> bool:
        """Update document content."""
        pass
    
    @abstractmethod
    async def delete_document(self, document_id: str) -> bool:
        """Delete document from vector store."""
        pass
    
    @abstractmethod
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get vector store collection statistics."""
        pass


class LLMServicePort(ABC):
    """
    Port for LLM operations.
    
    Infrastructure layer will implement this interface
    to provide actual LLM integration (Anthropic, OpenAI, etc).
    """
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate text response."""
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ):
        """Generate streaming text response."""
        pass
    
    @abstractmethod
    async def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        temperature: float = 0.1
    ) -> Dict[str, Any]:
        """Generate response with tool calling."""
        pass
    
    @abstractmethod
    async def create_embedding(self, text: str) -> List[float]:
        """Create text embedding."""
        pass


class NotificationServicePort(ABC):
    """
    Port for notification operations.
    
    Infrastructure layer will implement this interface
    to provide actual notification integration (Slack, Email, etc).
    """
    
    @abstractmethod
    async def send_alert(
        self,
        message: str,
        severity: str,
        channels: Optional[List[str]] = None
    ) -> bool:
        """Send alert notification."""
        pass
    
    @abstractmethod
    async def send_workflow_status(
        self,
        workflow_name: str,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send workflow status notification."""
        pass
    
    @abstractmethod
    async def send_error_notification(
        self,
        error: DPLError,
        channels: Optional[List[str]] = None
    ) -> bool:
        """Send error notification."""
        pass


# ============================================================================
# UNIT OF WORK PORT
# ============================================================================

class UnitOfWork(ABC):
    """
    Port for Unit of Work pattern.
    
    Manages transaction boundaries for repository operations.
    """
    
    # Repository properties
    tables: DPLTableRepository
    pipelines: DPLPipelineRepository
    workflows: DPLWorkflowRepository
    errors: DPLErrorRepository
    
    @abstractmethod
    async def __aenter__(self):
        """Enter context manager."""
        pass
    
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        pass
    
    @abstractmethod
    async def commit(self) -> None:
        """Commit transaction."""
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        """Rollback transaction."""
        pass

