# DPL Agent Examples

Professional examples demonstrating DPL Agent v3.0 capabilities.

---

## Quick Start

### Prerequisites
- Python 3.9+
- DPL Agent installed (`pip install data_pipeline_agent_lib-3.0.0-py3-none-any.whl`)
- Optional: API keys for full agent features

---

## Available Examples

### 1. Basic Usage (`basic_usage.py`)
**Purpose**: Demonstrates all 7 specialist tools with minimal code.  
**Complexity**: Beginner  
**Runtime**: < 1 minute  
**Dependencies**: None (no API key required)

**Usage**:
```bash
python examples/basic_usage.py
```

**What it shows**:
- Troubleshooter: Error diagnosis
- Bug Resolver: Resolution guidance
- Performance Advisor: Optimization recommendations
- Quality Assistant: Data validation
- DPL Commander: Workflow execution
- Ecosystem Assistant: Component documentation
- DPL Coordinator: Reprocessing coordination

---

### 2. Agent Conversation (`agent_conversation.py`)
**Purpose**: Full agent with LangGraph orchestration and memory.  
**Complexity**: Intermediate  
**Runtime**: Varies (depends on LLM)  
**Dependencies**: Anthropic API key required

**Setup**:
```python
# Set API key
export ANTHROPIC_API_KEY="sk-ant-api03-your-key"

# Or in Python
import os
os.environ["ANTHROPIC_API_KEY"] = "your-key"
```

**Usage**:
```bash
python examples/agent_conversation.py
```

**What it shows**:
- Simple queries with agent
- Multi-turn conversations with memory
- Context preservation across turns
- Stateful workflows

---

### 3. Databricks Deployment (`databricks_deployment.py`)
**Purpose**: Production deployment patterns for Databricks.  
**Complexity**: Intermediate  
**Runtime**: Varies  
**Dependencies**: Databricks environment, API key

**Usage**:
```python
# In Databricks notebook
%run examples/databricks_deployment
```

**What it shows**:
- Package installation in Databricks
- API key configuration with secrets
- Specialist usage in notebooks
- Production patterns

---

### 4. RAG System Demo (`rag_demo.py`)
**Purpose**: Demonstrates RAG (Retrieval-Augmented Generation) system.  
**Complexity**: Advanced  
**Runtime**: 2-3 minutes  
**Dependencies**: OpenAI API key (for embeddings)

**Usage**:
```bash
python examples/rag_demo.py
```

**What it shows**:
- Knowledge base indexing
- Semantic search
- Context-aware retrieval
- Filtered queries

---

### 5. Local Chat (`local_chat.py`)
**Purpose**: Interactive chat interface for local development.  
**Complexity**: Beginner  
**Runtime**: Interactive  
**Dependencies**: Anthropic API key

**Usage**:
```bash
python examples/local_chat.py
```

**What it shows**:
- Interactive conversation loop
- Streaming responses
- Chat history
- Exit handling

---

## Running Examples

### Without API Key (Specialists Only)
```bash
# Basic specialist demonstrations
python examples/basic_usage.py
```

### With API Key (Full Agent)
```bash
# Set API key
export ANTHROPIC_API_KEY="sk-ant-api03-your-key"

# Run agent examples
python examples/agent_conversation.py
python examples/local_chat.py
```

### In Databricks
```python
# Install package first
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
dbutils.library.restartPython()

# Run example
%run examples/databricks_deployment
```

---

## Example Outputs

### Basic Usage
```
DPL AGENT V3.0 - BASIC USAGE

1. TROUBLESHOOTER
Query: Pipeline timed out after 90 minutes
Output: TROUBLESHOOTING ANALYSIS
        Diagnosis: timeout pattern detected
        Severity: HIGH
        ...

2. BUG RESOLVER
Query: SCD2 is_current broken after update
Output: BUG RESOLUTION GUIDE
        Known Issue: SCD2 Corruption
        Resolution: Run AdjustIsCurrent.py
        ...
```

### Agent Conversation
```
User: How do I troubleshoot visits streaming timeouts?
Agent: Based on DPL knowledge, here are the steps:
       1. Check checkpoint location...
       2. Verify cluster resources...
       3. Review data volume...

User: What about performance optimization?
Agent: For streaming performance, consider:
       1. Increase cluster size...
       2. Optimize checkpoint intervals...
```

---

## Troubleshooting

### ModuleNotFoundError
```bash
# Ensure package is installed
pip list | grep hdl-agent-lib

# Reinstall if needed
pip install --Platform-reinstall data_pipeline_agent_lib-3.0.0-py3-none-any.whl
```

### API Key Issues
```python
# Verify API key is set
import os
print("API Key set:", "ANTHROPIC_API_KEY" in os.environ)

# Set manually if needed
os.environ["ANTHROPIC_API_KEY"] = "your-key"
```

### Import Errors
```python
# Check Python path
import sys
print(sys.path)

# Add project root if needed
sys.path.insert(0, "/path/to/data_pipeline_agent")
```

---

## Next Steps

1. Start with `basic_usage.py` to understand specialist capabilities
2. Try `agent_conversation.py` for full agent features
3. Review `databricks_deployment.py` for production patterns
4. Explore `rag_demo.py` for knowledge retrieval
5. Use `local_chat.py` for interactive testing

---

## Support

- **Documentation**: [Full Docs](../docs/index.md)
- **Installation**: [Installation Guide](../docs/getting-started/installation.md)
- **Specialists**: [Specialists Overview](../docs/specialists/overview.md)
- **Technical Lead**: Victor Cappelleto

---

**Last Updated**: 2025-10-04

