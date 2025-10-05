# Quick Start Guide

Get started with DPL Agent v3.0 in under 5 minutes!

---

## Installation (1 minute)

### Databricks Notebook
```python
# Install the package
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl

# Restart Python kernel
dbutils.library.restartPython()
```

---

## Basic Usage (2 minutes)

### Option 1: Use Specialists Directly (No API Key Needed)

Perfect for offline use or when you don't have API keys configured.

```python
from data_pipeline_agent_lib.specialists import (
troubleshoot_hdl_error,
resolve_hdl_bug,
optimize_hdl_pipeline
)

# Troubleshoot an error
result = troubleshoot_hdl_error(
"Timeout error after 1h30m in dpl-stream-visits pipeline"
)
print(result)

# Get bug resolution steps
result = resolve_hdl_bug(
"SCD2 is_current column has incorrect values"
)
print(result)

# Get performance optimization advice
result = optimize_hdl_pipeline(
"Batch pipeline for tasks entity is taking 2 hours"
)
print(result)
```

### Option 2: Use Full Agent (Requires API Key)

For interactive, context-aware assistance with RAG and LLM.

```python
import os
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph, create_initial_state
from data_pipeline_agent_lib.utils import create_conversation_config

# Set API key (use Databricks secrets in production!)
os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

# Create agent
graph = create_data_pipeline_agent_graph()
config = create_conversation_config("my_session")

# Ask a question
query = "My visits pipeline is timing out. Help me troubleshoot."
state = create_initial_state(query)
result = graph.invoke(state, config)

print(result["final_response"])
```

---

## API Key Setup (Production)

### Using Databricks Secrets (Recommended)
```python
# Retrieve API key from secure secret scope
api_key = dbutils.secrets.get(
scope="hdl-agent-secrets",
key="anthropic-api-key"
)

import os
os.environ["ANTHROPIC_API_KEY"] = api_key
```

---

## Common Use Cases

### Case 1: Diagnose Pipeline Error
```python
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

result = troubleshoot_hdl_error(
"ConnectionRefusedError: MongoDB connection refused"
)
# Returns: Diagnosis, severity, immediate actions, investigation steps
```

### Case 2: Get Performance Advice
```python
from data_pipeline_agent_lib.specialists import optimize_hdl_pipeline

result = optimize_hdl_pipeline(
"hdl-batch-orders pipeline taking 3 hours instead of 30 minutes"
)
# Returns: Optimization recommendations, expected improvement
```

### Case 3: Coordinate Urgent Reprocessing
```python
from data_pipeline_agent_lib.specialists import coordinate_hdl_reprocessing

result = coordinate_hdl_reprocessing(
"URGENT: Need to reprocess TASKS entity for October 4th. "
"Client waiting. Notify KPI team after."
)
# Returns: Step-by-step reprocessing plan, team coordination
```

### Case 4: Validate Data Quality
```python
from data_pipeline_agent_lib.specialists import validate_hdl_data_quality

result = validate_hdl_data_quality(
"Check completeness and consistency for visits entity in silver layer"
)
# Returns: Quality checklist, findings, recommendations
```

### Case 5: Learn DPL Architecture
```python
from data_pipeline_agent_lib.specialists import explain_hdl_component

result = explain_hdl_component("SCD2 merge process")
# Returns: Detailed explanation, related concepts
```

---

## Multi-Turn Conversations

```python
# Turn 1: Ask about bronze layer
state1 = create_initial_state("What is the bronze layer?")
result1 = graph.invoke(state1, config)
print(result1["final_response"])

# Turn 2: Follow-up question (agent remembers context)
state2 = create_initial_state("What about silver layer?")
state2["messages"] = result1["messages"] # Carry conversation
result2 = graph.invoke(state2, config)
print(result2["final_response"])
```

---

## All Available Specialists

| Specialist | Function | API Required? |
|------------|----------|---------------|
| **Troubleshooter** | `troubleshoot_hdl_error()` | No |
| **Bug Resolver** | `resolve_hdl_bug()` | No |
| **Performance Advisor** | `optimize_hdl_pipeline()` | No |
| **Quality Assistant** | `validate_hdl_data_quality()` | No |
| **DPL Commander** | `execute_hdl_workflow()` | No |
| **Ecosystem Assistant** | `explain_hdl_component()` | No |
| **DPL Coordinator** | `coordinate_hdl_reprocessing()` | No |

**Note:** All specialists work without API keys! The full agent (with LLM) requires `ANTHROPIC_API_KEY`.

---

## Verify Installation

```python
# Check if package is installed
try:
import data_pipeline_agent_lib
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

print(" DPL Agent installed successfully!")

# Quick test
result = troubleshoot_hdl_error("Test error")
print(" Specialists working!")

except ImportError as e:
print(f" Installation issue: {e}")
```

---

## Need Help?

### Common Issues

**Import Error:**
```python
# Restart Python kernel
dbutils.library.restartPython()
```

**API Key Error:**
```python
# Verify API key is set
import os
print("API Key set:", "ANTHROPIC_API_KEY" in os.environ)
```

### Documentation
- Full deployment guide: `docs/deployment/production-deployment.md`
- Architecture: `docs/architecture/clean-architecture.md`
- Specialists overview: `docs/specialists/overview.md`

---

## You're Ready!

Start using the DPL Agent to:
- Troubleshoot pipeline errors
- Get performance optimization advice
- Validate data quality
- Coordinate reprocessing
- Learn DPL architecture

**Next Steps:**
- Explore specialist tools
- Try the full agent with your queries
- Read the architecture documentation
- Review real-world examples

---

**Quick Start Complete!** 
**Version:** 3.0.0 
**Status:** Production Ready

