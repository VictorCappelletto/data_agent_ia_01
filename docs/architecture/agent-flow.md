# Arquitetura & Fluxo do Agent

Esta página fornece diagramas visuais explicando como o DPL Agent funciona internamente.

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
    participant Usuário
    participant Agent
    participant BC as Base de Conhecimento
    participant Especialista
    
    Usuário->>Agent: "Por que o pipeline visits está expirando?"
    Agent->>BC: Buscar docs relevantes
    BC-->>Agent: Documentação DPL
    Agent->>Especialista: Executar troubleshooter
    Especialista-->>Agent: Diagnóstico + etapas
    Agent-->>Usuário: Resposta profissional
```

**Etapas:**
1. Usuário faz pergunta
2. Agent busca base de conhecimento por contexto
3. Agent seleciona e executa especialista apropriado
4. Especialista fornece diagnóstico com fontes
5. Agent retorna resposta formatada

---

## Sistema RAG (Recuperação de Conhecimento)

```mermaid
graph TD
    A[Especialista precisa de contexto] --> B[Serviço RAG]
    B --> C[Buscar Base de Conhecimento]
    C --> D{Encontrou?}
    D -->|Sim| E[Retornar contexto + fontes]
    D -->|Não| F[Usar padrões fallback]
    E --> G[Resposta aprimorada]
    F --> G
    
    style B fill:#00acc1,stroke:#333,stroke-width:2px
```

**Como funciona:**
- Especialistas consultam o serviço RAG para documentação relevante
- RAG busca 66 arquivos markdown usando busca semântica
- Retorna contexto com fontes se encontrado
- Volta para padrões hardcoded se não encontrado

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
