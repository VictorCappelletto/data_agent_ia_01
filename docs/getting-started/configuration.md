# Configuration Guide

Configure DPL Agent for different environments and use cases.

---

## Environment Variables

### Required for Full Agent

```bash
# Anthropic API Key (for LLM)
ANTHROPIC_API_KEY=sk-ant-api03-...

# OpenAI API Key (for embeddings)
OPENAI_API_KEY=sk-...
```

### Optional Configuration

```bash
# Environment (DEV, UAT, PRD)
ENVIRONMENT=PRD

# ChromaDB persistence directory
CHROMA_PERSIST_DIR=/dbfs/data_pipeline_agent/chroma_db

# Logging level
LOG_LEVEL=INFO

# Max iterations for agent workflow
MAX_AGENT_ITERATIONS=10

# LLM Configuration
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=4096

# Vector Store Configuration
VECTOR_STORE_COLLECTION=hdl_knowledge
EMBEDDING_MODEL=text-embedding-3-small
TOP_K_RETRIEVAL=5
```

---

## Configuration Methods

### 1. Environment File (.env)

**Local Development:**

Create `.env` file in project root:

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
ENVIRONMENT=DEV
LOG_LEVEL=DEBUG
```

**Load in code:**

```python
from dotenv import load_dotenv
load_dotenv()
```

### 2. Databricks Secrets

**Setup Secrets:**

```bash
# Create secret scope
databricks secrets create-scope --scope ai-agents

# Add secrets
databricks secrets put --scope ai-agents --key anthropic-api-key
databricks secrets put --scope ai-agents --key openai-api-key
```

**Use in Notebook:**

```python
import os

os.environ["ANTHROPIC_API_KEY"] = dbutils.secrets.get("ai-agents", "anthropic-api-key")
os.environ["OPENAI_API_KEY"] = dbutils.secrets.get("ai-agents", "openai-api-key")
```

### 3. Direct Configuration

```python
import os

# Set directly in code (NOT recommended for production)
os.environ["ANTHROPIC_API_KEY"] = "your-key-here"
os.environ["OPENAI_API_KEY"] = "your-key-here"
```

---

## Agent Configuration

### Simple Agent (Default)

```python
from data_pipeline_agent_lib.agent import create_simple_hdl_graph

# Default configuration
agent = create_simple_hdl_graph()
```

### Custom Agent Configuration

```python
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph
from data_pipeline_agent_lib.infrastructure.vector_store import create_chroma_store
from data_pipeline_agent_lib.utils.checkpointer import CheckpointerFactory

# Custom vector store
vector_store = create_chroma_store(
persist_directory="/dbfs/data_pipeline_agent/chroma",
collection_name="hdl_production"
)

# Custom checkpointer
checkpointer = CheckpointerFactory.create_sqlite_checkpointer(
db_path="/dbfs/data_pipeline_agent/checkpoints.db"
)

# Create agent with custom config
agent = create_data_pipeline_agent_graph(
vector_store=vector_store,
checkpointer=checkpointer,
enable_debug=False
)
```

---

## LLM Provider Configuration

### Anthropic (Default)

```python
from data_pipeline_agent_lib.infrastructure.llm import create_anthropic_provider

llm = create_anthropic_provider(
model="claude-3-5-sonnet-20241022",
temperature=0.1,
max_tokens=4096
)
```

### Custom System Prompts

```python
from data_pipeline_agent_lib.infrastructure.llm import get_system_prompt

# Get intent-specific prompt
troubleshooting_prompt = get_system_prompt("troubleshooting")
architecture_prompt = get_system_prompt("architecture")
```

---

## Vector Store Configuration

### ChromaDB Configuration

```python
from data_pipeline_agent_lib.infrastructure.vector_store import create_chroma_store

vector_store = create_chroma_store(
persist_directory="./data/chroma_db",
collection_name="hdl_knowledge",
embedding_model="text-embedding-3-small"
)
```

### Knowledge Loading

```python
from data_pipeline_agent_lib.infrastructure.vector_store import create_knowledge_indexer

# Index knowledge base
indexer = create_knowledge_indexer(
knowledge_path="/dbfs/hdl_knowledge/",
vector_store=vector_store
)

result = await indexer.index_knowledge_base(clear_existing=True)
print(f"Indexed {result['chunks_indexed']} chunks from {result['documents_loaded']} documents")
```

---

## Specialist Configuration

### Get Tools by Intent

```python
from data_pipeline_agent_lib.specialists import get_tools_for_intent

# Get troubleshooting tools
troubleshooting_tools = get_tools_for_intent("troubleshooting")
# Returns: [troubleshoot_hdl_error, analyze_pipeline_health, resolve_hdl_bug]

# Get optimization tools
optimization_tools = get_tools_for_intent("optimization")
# Returns: [optimize_hdl_pipeline, validate_hdl_data_quality]
```

### Custom Tool Selection

```python
from data_pipeline_agent_lib.specialists import (
troubleshoot_hdl_error,
coordinate_hdl_reprocessing,
)

# Use only specific tools
my_tools = [troubleshoot_hdl_error, coordinate_hdl_reprocessing]
```

---

## Checkpointer Configuration

### Memory Checkpointer (Development)

```python
from data_pipeline_agent_lib.utils.checkpointer import CheckpointerFactory

checkpointer = CheckpointerFactory.create_memory_checkpointer()
```

**Good for:**
- Development and testing
- Temporary sessions
- Single-user scenarios

**Limitations:**
- Data lost when process ends
- Not suitable for production

### SQLite Checkpointer (Production)

```python
checkpointer = CheckpointerFactory.create_sqlite_checkpointer(
db_path="/dbfs/data_pipeline_agent/checkpoints.db"
)
```

**Good for:**
- Local development with persistence
- Single-instance deployments
- Testing with data retention

**Limitations:**
- Single-process (no concurrency)
- Not suitable for distributed systems

---

## Databricks-Specific Configuration

### Cluster Configuration

**Recommended Runtime:**
- Databricks Runtime 13.3 LTS or higher
- Python 3.9+
- Spark 3.4+

**Required Libraries:**
- hdl-agent-lib-3.0.0-py3-none-any.whl
- Dependencies auto-installed

### Secrets Configuration

```python
# Configure secrets
import os

# API Keys
os.environ["ANTHROPIC_API_KEY"] = dbutils.secrets.get("ai-agents", "anthropic-api-key")
os.environ["OPENAI_API_KEY"] = dbutils.secrets.get("ai-agents", "openai-api-key")

# Databricks Configuration (if needed)
os.environ["DATABRICKS_HOST"] = dbutils.secrets.get("ai-agents", "databricks-host")
os.environ["DATABRICKS_TOKEN"] = dbutils.secrets.get("ai-agents", "databricks-token")
```

### DBFS Paths

```python
# Knowledge base location
KNOWLEDGE_PATH = "/dbfs/data_pipeline_agent/knowledge/"

# ChromaDB persistence
CHROMA_PATH = "/dbfs/data_pipeline_agent/chroma_db/"

# Checkpoints
CHECKPOINT_PATH = "/dbfs/data_pipeline_agent/checkpoints.db"
```

---

## Configuration Validation

### Check Configuration

```python
import os

print("Configuration Status:")
print(f" ANTHROPIC_API_KEY: {' Set' if os.getenv('ANTHROPIC_API_KEY') else ' Missing'}")
print(f" OPENAI_API_KEY: {' Set' if os.getenv('OPENAI_API_KEY') else ' Missing'}")
print(f" ENVIRONMENT: {os.getenv('ENVIRONMENT', 'Not set (defaults to PRD)')}")
```

### Test Configuration

```python
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

# Test specialist (works without API keys)
try:
result = await troubleshoot_hdl_error.ainvoke({
"error_message": "test",
"entity_name": "visits"
})
print(" Specialists working")
except Exception as e:
print(f" Error: {e}")

# Test LLM (requires API key)
if os.getenv("ANTHROPIC_API_KEY"):
try:
from data_pipeline_agent_lib.infrastructure.llm import create_anthropic_provider
llm = create_anthropic_provider()
print(" LLM provider working")
except Exception as e:
print(f" LLM Error: {e}")
else:
print(" ANTHROPIC_API_KEY not set - LLM features unavailable")
```

---

## Troubleshooting Configuration

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'langchain'` 
**Solution**: Restart cluster after library installation

**Issue**: `ANTHROPIC_API_KEY not found` 
**Solution**: Configure Databricks secrets or .env file

**Issue**: `ChromaDB persistence error` 
**Solution**: Ensure DBFS path exists and has write permissions

---

## Best Practices

### Development

```python
# Use .env file
# Use memory checkpointer
# Enable debug logging
# Use small knowledge base
```

### Production

```python
# Use Databricks Secrets for API keys
# Use SQLite checkpointer
# Use DBFS for persistence
# Monitor resource usage
```

---

## Next Steps

- Configure your environment
- Test with specialists
- Load knowledge base
- Try complete agent
- Deploy to production

For more details, see:
- [Installation Guide](installation.md)
- [Architecture Overview](../architecture/clean-architecture.md)
- [Examples](../examples/basic.md)

