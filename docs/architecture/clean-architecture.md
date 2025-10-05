# Clean Architecture

DPL Agent implementation of Clean Architecture principles for maintainability and scalability.

---

## Core Principles

### Separation of Concerns
Each layer has a specific responsibility without interference from others.

### Dependency Rule
Dependencies point inward only. Inner layers have no knowledge of outer layers.

```
Infrastructure → Application → Domain
```

### Testability
Business logic isolated from infrastructure enables straightforward unit testing.

### Technology Independence
Domain logic remains independent of frameworks, databases, and external services.

---

## Three-Layer Architecture

### Domain Layer (Core)

**Location**: `data_pipeline_agent_lib/domain/`

**Contains**:
- Entities: `DPLTable`, `DPLPipeline`, `DPLWorkflow`, `DPLError`
- Value Objects: `Environment`, `PipelineType`, `ErrorSeverity`
- Ports: Repository interfaces
- Domain Services: Business rules

**Constraints**:
- No external dependencies
- Pure Python + Pydantic
- No framework imports
- No database/API calls

**Example**:
```python
from data_pipeline_agent_lib.domain import DPLPipeline, PipelineType, Environment

pipeline = DPLPipeline(
    pipeline_name="dpl-stream-visits",
    pipeline_type=PipelineType.STREAMING,
    environment=Environment.PRD
)
```

### Application Layer

**Location**: `data_pipeline_agent_lib/agent/`, `data_pipeline_agent_lib/specialists/`

**Contains**:
- Agent orchestration (LangGraph workflows)
- Seven specialist tools
- State management (`AgentState`)
- Processing nodes

**Dependencies**:
- Uses Domain layer
- Uses Infrastructure via interfaces
- LangChain/LangGraph frameworks

**Example**:
```python
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

agent = create_data_pipeline_agent_graph()
result = troubleshoot_hdl_error("timeout error")
```

### Infrastructure Layer

**Location**: `data_pipeline_agent_lib/infrastructure/`

**Contains**:
- LLM integration (Anthropic, OpenAI)
- Vector store (ChromaDB)
- Embeddings (SentenceTransformers)
- External service adapters

**Dependencies**:
- Implements Domain ports
- External libraries (langchain, chromadb, anthropic)
- No business logic

**Example**:
```python
from data_pipeline_agent_lib.infrastructure.llm import create_anthropic_provider
from data_pipeline_agent_lib.infrastructure.vector_store import create_chroma_store

llm = create_anthropic_provider()
vector_store = create_chroma_store()
```

---

## Dependency Inversion

Domain layer defines requirements via **Ports** (interfaces). Infrastructure provides **concrete implementations**.

### Port (Interface)

```python
# domain/ports/hdl_repository_port.py
from abc import ABC, abstractmethod

class VectorStorePort(ABC):
    @abstractmethod
    def retrieve_documents(self, query: str, k: int) -> List[str]:
        pass
```

### Adapter (Implementation)

```python
# infrastructure/vector_store/chroma_store.py
from data_pipeline_agent_lib.domain.ports import VectorStorePort

class ChromaVectorStore(VectorStorePort):
    def retrieve_documents(self, query: str, k: int) -> List[str]:
        results = self.collection.query(query_texts=[query], n_results=k)
        return results["documents"][0]
```

---

## Benefits

### Easy Testing

```python
def test_hdl_pipeline_validation():
    pipeline = DPLPipeline(
        pipeline_name="test",
        pipeline_type=PipelineType.BATCH,
        environment=Environment.UAT
    )
    assert pipeline.is_batch_pipeline() == True
```

### Flexible Infrastructure

```python
# Swap implementations without changing application code
vector_store = ChromaVectorStore(...)  # or QdrantVectorStore(...)
agent = create_data_pipeline_agent_graph(vector_store=vector_store)
```

### Clear Boundaries

- Domain changes don't affect infrastructure
- Infrastructure changes don't affect domain
- Application orchestrates both layers

---

## Design Patterns

### Repository Pattern
Abstract data access via ports/interfaces.

### Factory Pattern
Create complex objects (agents, vector stores).

### Strategy Pattern
Interchangeable algorithms (LLM providers, retrievers).

### Dependency Injection
Pass dependencies explicitly, not hardcoded.

---

## SOLID Principles

- **S**ingle Responsibility: Each class has one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Implementations replace interfaces seamlessly
- **I**nterface Segregation: Small, focused interfaces
- **D**ependency Inversion: Depend on abstractions, not concretions

---

## Real-World Example

```python
# Domain: Define entity
class DPLError:
    error_message: str
    severity: ErrorSeverity
    entity_name: str

# Application: Use case
def troubleshoot_hdl_error(input_data: dict) -> str:
    error = DPLError(**input_data)
    docs = vector_store.retrieve_documents(
        query=error.error_message,
        filters={"entity": error.entity_name}
    )
    diagnosis = analyze_error_pattern(error, docs)
    return diagnosis

# Infrastructure: Concrete implementation
vector_store = ChromaVectorStore(...)
```

**Benefits**:
- Pure domain logic (`DPLError`, `analyze_error_pattern`)
- Swappable infrastructure (`ChromaVectorStore`)
- Clean orchestration in application layer

---

## Next Steps

- [Specialists Overview](../specialists/overview.md)
- [Quick Start Guide](../getting-started/quickstart.md)
- [API Reference](../api/specialists.md)

---

**Last Updated**: 2025-10-04
