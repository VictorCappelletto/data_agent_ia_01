# Arquitetura & Fluxo do Agent

Esta página fornece diagramas visuais explicando como o DPL Agent funciona internamente.

---

## O Que é LangGraph?

**LangGraph** é um framework da LangChain para construir **aplicações multi-agent com estado** usando grafos direcionados.

### Conceito Core

LangGraph modela aplicações AI como um **grafo de estados** onde:
- **Nós** são funções que processam o estado (ex: especialistas, LLM calls)
- **Arestas** definem transições entre nós (ex: roteamento, condicionais)
- **Estado** é compartilhado e modificado ao longo do fluxo

### Por Que Usar LangGraph vs LangChain Puro?

| LangChain (Chains) | LangGraph (Graphs) |
|--------------------|-------------------|
| Fluxo linear sequencial | Fluxo com ciclos e condicionais |
| Difícil adicionar loops | Loops nativos (ex: retry, refinement) |
| Estado implícito | Estado explícito e controlado |
| Hard-coded routing | Dynamic routing baseado em estado |

### Como Funciona no DPL Agent

```python
# Definição simplificada do grafo
from langgraph.graph import StateGraph

# 1. Definir o estado compartilhado
class AgentState(TypedDict):
    messages: List[Message]
    specialist: str
    context: str

# 2. Criar grafo com nós (funções)
workflow = StateGraph(AgentState)
workflow.add_node("router", route_to_specialist)
workflow.add_node("troubleshooter", troubleshoot_specialist)
workflow.add_node("performance", performance_specialist)

# 3. Definir transições (arestas)
workflow.add_conditional_edges(
    "router",
    lambda state: state["specialist"],  # Decisão dinâmica
    {
        "troubleshooter": "troubleshooter",
        "performance": "performance"
    }
)

# 4. Compilar grafo
agent = workflow.compile()
```

### Benefícios para o DPL Agent

1. **Roteamento Dinâmico**: Seleciona especialista baseado na intenção do usuário
2. **Conversas Multi-turno**: Mantém contexto entre interações
3. **Retry e Validação**: Pode refazer passos se resposta inadequada
4. **Debugging**: Estado explícito facilita rastreamento

### Alternativas Consideradas

- **LangChain LCEL**: Bom para pipelines simples, limitado para decisões complexas
- **Custom Orchestration**: Mais flexível mas requer implementar gerenciamento de estado
- **AutoGPT/BabyAGI**: Muito autônomo, difícil de controlar

**Escolha:** LangGraph oferece o melhor equilíbrio entre flexibilidade e controle.

### Visualização do Grafo DPL Agent

```mermaid
graph TD
    START([Início]) --> ROUTER[Router Node<br/>Classifica Intenção]
    
    ROUTER -->|troubleshoot| TROUBLE[Troubleshooter<br/>Diagnóstico]
    ROUTER -->|performance| PERF[Performance Advisor<br/>Otimização]
    ROUTER -->|quality| QUAL[Quality Assistant<br/>Validação]
    ROUTER -->|workflow| CMD[DPL Commander<br/>Execução]
    ROUTER -->|bug| BUG[Bug Resolver<br/>Correção]
    ROUTER -->|docs| ECO[Ecosystem Assistant<br/>Documentação]
    ROUTER -->|reprocess| COORD[DPL Coordinator<br/>Coordenação]
    
    TROUBLE --> RESPOND[Response Node<br/>Formatar Resposta]
    PERF --> RESPOND
    QUAL --> RESPOND
    CMD --> RESPOND
    BUG --> RESPOND
    ECO --> RESPOND
    COORD --> RESPOND
    
    RESPOND --> END([Fim])
    
    style ROUTER fill:#ff9800,stroke:#333,stroke-width:2px,color:#000
    style RESPOND fill:#4caf50,stroke:#333,stroke-width:2px,color:#000
    style TROUBLE fill:#2196f3,stroke:#333,stroke-width:2px,color:#fff
    style PERF fill:#2196f3,stroke:#333,stroke-width:2px,color:#fff
    style QUAL fill:#2196f3,stroke:#333,stroke-width:2px,color:#fff
    style CMD fill:#2196f3,stroke:#333,stroke-width:2px,color:#fff
    style BUG fill:#2196f3,stroke:#333,stroke-width:2px,color:#fff
    style ECO fill:#2196f3,stroke:#333,stroke-width:2px,color:#fff
    style COORD fill:#2196f3,stroke:#333,stroke-width:2px,color:#fff
```

**Componentes do Grafo:**
- **START**: Recebe consulta do usuário
- **ROUTER**: Nó decisor que classifica intenção (conditional edge)
- **Especialistas (7 nós)**: Cada um processa tipos específicos de consultas
- **RESPOND**: Formata resposta final
- **END**: Retorna para o usuário

**Estado compartilhado entre nós:**
```python
{
    "messages": [...],           # Histórico da conversa
    "specialist": "troubleshoot", # Especialista selecionado
    "context": "...",            # Contexto RAG recuperado
    "pipeline_info": {...}       # Metadados do pipeline
}
```

---

## Arquitetura de Alto Nível

```mermaid
graph LR
    A[Consulta do Usuário] --> B[Núcleo do Agent]
    B --> C[7 Especialistas]
    B <--> D[Base de Conhecimento<br/>66 arquivos]
    C --> E[Resposta]
    
    style B fill:#1565c0,stroke:#333,stroke-width:2px,color:#000
    style D fill:#00acc1,stroke:#333,stroke-width:2px,color:#000
```

**Componentes:**
- **Núcleo do Agent**: Orquestração LangGraph + sistema RAG
- **7 Especialistas**: Troubleshooter, Bug Resolver, Performance, Quality, Commander, Ecosystem, Coordinator
- **Base de Conhecimento**: 66 arquivos markdown com documentação DPL

---

## Fluxo de Execução do Agent

```mermaid
sequenceDiagram
    participant U as Usuário
    participant A as Agent (LangGraph)
    participant S as Especialista
    participant R as DPLRetrieverService
    participant V as ChromaDB
    participant L as LLM (Claude)
    
    U->>A: "Pipeline visits expirando"
    
    Note over A: 1. ROTEAMENTO
    A->>A: Análise de intenção<br/>(LLM classifica)
    A->>S: Chamar Troubleshooter
    
    Note over S,V: 2. RETRIEVAL
    S->>R: search_error_patterns(<br/>"visits expirando")
    R->>R: Construir query otimizada
    R->>V: similarity_search(<br/>query_vector, k=5)
    V-->>R: Top-5 docs + scores
    R->>R: enhance_context()
    R-->>S: Contexto formatado
    
    Note over S,L: 3. GENERATION
    S->>S: Construir prompt:<br/>contexto + query
    S->>L: generate(prompt)
    L-->>S: Diagnóstico fundamentado
    
    S-->>A: Resultado + fontes
    A-->>U: Resposta formatada
```

**Etapas Detalhadas:**

1. **Roteamento**: Agent classifica intenção e seleciona especialista apropriado
2. **Retrieval**: Especialista busca documentação relevante via RAG (embeddings + similaridade)
3. **Generation**: LLM gera resposta baseada no contexto recuperado
4. **Resposta**: Inclui diagnóstico + citações das fontes consultadas

**Pontos Importantes:**

- **LLM usado 2x**: No Agent (classificação) e no Especialista (geração)
- **RAG no Especialista**: Cada especialista chama `DPLRetrieverService` automaticamente
- **Contexto flui**: ChromaDB → Retriever → Especialista → LLM → Usuário

---

## Sistema RAG (Retrieval-Augmented Generation)

### Arquitetura Completa em 3 Fases

```mermaid
graph TB
    subgraph "FASE 1: INDEXAÇÃO (Offline - Setup)"
        A[Documentos .md<br/>66 arquivos] --> B[Chunking<br/>Dividir em blocos]
        B --> C[Embedding Model<br/>all-MiniLM-L6-v2]
        C --> D[Vetores 384D<br/>representação numérica]
        D --> E[(ChromaDB<br/>Vector Store)]
    end
    
    subgraph "FASE 2: RETRIEVAL (Runtime - Busca)"
        F[Query do Usuário<br/>texto] --> G[Embedding Model<br/>mesma transformação]
        G --> H[Query Vector 384D]
        H --> I[Cosine Similarity<br/>Top-K Search]
        E --> I
        I --> J[Top-5 Documentos<br/>mais relevantes + scores]
    end
    
    subgraph "FASE 3: GENERATION (Runtime - Resposta)"
        J --> K[Context Injection<br/>formatar para prompt]
        K --> L[LLM Claude<br/>gerar resposta]
        L --> M[Resposta Final<br/>com citações das fontes]
    end
    
    style E fill:#00acc1,stroke:#333,stroke-width:2px,color:#fff
    style L fill:#1565c0,stroke:#333,stroke-width:2px,color:#fff
    style I fill:#ff9800,stroke:#333,stroke-width:2px,color:#000
```

### Componentes Técnicos Explicados

**1. Embedding Model (Sentence Transformers)**
- Converte texto em vetores numéricos de 384 dimensões
- Textos semanticamente similares → vetores próximos no espaço vetorial
- Modelo: `all-MiniLM-L6-v2` (rápido, leve, 80MB)

**2. Vector Database (ChromaDB)**
- Armazena embeddings dos 66 documentos da base de conhecimento
- Busca eficiente usando índices aproximados (HNSW algorithm)
- Persiste em disco para reuso entre execuções

**3. Similarity Search (Cosine)**
- Calcula similaridade entre query vector e document vectors
- Métrica: Cosine Similarity (0 = totalmente diferente, 1 = idêntico)
- Retorna Top-K documentos mais similares (default K=5)

**4. Context Injection**
- Formata documentos recuperados em texto estruturado
- Injeta no prompt do LLM com instruções específicas
- Garante resposta fundamentada em documentação real

**5. LLM Generation (Claude)**
- Recebe: contexto recuperado + query original + instruções
- Gera: resposta baseada APENAS no contexto fornecido
- Inclui: citações das fontes consultadas

---

## Camadas de Arquitetura Limpa

```mermaid
graph BT
    A[Camada de Domínio<br/>Entidades & Regras de Negócio] 
    B[Camada de Aplicação<br/>Agent & Especialistas]
    C[Camada de Infraestrutura<br/>Databricks & Vector Store]
    
    C --> B --> A
    
    style A fill:#e91e63,stroke:#333,stroke-width:2px
    style B fill:#1565c0,stroke:#333,stroke-width:2px
```

**Camadas (Interna para Externa):**
1. **Domínio**: Lógica de negócio central (entidades DPL, workflows)
2. **Aplicação**: Orquestração do agent, especialistas, RAG
3. **Infraestrutura**: Sistemas externos (Databricks, Claude, ChromaDB)

**Regra**: Dependências fluem apenas para dentro (camadas externas dependem das internas)

---

## Processo de Execução do Especialista

```mermaid
graph LR
    A[Receber Consulta] --> B[Buscar Base de Conhecimento]
    B --> C[Executar Lógica]
    C --> D[Formatar Resposta]
    D --> E[Retornar Resultado]
    
    style B fill:#00acc1,stroke:#333,stroke-width:2px
```

**Processo:**
1. **Receber Consulta**: Obter pergunta do usuário
2. **Buscar BC**: Encontrar documentação relevante (RAG)
3. **Executar Lógica**: Aplicar expertise do especialista
4. **Formatar**: Saída profissional e estruturada
5. **Retornar**: De volta ao núcleo do agent

---

## Estados do Workflow do Agent

```mermaid
graph LR
    A[Analisar Intenção] --> B[Selecionar Ferramentas]
    B --> C[Executar Especialistas]
    C --> D[Gerar Resposta]
    
    style B fill:#1565c0,stroke:#333,stroke-width:2px
    style C fill:#e91e63,stroke:#333,stroke-width:2px
```

**Estados:**
- **Analisar**: Entender objetivo do usuário (troubleshooting? otimização?)
- **Selecionar**: Escolher especialistas apropriados
- **Executar**: Executar especialistas selecionados em paralelo se necessário
- **Gerar**: Criar resposta final formatada

---

## Seleção de Ferramenta por Intenção

```mermaid
graph TD
    A[Consulta do Usuário] --> B{Qual é a intenção?}
    B -->|Erro/Problema| C[Troubleshooter]
    B -->|Performance| D[Performance Advisor]
    B -->|Qualidade de Dados| E[Quality Assistant]
    B -->|Executar/Monitorar| F[DPL Commander]
    B -->|Aprender| G[Ecosystem Assistant]
```

**Categorias de Intenção:**
- **Erro/Problema**: Usa Troubleshooter + Bug Resolver
- **Performance**: Usa Performance Advisor
- **Qualidade de Dados**: Usa Quality Assistant
- **Executar/Monitorar**: Usa DPL Commander
- **Aprender/Explicar**: Usa Ecosystem Assistant

---

## Memória de Conversa

```mermaid
graph LR
    A[Consulta do Usuário 1] --> B[Resposta do Agent 1]
    B --> C[Armazenado na Memória]
    C --> D[Consulta do Usuário 2]
    D --> E[Agent usa contexto]
    E --> F[Resposta 2]
    
    style C fill:#00acc1,stroke:#333,stroke-width:2px
```

**Como a Memória Funciona:**
- Cada conversa tem um `session_id`
- Agent armazena todas as interações no SQLite
- Perguntas de acompanhamento usam contexto anterior
- Permite conversas multi-turno

---

## Resumo dos 7 Especialistas

```mermaid
graph TB
    A[DPL Agent] --> B[Troubleshooter<br/>Diagnóstico de erros]
    A --> C[Bug Resolver<br/>Soluções de correção]
    A --> D[Performance Advisor<br/>Otimização]
    A --> E[Quality Assistant<br/>Validação de dados]
    A --> F[DPL Commander<br/>Execução de workflow]
    A --> G[Ecosystem Assistant<br/>Documentação]
    A --> H[DPL Coordinator<br/>Reprocessamento]
    
    style B fill:#f44336,stroke:#333,stroke-width:2px
    style D fill:#1565c0,stroke:#333,stroke-width:2px
    style E fill:#4caf50,stroke:#333,stroke-width:2px
```

**Todos os 7 Especialistas:**
1. **Troubleshooter**: Diagnosticar erros e problemas
2. **Bug Resolver**: Fornecer correções passo a passo
3. **Performance Advisor**: Otimizar performance de pipeline
4. **Quality Assistant**: Validar qualidade de dados
5. **DPL Commander**: Executar e monitorar workflows
6. **Ecosystem Assistant**: Explicar componentes DPL
7. **DPL Coordinator**: Coordenar cenários de reprocessamento

---

## Deploy no Databricks

```mermaid
graph LR
    A[Pacote .whl] --> B[Cluster Databricks]
    B --> C[DPL Agent Executando]
    C --> D[Claude via<br/>Serving Endpoints]
    C --> E[Workflows DPL]
    
    style C fill:#1565c0,stroke:#333,stroke-width:2px
```

**Etapas de Deploy:**
1. Build do pacote `.whl` (data_pipeline_agent_lib-3.1.0)
2. Upload para cluster Databricks
3. Import e uso em notebooks
4. Agent usa endpoints Claude do Databricks
5. Interage com workflows DPL

**Sem Chaves API Externas Necessárias** - Usa serviços nativos do Databricks

---

## Tratamento de Erros & Fallback

```mermaid
graph TD
    A[Especialista Executa] --> B{RAG Encontrou Docs?}
    B -->|Sim| C[Usar Contexto BC]
    B -->|Não| D[Usar Padrões Fallback]
    C --> E[Retornar Resultado Aprimorado]
    D --> E
    
    style C fill:#4caf50,stroke:#333,stroke-width:2px
    style D fill:#f44336,stroke:#333,stroke-width:2px
```

**Degradação Graciosa:**
- Agent sempre tenta RAG primeiro para conhecimento específico
- Se RAG falha, usa padrões fallback hardcoded
- Sistema nunca falha completamente
- Todos os especialistas têm lógica fallback

---

## Princípios Chave da Arquitetura

**1. Arquitetura Limpa** - Dependências fluem para dentro, domínio protegido

**2. RAG-First** - Sempre tenta base de conhecimento, fallback se necessário

**3. Degradação Graciosa** - Sistema funciona mesmo se componentes falharem

**4. Saída Profissional** - Sem emojis, estruturada, acionável

**5. Testabilidade** - 136 testes passando (100% cobertura core)

---

## Próximos Passos

- **[Visão Geral dos Especialistas](../specialists/overview.md)** - Todos os 7 especialistas detalhados
- **[Exemplos](../examples/basic.md)** - Exemplos práticos de código
- **[Arquitetura Limpa](clean-architecture.md)** - Responsabilidades das camadas
- **[Guia de Deploy](../deployment/quickstart.md)** - Deploy no Databricks
