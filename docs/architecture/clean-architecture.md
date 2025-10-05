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
