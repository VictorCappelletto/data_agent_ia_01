# Agent Architecture & Flow

This page provides visual diagrams explaining how the DPL Agent works internally.

---

## High-Level Architecture

```mermaid
graph LR
    A[User Query] --> B[Agent Core]
    B --> C[7 Specialists]
    B <--> D[Knowledge Base<br/>66 files]
    C --> E[Response]
    
    style B fill:#1565c0,stroke:#333,stroke-width:2px,color:#000
    style D fill:#00acc1,stroke:#333,stroke-width:2px,color:#000
```

**Components:**
- **Agent Core**: LangGraph orchestration + RAG system
- **7 Specialists**: Troubleshooter, Bug Resolver, Performance, Quality, Commander, Ecosystem, Coordinator
- **Knowledge Base**: 66 markdown files with DPL documentation

---

## Agent Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant KB as Knowledge Base
    participant Specialist
    
    User->>Agent: "Why is visits pipeline timing out?"
    Agent->>KB: Search relevant docs
    KB-->>Agent: DPL documentation
    Agent->>Specialist: Execute troubleshooter
    Specialist-->>Agent: Diagnosis + steps
    Agent-->>User: Professional response
```

**Steps:**
1. User asks question
2. Agent searches knowledge base for context
3. Agent selects and executes appropriate specialist
4. Specialist provides diagnosis with sources
5. Agent returns formatted response

---

## RAG System (Knowledge Retrieval)

```mermaid
graph TD
    A[Specialist needs context] --> B[RAG Service]
    B --> C[Search Knowledge Base]
    C --> D{Found?}
    D -->|Yes| E[Return context + sources]
    D -->|No| F[Use fallback patterns]
    E --> G[Enhanced response]
    F --> G
    
    style B fill:#00acc1,stroke:#333,stroke-width:2px
```

**How it works:**
- Specialists query the RAG service for relevant documentation
- RAG searches 66 markdown files using semantic search
- Returns context with sources if found
- Falls back to hardcoded patterns if not found

---

## Clean Architecture Layers

```mermaid
graph BT
    A[Domain Layer<br/>Entities & Business Rules] 
    B[Application Layer<br/>Agent & Specialists]
    C[Infrastructure Layer<br/>Databricks & Vector Store]
    
    C --> B --> A
    
    style A fill:#e91e63,stroke:#333,stroke-width:2px
    style B fill:#1565c0,stroke:#333,stroke-width:2px
```

**Layers (Inner to Outer):**
1. **Domain**: Core business logic (DPL entities, workflows)
2. **Application**: Agent orchestration, specialists, RAG
3. **Infrastructure**: External systems (Databricks, Claude, ChromaDB)

**Rule**: Dependencies flow inward only (outer layers depend on inner)

---

## Specialist Execution Process

```mermaid
graph LR
    A[Receive Query] --> B[Search Knowledge Base]
    B --> C[Execute Logic]
    C --> D[Format Response]
    D --> E[Return Result]
    
    style B fill:#00acc1,stroke:#333,stroke-width:2px
```

**Process:**
1. **Receive Query**: Get user question
2. **Search KB**: Find relevant documentation (RAG)
3. **Execute Logic**: Apply specialist expertise
4. **Format**: Professional, structured output
5. **Return**: Back to agent core

---

## Agent Workflow States

```mermaid
graph LR
    A[Analyze Intent] --> B[Select Tools]
    B --> C[Execute Specialists]
    C --> D[Generate Response]
    
    style B fill:#1565c0,stroke:#333,stroke-width:2px
    style C fill:#e91e63,stroke:#333,stroke-width:2px
```

**States:**
- **Analyze**: Understand user's goal (troubleshooting? optimization?)
- **Select**: Choose appropriate specialists
- **Execute**: Run selected specialists in parallel if needed
- **Generate**: Create final formatted response

---

## Tool Selection by Intent

```mermaid
graph TD
    A[User Query] --> B{What's the intent?}
    B -->|Error/Issue| C[Troubleshooter]
    B -->|Performance| D[Performance Advisor]
    B -->|Data Quality| E[Quality Assistant]
    B -->|Execute/Monitor| F[DPL Commander]
    B -->|Learn| G[Ecosystem Assistant]
```

**Intent Categories:**
- **Error/Issue**: Uses Troubleshooter + Bug Resolver
- **Performance**: Uses Performance Advisor
- **Data Quality**: Uses Quality Assistant
- **Execute/Monitor**: Uses DPL Commander
- **Learn/Explain**: Uses Ecosystem Assistant

---

## Conversation Memory

```mermaid
graph LR
    A[User Query 1] --> B[Agent Response 1]
    B --> C[Stored in Memory]
    C --> D[User Query 2]
    D --> E[Agent uses context]
    E --> F[Response 2]
    
    style C fill:#00acc1,stroke:#333,stroke-width:2px
```

**How Memory Works:**
- Each conversation has a `session_id`
- Agent stores all interactions in SQLite
- Follow-up questions use previous context
- Enables multi-turn conversations

---

## 7 Specialists Summary

```mermaid
graph TB
    A[DPL Agent] --> B[Troubleshooter<br/>Error diagnosis]
    A --> C[Bug Resolver<br/>Fix solutions]
    A --> D[Performance Advisor<br/>Optimization]
    A --> E[Quality Assistant<br/>Data validation]
    A --> F[DPL Commander<br/>Workflow execution]
    A --> G[Ecosystem Assistant<br/>Documentation]
    A --> H[DPL Coordinator<br/>Reprocessing]
    
    style B fill:#f44336,stroke:#333,stroke-width:2px
    style D fill:#1565c0,stroke:#333,stroke-width:2px
    style E fill:#4caf50,stroke:#333,stroke-width:2px
```

**All 7 Specialists:**
1. **Troubleshooter**: Diagnose errors and issues
2. **Bug Resolver**: Provide step-by-step fixes
3. **Performance Advisor**: Optimize pipeline performance
4. **Quality Assistant**: Validate data quality
5. **DPL Commander**: Execute and monitor workflows
6. **Ecosystem Assistant**: Explain DPL components
7. **DPL Coordinator**: Coordinate reprocessing scenarios

---

## Databricks Deployment

```mermaid
graph LR
    A[.whl Package] --> B[Databricks Cluster]
    B --> C[DPL Agent Running]
    C --> D[Claude via<br/>Serving Endpoints]
    C --> E[DPL Workflows]
    
    style C fill:#1565c0,stroke:#333,stroke-width:2px
```

**Deployment Steps:**
1. Build `.whl` package (data_pipeline_agent_lib-3.1.0)
2. Upload to Databricks cluster
3. Import and use in notebooks
4. Agent uses Databricks Claude endpoints
5. Interacts with DPL workflows

**No External API Keys Required** - Uses Databricks native services

---

## Error Handling & Fallback

```mermaid
graph TD
    A[Specialist Executes] --> B{RAG Found Docs?}
    B -->|Yes| C[Use KB Context]
    B -->|No| D[Use Fallback Patterns]
    C --> E[Return Enhanced Result]
    D --> E
    
    style C fill:#4caf50,stroke:#333,stroke-width:2px
    style D fill:#f44336,stroke:#333,stroke-width:2px
```

**Graceful Degradation:**
- Agent always tries RAG first for specific knowledge
- If RAG fails, uses hardcoded fallback patterns
- System never fails completely
- All specialists have fallback logic

---

## Key Architecture Principles

**1. Clean Architecture** - Dependencies flow inward, domain protected

**2. RAG-First** - Always try knowledge base, fallback if needed

**3. Graceful Degradation** - System works even if components fail

**4. Professional Output** - No emojis, structured, actionable

**5. Testability** - 136 tests passing (100% core coverage)

---

## Next Steps

- **[Specialists Overview](../specialists/overview.md)** - All 7 specialists detailed
- **[Examples](../examples/basic.md)** - Practical code examples
- **[Clean Architecture](clean-architecture.md)** - Layer responsibilities
- **[Deployment Guide](../deployment/quickstart.md)** - Deploy to Databricks

