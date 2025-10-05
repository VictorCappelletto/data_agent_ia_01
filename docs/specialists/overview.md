# DPL Specialists Overview

The DPL Agent includes **7 specialized tools** designed for different DPL operational scenarios.

---

## Why Specialists?

Instead of a monolithic agent trying to do everything, we have **focused specialists** that excel at specific tasks:

- **Better accuracy** - Specialized prompts and logic
- **Easier maintenance** - Update one specialist without affecting others
- **Clear responsibilities** - Each specialist has a defined role
- **Composable** - Use individually or together

---

## All 7 Specialists

### 1. **Troubleshooter**

**Purpose**: Diagnose errors and investigate issues

**Tools** (2):
- `troubleshoot_hdl_error` - Error diagnosis with pattern matching
- `analyze_pipeline_health` - Pipeline health check

**When to use**:
- Pipeline failed or timing out
- Unexpected behavior in streaming/batch
- Need to understand what went wrong

**Example**:
```python
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

result = await troubleshoot_hdl_error.ainvoke({
"error_message": "Pipeline timeout after 90 minutes",
"entity_name": "visits",
"pipeline_type": "streaming"
})
```

---

### 2. **Bug Resolver**

**Purpose**: Provide solutions for known bugs and issues

**Tools** (1):
- `resolve_hdl_bug` - Bug resolution guidance

**When to use**:
- Known bug patterns (SCD2, UUID conversion, etc.)
- Need step-by-step fix instructions
- Looking for tested solutions

**Example**:
```python
from data_pipeline_agent_lib.specialists import resolve_hdl_bug

result = await resolve_hdl_bug.ainvoke({
"bug_description": "SCD2 is_current flags are incorrect",
"entity_name": "visits"
})
```

---

### 3. **Performance Advisor**

**Purpose**: Optimize pipeline performance

**Tools** (1):
- `optimize_hdl_pipeline` - Performance optimization strategies

**When to use**:
- Pipeline running slowly
- Need to improve throughput
- Resource optimization required

**Example**:
```python
from data_pipeline_agent_lib.specialists import optimize_hdl_pipeline

result = await optimize_hdl_pipeline.ainvoke({
"pipeline_name": "hdl-batch-tasks",
"performance_issue": "Processing taking too long"
})
```

---

### 4. **Quality Assistant**

**Purpose**: Validate data quality

**Tools** (1):
- `validate_hdl_data_quality` - Data quality validation

**When to use**:
- Suspect data quality issues
- Need completeness/accuracy checks
- Validating after reprocessing

**Example**:
```python
from data_pipeline_agent_lib.specialists import validate_hdl_data_quality

result = await validate_hdl_data_quality.ainvoke({
"entity_name": "visits",
"quality_dimension": "completeness"
})
```

---

### 5. DPL Commander

**Purpose**: Execute and monitor workflows

**Tools** (2):
- `execute_hdl_workflow` - Workflow execution
- `get_workflow_status` - Workflow monitoring

**When to use**:
- Need to run a workflow
- Check workflow execution status
- Monitor pipeline progress

**Example**:
```python
from data_pipeline_agent_lib.specialists import execute_hdl_workflow, get_workflow_status

# Execute workflow
exec_result = await execute_hdl_workflow.ainvoke({
"workflow_name": "dpl-stream-visits",
"parameters": {}
})

# Check status
status_result = await get_workflow_status.ainvoke({
"workflow_name": "dpl-stream-visits"
})
```

---

### 6. **Ecosystem Assistant**

**Purpose**: Explain DPL components and provide guidance

**Tools** (2):
- `explain_hdl_component` - Component explanations
- `get_hdl_best_practices` - Best practices guidance

**When to use**:
- Learning about DPL architecture
- Understanding specific components
- Need best practices guidance

**Example**:
```python
from data_pipeline_agent_lib.specialists import explain_hdl_component, get_hdl_best_practices

# Explain component
explanation = await explain_hdl_component.ainvoke({
"component_name": "IngestionControl",
"include_examples": True
})

# Get best practices
practices = await get_hdl_best_practices.ainvoke({
"topic": "error handling"
})
```

---

### 7. **DPL Coordinator**

**Purpose**: Coordinate reprocessing scenarios

**Tools** (1):
- `coordinate_hdl_reprocessing` - Reprocessing coordination

**When to use**:
- Urgent reprocessing needed
- Client escalation scenarios
- Need to coordinate with KPI team

**Example**:
```python
from data_pipeline_agent_lib.specialists import coordinate_hdl_reprocessing

result = await coordinate_hdl_reprocessing.ainvoke({
"entity_name": "tasks",
"date_range": "2025-10-04",
"notify_kpi_team": True
})
```

---

## Tool Registry

All tools are registered and categorized:

```python
from data_pipeline_agent_lib.specialists import (
ALL_DPL_TOOLS, # All 10 tools
TROUBLESHOOTING_TOOLS, # 3 tools
OPTIMIZATION_TOOLS, # 2 tools
OPERATIONAL_TOOLS, # 3 tools
DOCUMENTATION_TOOLS, # 2 tools
get_tools_for_intent # Helper function
)

# Get tools by intent
troubleshooting = get_tools_for_intent("troubleshooting")
optimization = get_tools_for_intent("optimization")
```

---

## Specialist Architecture

Each specialist is implemented as a **LangChain Tool**:

```python
from langchain.tools import tool

@tool
async def troubleshoot_hdl_error(
error_message: str,
entity_name: str = None,
pipeline_type: str = None
) -> str:
"""
Diagnose DPL pipeline errors with pattern matching and root cause analysis.

Args:
error_message: The error message or symptom
entity_name: Optional DPL entity (visits, tasks, etc.)
pipeline_type: Optional pipeline type (streaming, batch)

Returns:
Detailed diagnosis with investigation steps
"""
# Implementation here
return diagnosis
```

**Key Features**:
- Async support
- Type hints
- Docstring for LLM understanding
- Structured input/output

---

## Integration with LangGraph

Specialists are integrated into the agent workflow:

```python
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph
from data_pipeline_agent_lib.agent.state import create_initial_state

# Create agent (specialists automatically included)
agent = create_data_pipeline_agent_graph()

# Ask question
state = create_initial_state(
query="Why is the visits streaming pipeline timing out?",
session_id="session_001"
)

# Agent intelligently selects and uses specialists
result = await agent.ainvoke(state)
```

**Agent Workflow**:
1. **Analyze Intent** → Determine user's goal
2. **Select Tools** → Choose relevant specialists
3. **Execute Tools** → Run specialists
4. **Aggregate Results** → Combine outputs
5. **Generate Response** → Create final answer

---

## Specialist Capabilities Comparison

| Specialist | Error Diagnosis | Solutions | Monitoring | Execution | Documentation |
|-----------|----------------|-----------|------------|-----------|---------------|
| Troubleshooter | | | | | |
| Bug Resolver | | | | | |
| Performance Advisor | | | | | |
| Quality Assistant | | | | | |
| DPL Commander | | | | | |
| Ecosystem Assistant | | | | | |
| DPL Coordinator | | | | | |

---

## Common Workflows

### Troubleshooting → Resolution

```python
# Step 1: Diagnose
diagnosis = await troubleshoot_hdl_error.ainvoke({
"error_message": "SCD2 broken",
"entity_name": "visits"
})

# Step 2: Get solution
solution = await resolve_hdl_bug.ainvoke({
"bug_description": "SCD2 is_current incorrect",
"entity_name": "visits"
})
```

### Performance → Quality

```python
# Step 1: Optimize
optimization = await optimize_hdl_pipeline.ainvoke({
"pipeline_name": "dpl-stream-visits",
"performance_issue": "slow processing"
})

# Step 2: Validate
validation = await validate_hdl_data_quality.ainvoke({
"entity_name": "visits",
"quality_dimension": "all"
})
```

### Execute → Monitor

```python
# Step 1: Execute
exec_result = await execute_hdl_workflow.ainvoke({
"workflow_name": "dpl-stream-visits"
})

# Step 2: Monitor
status = await get_workflow_status.ainvoke({
"workflow_name": "dpl-stream-visits"
})
```

---

## Next Steps

### Explore More

- **[Examples](../examples/basic.md)** - Practical usage examples
- **[API Reference](../api/specialists.md)** - Complete API documentation
- **[Architecture](../architecture/clean-architecture.md)** - Design principles
- **[Testing](../testing/test-results.md)** - Test coverage and results

### Individual Specialist Details

All specialists are documented above with:
- Purpose and capabilities
- Available tools
- When to use
- Code examples

For detailed API signatures, see the [API Reference](../api/specialists.md).

