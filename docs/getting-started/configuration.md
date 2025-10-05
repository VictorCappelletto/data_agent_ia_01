# Guia de Configuração

Configure o DPL Agent para diferentes ambientes e casos de uso.

---

## Variáveis de Ambiente

### Requerido para Agent Completo

```bash
# Chave API Anthropic (para LLM)
ANTHROPIC_API_KEY=sk-ant-api03-...

# Chave API OpenAI (para embeddings)
OPENAI_API_KEY=sk-...
```

### Configuração Opcional

```bash
# Ambiente (DEV, UAT, PRD)
ENVIRONMENT=PRD

# Diretório de persistência ChromaDB
CHROMA_PERSIST_DIR=/dbfs/data_pipeline_agent/chroma_db

# Nível de logging
LOG_LEVEL=INFO

# Máximo de iterações para workflow do agent
MAX_AGENT_ITERATIONS=10

# Configuração do LLM
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=4096

# Configuração do Vector Store
VECTOR_STORE_COLLECTION=hdl_knowledge
EMBEDDING_MODEL=text-embedding-3-small
TOP_K_RETRIEVAL=5
```

---

## Métodos de Configuração

### 1. Arquivo de Ambiente (.env)

**Desenvolvimento Local:**

Criar arquivo `.env` na raiz do projeto:

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
ENVIRONMENT=DEV
LOG_LEVEL=DEBUG
```

**Carregar no código:**

```python
from dotenv import load_dotenv
load_dotenv()
```

### 2. Secrets do Databricks

**Configurar Secrets:**

```bash
# Criar secret scope
databricks secrets create-scope --scope ai-agents

# Adicionar secrets
databricks secrets put --scope ai-agents --key anthropic-api-key
databricks secrets put --scope ai-agents --key openai-api-key
```

**Usar no Notebook:**

```python
import os

os.environ["ANTHROPIC_API_KEY"] = dbutils.secrets.get("ai-agents", "anthropic-api-key")
os.environ["OPENAI_API_KEY"] = dbutils.secrets.get("ai-agents", "openai-api-key")
```

### 3. Configuração Direta

```python
import os

# Definir diretamente no código (NÃO recomendado para produção)
os.environ["ANTHROPIC_API_KEY"] = "sua-chave-aqui"
os.environ["OPENAI_API_KEY"] = "sua-chave-aqui"
```

---

## Configuração do Agent

### Agent Simples (Padrão)

```python
from data_pipeline_agent_lib.agent import create_simple_hdl_graph

# Configuração padrão
agent = create_simple_hdl_graph()
```

### Configuração Customizada do Agent

```python
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph
from data_pipeline_agent_lib.infrastructure.vector_store import create_chroma_store
from data_pipeline_agent_lib.utils.checkpointer import CheckpointerFactory

# Vector store customizado
vector_store = create_chroma_store(
    persist_directory="/dbfs/data_pipeline_agent/chroma",
    collection_name="hdl_production"
)

# Checkpointer customizado
checkpointer = CheckpointerFactory.create_sqlite_checkpointer(
    db_path="/dbfs/data_pipeline_agent/checkpoints.db"
)

# Criar agent com configuração customizada
agent = create_data_pipeline_agent_graph(
    vector_store=vector_store,
    checkpointer=checkpointer,
    enable_debug=False
)
```

---

## Configuração do Provedor LLM

### Anthropic (Padrão)

```python
from data_pipeline_agent_lib.infrastructure.llm import create_anthropic_provider

llm = create_anthropic_provider(
    model="claude-3-5-sonnet-20241022",
    temperature=0.1,
    max_tokens=4096
)
```

### Prompts de Sistema Customizados

```python
from data_pipeline_agent_lib.infrastructure.llm import get_system_prompt

# Obter prompt específico para intent
troubleshooting_prompt = get_system_prompt("troubleshooting")
architecture_prompt = get_system_prompt("architecture")
```

---

## Configuração do Vector Store

### Configuração do ChromaDB

```python
from data_pipeline_agent_lib.infrastructure.vector_store import create_chroma_store

vector_store = create_chroma_store(
    persist_directory="./data/chroma_db",
    collection_name="hdl_knowledge",
    embedding_model="text-embedding-3-small"
)
```

### Carregamento de Conhecimento

```python
from data_pipeline_agent_lib.infrastructure.vector_store import create_knowledge_indexer

# Indexar base de conhecimento
indexer = create_knowledge_indexer(
    knowledge_path="/dbfs/hdl_knowledge/",
    vector_store=vector_store
)

result = await indexer.index_knowledge_base(clear_existing=True)
print(f"Indexados {result['chunks_indexed']} chunks de {result['documents_loaded']} documentos")
```

---

## Configuração de Especialistas

### Obter Ferramentas por Intent

```python
from data_pipeline_agent_lib.specialists import get_tools_for_intent

# Obter ferramentas de troubleshooting
troubleshooting_tools = get_tools_for_intent("troubleshooting")
# Retorna: [troubleshoot_hdl_error, analyze_pipeline_health, resolve_hdl_bug]

# Obter ferramentas de otimização
optimization_tools = get_tools_for_intent("optimization")
# Retorna: [optimize_hdl_pipeline, validate_hdl_data_quality]
```

### Seleção Customizada de Ferramentas

```python
from data_pipeline_agent_lib.specialists import (
    troubleshoot_hdl_error,
    coordinate_hdl_reprocessing,
)

# Usar apenas ferramentas específicas
my_tools = [troubleshoot_hdl_error, coordinate_hdl_reprocessing]
```

---

## Configuração do Checkpointer

### Memory Checkpointer (Desenvolvimento)

```python
from data_pipeline_agent_lib.utils.checkpointer import CheckpointerFactory

checkpointer = CheckpointerFactory.create_memory_checkpointer()
```

**Bom para:**
- Desenvolvimento e testes
- Sessões temporárias
- Cenários de usuário único

**Limitações:**
- Dados perdidos quando o processo termina
- Não adequado para produção

### SQLite Checkpointer (Produção)

```python
checkpointer = CheckpointerFactory.create_sqlite_checkpointer(
    db_path="/dbfs/data_pipeline_agent/checkpoints.db"
)
```

**Bom para:**
- Desenvolvimento local com persistência
- Deployments de instância única
- Testes com retenção de dados

**Limitações:**
- Processo único (sem concorrência)
- Não adequado para sistemas distribuídos

---

## Configuração Específica do Databricks

### Configuração do Cluster

**Runtime Recomendado:**
- Databricks Runtime 13.3 LTS ou superior
- Python 3.9+
- Spark 3.4+

**Bibliotecas Necessárias:**
- hdl-agent-lib-3.0.0-py3-none-any.whl
- Dependências auto-instaladas

### Configuração de Secrets

```python
# Configurar secrets
import os

# Chaves API
os.environ["ANTHROPIC_API_KEY"] = dbutils.secrets.get("ai-agents", "anthropic-api-key")
os.environ["OPENAI_API_KEY"] = dbutils.secrets.get("ai-agents", "openai-api-key")

# Configuração do Databricks (se necessário)
os.environ["DATABRICKS_HOST"] = dbutils.secrets.get("ai-agents", "databricks-host")
os.environ["DATABRICKS_TOKEN"] = dbutils.secrets.get("ai-agents", "databricks-token")
```

### Caminhos DBFS

```python
# Localização da base de conhecimento
KNOWLEDGE_PATH = "/dbfs/data_pipeline_agent/knowledge/"

# Persistência do ChromaDB
CHROMA_PATH = "/dbfs/data_pipeline_agent/chroma_db/"

# Checkpoints
CHECKPOINT_PATH = "/dbfs/data_pipeline_agent/checkpoints.db"
```

---

## Validação de Configuração

### Verificar Configuração

```python
import os

print("Status da Configuração:")
print(f"✓ ANTHROPIC_API_KEY: {'Configurada' if os.getenv('ANTHROPIC_API_KEY') else '✗ Faltando'}")
print(f"✓ OPENAI_API_KEY: {'Configurada' if os.getenv('OPENAI_API_KEY') else '✗ Faltando'}")
print(f"✓ ENVIRONMENT: {os.getenv('ENVIRONMENT', 'Não configurado (padrão PRD)')}")
```

### Testar Configuração

```python
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

# Testar especialista (funciona sem chaves API)
try:
    result = await troubleshoot_hdl_error.ainvoke({
        "error_message": "teste",
        "entity_name": "visits"
    })
    print("✓ Especialistas funcionando")
except Exception as e:
    print(f"✗ Erro: {e}")

# Testar LLM (requer chave API)
if os.getenv("ANTHROPIC_API_KEY"):
    try:
        from data_pipeline_agent_lib.infrastructure.llm import create_anthropic_provider
        llm = create_anthropic_provider()
        print("✓ Provedor LLM funcionando")
    except Exception as e:
        print(f"✗ Erro LLM: {e}")
else:
    print("✗ ANTHROPIC_API_KEY não configurada - recursos LLM indisponíveis")
```

---

## Solução de Problemas de Configuração

### Problemas Comuns

**Problema**: `ModuleNotFoundError: No module named 'langchain'` 
**Solução**: Reiniciar cluster após instalação da biblioteca

**Problema**: `ANTHROPIC_API_KEY not found` 
**Solução**: Configurar secrets do Databricks ou arquivo .env

**Problema**: `ChromaDB persistence error` 
**Solução**: Garantir que o caminho DBFS existe e tem permissões de escrita

---

## Melhores Práticas

### Desenvolvimento

```python
# Usar arquivo .env
# Usar memory checkpointer
# Habilitar logging de debug
# Usar base de conhecimento pequena
```

### Produção

```python
# Usar Databricks Secrets para chaves API
# Usar SQLite checkpointer
# Usar DBFS para persistência
# Monitorar uso de recursos
```

---

## Próximos Passos

- Configurar seu ambiente
- Testar com especialistas
- Carregar base de conhecimento
- Experimentar agent completo
- Deploy para produção

Para mais detalhes, veja:
- [Guia de Instalação](installation.md)
- [Visão Geral da Arquitetura](../architecture/clean-architecture.md)
- [Exemplos](../examples/basic.md)
