# Arquitetura Limpa

Implementação do DPL Agent dos princípios de Clean Architecture para manutenibilidade e escalabilidade.

---

## Princípios Fundamentais

### Separação de Responsabilidades
Cada camada tem uma responsabilidade específica sem interferência de outras.

### Regra de Dependência
Dependências apontam apenas para dentro. Camadas internas não têm conhecimento das camadas externas.

```
Infraestrutura → Aplicação → Domínio
```

### Testabilidade
Lógica de negócio isolada da infraestrutura permite testes unitários diretos.

### Independência de Tecnologia
Lógica de domínio permanece independente de frameworks, bancos de dados e serviços externos.

---

## Arquitetura de Três Camadas

### Camada de Domínio (Core)

**Localização**: `data_pipeline_agent_lib/domain/`

**Contém**:
- Entidades: `DPLTable`, `DPLPipeline`, `DPLWorkflow`, `DPLError`
- Objetos de Valor: `Environment`, `PipelineType`, `ErrorSeverity`
- Portas: Interfaces de repositório
- Serviços de Domínio: Regras de negócio

**Restrições**:
- Sem dependências externas
- Python puro + Pydantic
- Sem imports de framework
- Sem chamadas de banco de dados/API

**Exemplo**:
```python
from data_pipeline_agent_lib.domain import DPLPipeline, PipelineType, Environment

pipeline = DPLPipeline(
    pipeline_name="dpl-stream-visits",
    pipeline_type=PipelineType.STREAMING,
    environment=Environment.PRD
)
```

### Camada de Aplicação

**Localização**: `data_pipeline_agent_lib/agent/`, `data_pipeline_agent_lib/specialists/`

**Contém**:
- Orquestração do agent (workflows LangGraph)
- Sete ferramentas especialistas
- Gerenciamento de estado (`AgentState`)
- Nós de processamento

**Dependências**:
- Usa camada de Domínio
- Usa Infraestrutura via interfaces
- Frameworks LangChain/LangGraph

**Exemplo**:
```python
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

agent = create_data_pipeline_agent_graph()
result = troubleshoot_hdl_error("erro de timeout")
```

### Camada de Infraestrutura

**Localização**: `data_pipeline_agent_lib/infrastructure/`

**Contém**:
- Integração LLM (Anthropic, OpenAI)
- Vector store (ChromaDB)
- Embeddings (SentenceTransformers)
- Adaptadores de serviços externos

**Dependências**:
- Implementa portas do Domínio
- Bibliotecas externas (langchain, chromadb, anthropic)
- Sem lógica de negócio

**Exemplo**:
```python
from data_pipeline_agent_lib.infrastructure.llm import create_anthropic_provider
from data_pipeline_agent_lib.infrastructure.vector_store import create_chroma_store

llm = create_anthropic_provider()
vector_store = create_chroma_store()
```

---

## Inversão de Dependência

Camada de domínio define requisitos via **Portas** (interfaces). Infraestrutura fornece **implementações concretas**.

### Porta (Interface)

```python
# domain/ports/hdl_repository_port.py
from abc import ABC, abstractmethod

class VectorStorePort(ABC):
    @abstractmethod
    def retrieve_documents(self, query: str, k: int) -> List[str]:
        pass
```

### Adaptador (Implementação)

```python
# infrastructure/vector_store/chroma_store.py
from data_pipeline_agent_lib.domain.ports import VectorStorePort

class ChromaVectorStore(VectorStorePort):
    def retrieve_documents(self, query: str, k: int) -> List[str]:
        results = self.collection.query(query_texts=[query], n_results=k)
        return results["documents"][0]
```

---

## Dependency Injection (Injeção de Dependências)

O DPL Agent implementa Dependency Injection para garantir baixo acoplamento e alta testabilidade.

### Princípios Implementados

1. **Constructor Injection**: Dependências são injetadas via construtor
2. **Interface-based**: Classes dependem de abstrações (Ports), não de implementações concretas
3. **Factory Pattern**: Funções factory compõem o grafo de dependências
4. **Type Hints**: Tipos explícitos para validação em tempo de compilação

### Implementação no RAG System

#### Camada de Domínio: Define a Interface

```python
# domain/ports/hdl_repository_port.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class VectorStorePort(ABC):
    """Port (interface) for vector store operations."""
    
    @abstractmethod
    async def search(
        self, 
        query: str, 
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        pass
```

#### Camada de Infraestrutura: Implementa a Interface

```python
# infrastructure/vector_store/chroma_store.py
from ...domain.ports import VectorStorePort

class ChromaVectorStore(VectorStorePort):
    """ChromaDB implementation of VectorStorePort."""
    
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        # Implementation using ChromaDB
        results = self._vectorstore.similarity_search(query, k=top_k)
        return [{"content": doc.page_content, "metadata": doc.metadata} 
                for doc in results]
```

#### Infraestrutura: Recebe Dependência Injetada

```python
# infrastructure/vector_store/dpl_retriever.py
from ...domain.ports import VectorStorePort

class DPLRetriever:
    """DPL-specific retriever with dependency injection."""
    
    def __init__(self, vector_store: VectorStorePort):
        """
        Initialize with injected vector store.
        
        Args:
            vector_store: VectorStorePort implementation (injected)
        """
        self.vector_store: VectorStorePort = vector_store
```

#### Camada de Aplicação: Usa via Factory

```python
# application/services/dpl_retriever_service.py
from ...infrastructure.vector_store import DPLRetriever

class DPLRetrieverService:
    """Application service with dependency injection."""
    
    def __init__(self, retriever: DPLRetriever):
        """
        Initialize with injected retriever.
        
        Args:
            retriever: DPLRetriever instance (injected)
        """
        self.retriever: DPLRetriever = retriever
```

#### Composition Root: Factory Compõe Dependências

```python
# infrastructure/vector_store/dpl_retriever.py
def get_hdl_retriever() -> DPLRetriever:
    """
    Factory function that composes the dependency graph.
    
    Creates the full stack:
    1. ChromaVectorStore (implements VectorStorePort)
    2. Injects into DPLRetriever via constructor
    3. Returns configured retriever
    """
    from .chroma_store import create_chroma_store
    
    # Create infrastructure implementation
    vector_store: VectorStorePort = create_chroma_store()
    
    # Inject dependency via constructor
    retriever = DPLRetriever(vector_store)
    
    return retriever
```

### Benefícios do Dependency Injection

#### 1. Testabilidade

```python
# Em testes, injete mocks:
def test_retriever_with_mock():
    mock_store = MockVectorStore()
    retriever = DPLRetriever(mock_store)  # Injeta mock
    
    result = retriever.search("query")
    assert mock_store.search_called  # Verifica comportamento
```

#### 2. Flexibilidade

```python
# Fácil trocar implementações:
# Produção: ChromaDB
vector_store = ChromaVectorStore()

# Desenvolvimento: In-memory
vector_store = InMemoryVectorStore()

# Ambos implementam VectorStorePort
retriever = DPLRetriever(vector_store)
```

#### 3. Configuração Dinâmica

```python
# Escolher implementação via configuração:
if config.vector_store == "chroma":
    store = ChromaVectorStore()
elif config.vector_store == "pinecone":
    store = PineconeVectorStore()
    
retriever = DPLRetriever(store)
```

### Validação de Arquitetura

O projeto inclui testes automatizados para garantir conformidade:

```python
# tests/unit/test_architecture.py
def test_dpl_retriever_uses_port():
    """Valida que DPLRetriever depende de VectorStorePort."""
    from dpl_agent_lib.infrastructure.vector_store import DPLRetriever
    from dpl_agent_lib.domain.ports import VectorStorePort
    
    init_signature = inspect.signature(DPLRetriever.__init__)
    vector_store_param = init_signature.parameters.get('vector_store')
    
    assert vector_store_param.annotation == VectorStorePort
```

Execute os testes:

```bash
pytest tests/unit/test_architecture.py -v
```

### Fluxo de Dependências no RAG

```
┌─────────────────────────────────────────────────────────────────┐
│ Application Layer (Specialists)                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ DPLRetrieverService                                         │ │
│ │   receives: DPLRetriever (injected)                         │ │
│ └─────────────────────┬───────────────────────────────────────┘ │
└───────────────────────┼─────────────────────────────────────────┘
                        │ depends on
┌───────────────────────┼─────────────────────────────────────────┐
│ Infrastructure Layer  ▼                                          │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ DPLRetriever                                                │ │
│ │   receives: VectorStorePort (injected)                      │ │
│ └─────────────────────┬───────────────────────────────────────┘ │
│                       │ depends on (interface)                  │
│ ┌─────────────────────┼───────────────────────────────────────┐ │
│ │ ChromaVectorStore   ▼                                       │ │
│ │   implements: VectorStorePort                               │ │
│ └─────────────────────┬───────────────────────────────────────┘ │
└───────────────────────┼─────────────────────────────────────────┘
                        │ implements
┌───────────────────────┼─────────────────────────────────────────┐
│ Domain Layer          ▼                                          │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ VectorStorePort (Interface/Port)                            │ │
│ │   defines: abstract methods                                 │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

Dependency Rule: All arrows point INWARD (to Domain)
```

---

## Benefícios

### Testes Fáceis

```python
def test_hdl_pipeline_validation():
    pipeline = DPLPipeline(
        pipeline_name="test",
        pipeline_type=PipelineType.BATCH,
        environment=Environment.UAT
    )
    assert pipeline.is_batch_pipeline() == True
```

### Infraestrutura Flexível

```python
# Trocar implementações sem mudar código da aplicação
vector_store = ChromaVectorStore(...)  # ou QdrantVectorStore(...)
agent = create_data_pipeline_agent_graph(vector_store=vector_store)
```

### Limites Claros

- Mudanças no domínio não afetam infraestrutura
- Mudanças na infraestrutura não afetam domínio
- Aplicação orquestra ambas as camadas

---

## Padrões de Design

### Padrão Repository
Abstrair acesso a dados via portas/interfaces.

### Padrão Factory
Criar objetos complexos (agents, vector stores).

### Padrão Strategy
Algoritmos intercambiáveis (provedores LLM, retrievers).

### Injeção de Dependência
Passar dependências explicitamente, não hardcoded.

---

## Princípios SOLID

- **S**ingle Responsibility: Cada classe tem uma razão para mudar
- **O**pen/Closed: Aberto para extensão, fechado para modificação
- **L**iskov Substitution: Implementações substituem interfaces perfeitamente
- **I**nterface Segregation: Interfaces pequenas e focadas
- **D**ependency Inversion: Depender de abstrações, não concreções

---

## Exemplo do Mundo Real

```python
# Domínio: Definir entidade
class DPLError:
    error_message: str
    severity: ErrorSeverity
    entity_name: str

# Aplicação: Caso de uso
def troubleshoot_hdl_error(input_data: dict) -> str:
    error = DPLError(**input_data)
    docs = vector_store.retrieve_documents(
        query=error.error_message,
        filters={"entity": error.entity_name}
    )
    diagnosis = analyze_error_pattern(error, docs)
    return diagnosis

# Infraestrutura: Implementação concreta
vector_store = ChromaVectorStore(...)
```

**Benefícios**:
- Lógica de domínio pura (`DPLError`, `analyze_error_pattern`)
- Infraestrutura intercambiável (`ChromaVectorStore`)
- Orquestração limpa na camada de aplicação

---

## Próximos Passos

- [Visão Geral dos Especialistas](../specialists/overview.md)
- [Guia de Início Rápido](../getting-started/quickstart.md)
- [Referência da API](../api/specialists.md)

---

**Última Atualização**: 2025-10-04
