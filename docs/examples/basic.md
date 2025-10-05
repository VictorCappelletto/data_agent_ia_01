# Basic Examples

Simple examples to get you started with DPL Agent.

---

## Specialist Tools (No API Keys Required)

### Example 1: Error Diagnosis

```python
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

# Diagnose a timeout error
result = await troubleshoot_hdl_error.ainvoke({
"error_message": "Pipeline timeout after 90 minutes",
"entity_name": "visits",
"pipeline_type": "streaming"
})

print(result)
```

**Output:**
```
TROUBLESHOOTING ANALYSIS

Diagnosis: Detected timeout error pattern
Severity: HIGH
Confidence: 85%

Root Cause Candidates:
• Large data volume processing
• Cluster resource constraints

Investigation Steps:
1. Check pipeline execution duration
2. Review cluster resource utilization
3. Verify data volume processed
4. Inspect checkpoint location
```

---

### Example 2: Bug Resolution

```python
from data_pipeline_agent_lib.specialists import resolve_hdl_bug

# Get solution for SCD2 issue
result = await resolve_hdl_bug.ainvoke({
"bug_description": "SCD2 is_current flags are incorrect after merge",
"entity_name": "visits"
})

print(result)
```

---

### Example 3: Performance Optimization

```python
from data_pipeline_agent_lib.specialists import optimize_hdl_pipeline

# Get optimization recommendations
result = await optimize_hdl_pipeline.ainvoke({
"pipeline_name": "hdl-batch-tasks",
"performance_issue": "Pipeline is running too slow, takes 2+ hours"
})

print(result)
```

---

### Example 4: Data Quality Validation

```python
from data_pipeline_agent_lib.specialists import validate_hdl_data_quality

# Check data quality
result = await validate_hdl_data_quality.ainvoke({
"entity_name": "visits",
"quality_dimension": "completeness"
})

print(result)
```

---

### Example 5: Workflow Execution

```python
from data_pipeline_agent_lib.specialists import execute_hdl_workflow, get_workflow_status

# Execute workflow
exec_result = await execute_hdl_workflow.ainvoke({
"workflow_name": "dpl-stream-visits",
"parameters": {"vendor": "BR"}
})

print(f"Execution: {exec_result}")

# Check status
status_result = await get_workflow_status.ainvoke({
"workflow_name": "dpl-stream-visits"
})

print(f"Status: {status_result}")
```

---

### Example 6: Component Explanation

```python
from data_pipeline_agent_lib.specialists import explain_hdl_component

# Learn about a component
result = await explain_hdl_component.ainvoke({
"component_name": "IngestionControl",
"include_examples": True
})

print(result)
```

---

### Example 7: Reprocessing Coordination

```python
from data_pipeline_agent_lib.specialists import coordinate_hdl_reprocessing

# Coordinate urgent reprocessing
result = await coordinate_hdl_reprocessing.ainvoke({
"entity_name": "tasks",
"date_range": "2025-10-04",
"urgency": "high",
"notify_kpi_team": True
})

print(result)
```

---

## Complete Agent (Requires API Keys)

### Example 8: Simple Q&A

```python
import os
from data_pipeline_agent_lib.agent import create_simple_hdl_graph
from data_pipeline_agent_lib.agent.state import create_initial_state

# Configure API keys
os.environ["ANTHROPIC_API_KEY"] = "your-key-here"
os.environ["OPENAI_API_KEY"] = "your-key-here"

# Create agent
agent = create_simple_hdl_graph()

# Ask question
state = create_initial_state(
query="What is SCD2 and how is it used in DPL?",
session_id="session_001"
)

# Get response
result = await agent.ainvoke(state)

print(result["final_response"])
```

---

### Example 9: Multi-Turn Conversation

```python
from data_pipeline_agent_lib.utils.checkpointer import create_conversation_config

# Create config with thread ID
config = create_conversation_config("my_thread_001")

# First question
state1 = create_initial_state(
query="How do I troubleshoot a timeout in visits streaming?",
session_id="my_thread_001"
)
result1 = await agent.ainvoke(state1, config=config)
print(f"Response 1: {result1['final_response']}")

# Follow-up (agent remembers context!)
state2 = create_initial_state(
query="What are the most common causes?",
session_id="my_thread_001"
)
result2 = await agent.ainvoke(state2, config=config)
print(f"Response 2: {result2['final_response']}")

# Another follow-up
state3 = create_initial_state(
query="How do I fix it?",
session_id="my_thread_001"
)
result3 = await agent.ainvoke(state3, config=config)
print(f"Response 3: {result3['final_response']}")
```

---

### Example 10: Streaming Responses

```python
async def stream_agent_response(query: str):
"""Stream agent responses in real-time"""

agent = create_simple_hdl_graph()
state = create_initial_state(query, session_id="stream_001")

print(f"Query: {query}\n")
print("Response: ", end="", flush=True)

async for chunk in agent.astream(state):
if "final_response" in chunk:
print(chunk["final_response"], end="", flush=True)

print("\n")

# Use it
await stream_agent_response("How do I reprocess visits data for yesterday?")
```

---

### Example 11: Inspect Agent State

```python
# Create and invoke agent
agent = create_simple_hdl_graph()
state = create_initial_state(
query="Diagnose timeout in visits streaming pipeline",
session_id="debug_001"
)

result = await agent.ainvoke(state)

# Inspect state
print("=== Agent State ===")
print(f"Intent: {result.get('intent', 'N/A')}")
print(f"Tools Called: {result.get('tools_to_call', [])}")
print(f"Iterations: {result.get('iteration_count', 0)}")
print(f"\nReasoning Steps:")
for step in result.get("reasoning", []):
print(f" • {step}")

print(f"\nRetrieved Documents: {len(result.get('retrieved_documents', []))}")
print(f"\nFinal Response:\n{result['final_response']}")
```

---

## Batch Processing

### Example 12: Process Multiple Queries

```python
async def batch_diagnose(errors: list):
"""Diagnose multiple errors"""

from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error
import asyncio

tasks = [
troubleshoot_hdl_error.ainvoke({
"error_message": error["message"],
"entity_name": error.get("entity"),
"pipeline_type": error.get("type")
})
for error in errors
]

results = await asyncio.gather(*tasks)
return results

# Use it
errors = [
{"message": "Timeout after 90 minutes", "entity": "visits", "type": "streaming"},
{"message": "SCD2 is_current broken", "entity": "tasks", "type": "batch"},
{"message": "UUID conversion failed", "entity": "accounts", "type": "batch"}
]

diagnoses = await batch_diagnose(errors)

for i, diagnosis in enumerate(diagnoses):
print(f"\n=== Error {i+1} ===")
print(diagnosis)
```

---

## Error Handling

### Example 13: Graceful Error Handling

```python
async def safe_troubleshoot(error_message: str, entity: str = None):
"""Troubleshoot with error handling"""

from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

try:
result = await troubleshoot_hdl_error.ainvoke({
"error_message": error_message,
"entity_name": entity
})
return {"success": True, "result": result}

except Exception as e:
return {
"success": False,
"error": str(e),
"fallback": "Please contact DPL support team"
}

# Use it
result = await safe_troubleshoot("Unknown error XYZ123", "visits")

if result["success"]:
print(result["result"])
else:
print(f"Error: {result['error']}")
print(f"Fallback: {result['fallback']}")
```

---

## Complete Workflow Example

### Example 14: Full Troubleshooting Workflow

```python
async def complete_troubleshooting_workflow(
error_message: str,
entity_name: str,
pipeline_type: str
):
"""
Complete workflow:
1. Diagnose error
2. Get resolution steps
3. Validate data quality
4. Check pipeline status
"""

from data_pipeline_agent_lib.specialists import (
troubleshoot_hdl_error,
resolve_hdl_bug,
validate_hdl_data_quality,
get_workflow_status
)

print("=== STEP 1: Diagnosis ===")
diagnosis = await troubleshoot_hdl_error.ainvoke({
"error_message": error_message,
"entity_name": entity_name,
"pipeline_type": pipeline_type
})
print(diagnosis)

print("\n=== STEP 2: Resolution ===")
resolution = await resolve_hdl_bug.ainvoke({
"bug_description": error_message,
"entity_name": entity_name
})
print(resolution)

print("\n=== STEP 3: Quality Check ===")
quality = await validate_hdl_data_quality.ainvoke({
"entity_name": entity_name,
"quality_dimension": "all"
})
print(quality)

print("\n=== STEP 4: Pipeline Status ===")
status = await get_workflow_status.ainvoke({
"workflow_name": f"hdl-{pipeline_type}-{entity_name}"
})
print(status)

return {
"diagnosis": diagnosis,
"resolution": resolution,
"quality": quality,
"status": status
}

# Use it
result = await complete_troubleshooting_workflow(
error_message="Pipeline timeout after 90 minutes",
entity_name="visits",
pipeline_type="streaming"
)
```

---

## Next Steps

- **[Deployment Guide](../deployment/quickstart.md)** - Deploy to Databricks
- **[Architecture Diagrams](../architecture/agent-flow.md)** - Visual architecture
- **[API Reference](../api/specialists.md)** - Complete API documentation
- **[Testing Results](../testing/test-results.md)** - 179 tests passing

