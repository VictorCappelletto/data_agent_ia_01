# DPL Agent v3.1

Agent AI pronto para produção para troubleshooting, monitoramento e otimização de pipelines DPL (Data Pipeline Layer) no Databricks.

---

## Visão Geral

DPL Agent é um assistente AI especializado construído com LangChain e LangGraph que automatiza operações de pipeline DPL através de sete ferramentas especialistas com recuperação de conhecimento via RAG.

### Capacidades Principais

- **Diagnóstico de Erros**: Troubleshooting automatizado para falhas de pipeline
- **Resolução de Bugs**: Soluções conhecidas e orientação de resolução
- **Otimização de Performance**: Recomendações acionáveis para pipelines lentos
- **Qualidade de Dados**: Validação abrangente em dimensões de qualidade
- **Gerenciamento de Workflow**: Coordenação de execução e monitoramento
- **Base de Conhecimento**: Arquitetura DPL e melhores práticas
- **Coordenação de Reprocessamento**: Workflows de recuperação de dados com notificação de equipe

---

## Arquitetura

### Implementação de Arquitetura Limpa
- **Camada de Domínio**: Lógica de negócio e entidades principais
- **Camada de Aplicação**: Casos de uso e orquestração (7 especialistas)
- **Camada de Infraestrutura**: LLM, vector store e integrações externas

### Sistema RAG (Retrieval-Augmented Generation)

O DPL Agent utiliza **RAG** para fornecer respostas fundamentadas em documentação real, não em conhecimento genérico do LLM.

**Como Funciona:**

1. **Retrieval**: Busca documentos relevantes usando embeddings vetoriais (Sentence Transformers)
2. **Augmentation**: Injeta contexto recuperado no prompt do LLM
3. **Generation**: LLM gera resposta baseada na documentação DPL específica

**Benefícios:**

- ✅ Respostas específicas do DPL (não genéricas)
- ✅ Fundamentadas em documentação real com citações
- ✅ Reduz "alucinações" do LLM
- ✅ Conhecimento atualizado sem retreinar modelo

**Stack Técnico:**

- **Base de Conhecimento**: 66 arquivos markdown (41 core + 25 workflows)
- **Vector Store**: ChromaDB para busca semântica
- **Embeddings**: Sentence Transformers `all-MiniLM-L6-v2` (384D)
- **Similaridade**: Cosine similarity para ranking de relevância
- **Integração**: ✅ Todos os 7 especialistas usam RAG automaticamente

📖 **[Explicação Técnica Completa do RAG](architecture/rag-explained.md)**

### Orquestração LangGraph
- **Workflows com estado** para interações multi-turno
- **Roteamento inteligente** baseado na intenção da consulta
- **Chamada de ferramentas** com seleção de especialista
- **Memória de conversa** para preservação de contexto

---

## Sete Ferramentas Especialistas

1. **Troubleshooter** - Diagnóstico de erro e análise de saúde de pipeline
2. **Bug Resolver** - Soluções de bugs conhecidos e etapas de resolução
3. **Performance Advisor** - Estratégias de otimização e recomendações
4. **Quality Assistant** - Validação de qualidade de dados
5. **DPL Commander** - Execução e monitoramento de workflow
6. **Ecosystem Assistant** - Documentação de componentes e melhores práticas
7. **DPL Coordinator** - Coordenação de reprocessamento e notificação de equipe

---

## Início Rápido

### Instalação
```python
# Databricks
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
dbutils.library.restartPython()
```

### Uso Básico
```python
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

# Diagnosticar erro de pipeline
result = troubleshoot_hdl_error(
    "Erro de timeout em dpl-stream-visits após 1h30m"
)
print(result)
```

**Guia Completo**: [Início Rápido](deployment/quickstart.md)

---

## Métricas de Qualidade

- **136 testes unitários** (100% passando)
- **40 testes E2E** (100% passando)
- **51% cobertura de código** (91% para especialistas)
- **Saída profissional** (sem emoji, logging estruturado)
- **Integração RAG** (todos os 7 especialistas)

---

## Documentação

### Primeiros Passos
- [Instalação](getting-started/installation.md) - Configuração para Databricks e local
- [Início Rápido](getting-started/quickstart.md) - Comece em 5 minutos
- [Configuração](getting-started/configuration.md) - Chaves API e configuração de ambiente

### Deploy
- [Deploy Rápido](deployment/quickstart.md) - Guia de deploy rápido
- [Deploy em Produção](deployment/production-deployment.md) - Workflow completo

### Referência
- [Arquitetura](architecture/clean-architecture.md) - Princípios de design
- [Especialistas](specialists/overview.md) - Documentação de ferramentas
- [Referência da API](api/specialists.md) - Docs detalhados da API
- [Exemplos](examples/basic.md) - Exemplos de código
- [Resultados de Testes](testing/test-results.md) - Cobertura e qualidade

---

## Informações do Pacote

- **Versão**: 3.1.0
- **Tamanho**: 162 KB
- **Formato**: Python Wheel (.whl)
- **Python**: >=3.9
- **Conhecimento**: 66 arquivos (41 core + 25 workflows)
- **Dependências**: LangChain, LangGraph, ChromaDB, Databricks SDK

---

## Suporte

- **Líder Técnico**: Victor Cappelletto
- **Projeto**: Operations Strategy - DPL Operations
- **Documentação**: [Site MkDocs](https://victorcappelletto.github.io/data_agent_ia_01/)

---

**Última Atualização**: 2025-10-05  
**Status**: Pronto para Produção (v3.1.0 - RAG Completo)
