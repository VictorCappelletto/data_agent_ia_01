# Quick Start

Get started with DPL Agent v3.0 in 5 minutes.

---

## Prerequisites

- Python 3.9+
- Databricks workspace or local Python environment
- Optional: Anthropic API key (for full agent features)

---

## Installation

```python
# Databricks
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
dbutils.library.restartPython()

# Verify
from data_pipeline_agent_lib.specialists import ALL_DPL_TOOLS
print(f"{len(ALL_DPL_TOOLS)} specialist tools available")
```

---

## Basic Usage

### Troubleshoot Pipeline Error

```python
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

result = troubleshoot_hdl_error(
    "Sessions streaming pipeline timed out after 90 minutes"
)

print(result)
```

**Output**:
```
TROUBLESHOOTING ANALYSIS

Diagnosis: Detected timeout error pattern
Severity: HIGH
Confidence: 85%

Root Cause Candidates:
- Large data volume processing
- Cluster resource constraints

Investigation Steps:
1. Check pipeline execution duration
2. Review cluster resource utilization
3. Verify data volume processed
4. Inspect checkpoint location
```

### Optimize Performance

```python
from data_pipeline_agent_lib.specialists import optimize_hdl_pipeline

recommendations = optimize_hdl_pipeline(
    "hdl-batch-tasks running 2 hours instead of usual 30 minutes"
)

print(recommendations)
```

### Validate Data Quality

```python
from data_pipeline_agent_lib.specialists import validate_hdl_data_quality

report = validate_hdl_data_quality(
    "Check completeness and consistency for visits entity"
)

print(report)
```

### Coordinate Reprocessing

```python
from data_pipeline_agent_lib.specialists import coordinate_hdl_reprocessing

plan = coordinate_hdl_reprocessing(
    "TASKS entity for October 4th. Client waiting. Notify KPI team."
)

print(plan)
```

---

## Using the Full Agent

Requires API key configuration.

### Configure API Keys

```python
import os

# Databricks
os.environ["ANTHROPIC_API_KEY"] = dbutils.secrets.get(
    "hdl-agent-secrets", "anthropic-api-key"
)

# Local (use .env file)
from dotenv import load_dotenv
load_dotenv()
```

### Create Agent

```python
from data_pipeline_agent_lib.agent import create_simple_hdl_graph
from data_pipeline_agent_lib.agent.state import create_initial_state

# Initialize agent
agent = create_simple_hdl_graph()

# Ask question
state = create_initial_state(
    query="How do I troubleshoot a timeout in visits streaming pipeline?",
    session_id="session_001"
)

# Get response
result = agent.invoke(state)
print(result["final_response"])
```

### Multi-Turn Conversation

```python
from data_pipeline_agent_lib.utils.checkpointer import create_conversation_config

config = create_conversation_config("thread_001")

# First question
state1 = create_initial_state("What is SCD2?", "thread_001")
result1 = agent.invoke(state1, config=config)

# Follow-up (remembers context)
state2 = create_initial_state("How is it used in DPL?", "thread_001")
result2 = agent.invoke(state2, config=config)
```

---

## Available Specialists

### Troubleshooting
- `troubleshoot_hdl_error` - Error diagnosis
- `analyze_pipeline_health` - Health check
- `resolve_hdl_bug` - Bug resolution

### Optimization
- `optimize_hdl_pipeline` - Performance recommendations
- `validate_hdl_data_quality` - Quality validation

### Operations
- `execute_hdl_workflow` - Workflow execution
- `get_workflow_status` - Monitoring
- `coordinate_hdl_reprocessing` - Reprocessing coordination

### Documentation
- `explain_hdl_component` - Component explanations
- `get_hdl_best_practices` - Best practices

---

## Real-World Examples

### Urgent Pipeline Failure

```python
from data_pipeline_agent_lib.specialists import (
    troubleshoot_hdl_error,
    coordinate_hdl_reprocessing
)

# Diagnose
diagnosis = troubleshoot_hdl_error(
    "URGENT: TASKS batch pipeline timed out. Data not in silver layer."
)

# Get reprocessing plan
plan = coordinate_hdl_reprocessing(
    "TASKS entity for October 4th. Client waiting. Notify KPI team."
)
```

### Performance Investigation

```python
from data_pipeline_agent_lib.specialists import optimize_hdl_pipeline

advice = optimize_hdl_pipeline(
    "hdl-batch-orders taking 2 hours instead of usual 30 minutes"
)
```

### Data Quality Check

```python
from data_pipeline_agent_lib.specialists import validate_hdl_data_quality

report = validate_hdl_data_quality(
    "Check completeness and consistency for visits entity"
)
```

---

## Next Steps

1. [Installation Guide](installation.md) - Detailed setup
2. [Specialists Overview](../specialists/overview.md) - All 7 specialists
3. [Architecture](../architecture/clean-architecture.md) - Design principles
4. [Examples](../examples/basic.md) - More code examples

---

## Support

- **Technical Lead**: Victor Cappelleto
- **Project**: Operations Strategy - DPL Operations

---

**Last Updated**: 2025-10-04
