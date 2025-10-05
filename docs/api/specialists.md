# Specialists API Reference

Complete API reference for all DPL specialist tools.

---

## Import

```python
from data_pipeline_agent_lib.specialists import (
# Troubleshooting
troubleshoot_hdl_error,
analyze_pipeline_health,

# Bug Resolution
resolve_hdl_bug,

# Performance
optimize_hdl_pipeline,

# Quality
validate_hdl_data_quality,

# Workflow Management
execute_hdl_workflow,
get_workflow_status,

# Documentation
explain_hdl_component,
get_hdl_best_practices,

# Coordination
coordinate_hdl_reprocessing,

# Collections
ALL_DPL_TOOLS,
TROUBLESHOOTING_TOOLS,
OPTIMIZATION_TOOLS,
OPERATIONAL_TOOLS,
DOCUMENTATION_TOOLS,

# Helper
get_tools_for_intent
)
```

---

## Troubleshooting Tools

### troubleshoot_hdl_error

Diagnose DPL pipeline errors with pattern matching and root cause analysis.

**Signature:**
```python
async def troubleshoot_hdl_error(
error_message: str,
entity_name: str = None,
pipeline_type: str = None
) -> str
```

**Parameters:**
- `error_message` (str, required): The error message or symptom to diagnose
- `entity_name` (str, optional): DPL entity name (visits, tasks, accounts, etc.)
- `pipeline_type` (str, optional): Pipeline type (streaming, batch, sharedtables)

**Returns:**
- str: Detailed diagnosis with severity, confidence, root causes, investigation steps

**Example:**
```python
result = await troubleshoot_hdl_error.ainvoke({
"error_message": "Pipeline timeout after 90 minutes",
"entity_name": "visits",
"pipeline_type": "streaming"
})
```

---

### analyze_pipeline_health

Analyze DPL pipeline health and identify potential issues.

**Signature:**
```python
async def analyze_pipeline_health(
pipeline_name: str,
check_metrics: bool = True
) -> str
```

**Parameters:**
- `pipeline_name` (str, required): Name of the DPL pipeline
- `check_metrics` (bool, optional): Whether to include performance metrics. Default: True

**Returns:**
- str: Health analysis with status, metrics, and recommendations

**Example:**
```python
result = await analyze_pipeline_health.ainvoke({
"pipeline_name": "dpl-stream-visits",
"check_metrics": True
})
```

---

## Bug Resolution Tools

### resolve_hdl_bug

Get resolution steps for known DPL bugs and issues.

**Signature:**
```python
async def resolve_hdl_bug(
bug_description: str,
entity_name: str = None
) -> str
```

**Parameters:**
- `bug_description` (str, required): Description of the bug or issue
- `entity_name` (str, optional): DPL entity affected

**Returns:**
- str: Step-by-step resolution guide with known solutions

**Example:**
```python
result = await resolve_hdl_bug.ainvoke({
"bug_description": "SCD2 is_current flags are incorrect",
"entity_name": "visits"
})
```

---

## Performance Tools

### optimize_hdl_pipeline

Get performance optimization recommendations for DPL pipelines.

**Signature:**
```python
async def optimize_hdl_pipeline(
pipeline_name: str,
performance_issue: str = None
) -> str
```

**Parameters:**
- `pipeline_name` (str, required): Name of the DPL pipeline
- `performance_issue` (str, optional): Specific performance issue observed

**Returns:**
- str: Optimization strategies and recommendations

**Example:**
```python
result = await optimize_hdl_pipeline.ainvoke({
"pipeline_name": "hdl-batch-tasks",
"performance_issue": "Pipeline taking 2+ hours to complete"
})
```

---

## Quality Tools

### validate_hdl_data_quality

Validate DPL data quality across various dimensions.

**Signature:**
```python
async def validate_hdl_data_quality(
entity_name: str,
quality_dimension: str = "all"
) -> str
```

**Parameters:**
- `entity_name` (str, required): DPL entity to validate
- `quality_dimension` (str, optional): Quality dimension to check
- Options: "completeness", "accuracy", "consistency", "timeliness", "all"
- Default: "all"

**Returns:**
- str: Data quality report with validation results

**Example:**
```python
result = await validate_hdl_data_quality.ainvoke({
"entity_name": "visits",
"quality_dimension": "completeness"
})
```

---

## Workflow Management Tools

### execute_hdl_workflow

Execute an DPL Databricks workflow.

**Signature:**
```python
async def execute_hdl_workflow(
workflow_name: str,
parameters: dict = None
) -> str
```

**Parameters:**
- `workflow_name` (str, required): Name of the workflow to execute
- `parameters` (dict, optional): Workflow parameters

**Returns:**
- str: Execution confirmation with run ID and status

**Example:**
```python
result = await execute_hdl_workflow.ainvoke({
"workflow_name": "dpl-stream-visits",
"parameters": {"vendor": "BR", "date": "2025-10-04"}
})
```

---

### get_workflow_status

Get the status of an DPL workflow execution.

**Signature:**
```python
async def get_workflow_status(
workflow_name: str,
run_id: str = None
) -> str
```

**Parameters:**
- `workflow_name` (str, required): Name of the workflow
- `run_id` (str, optional): Specific run ID to check. If not provided, checks latest run

**Returns:**
- str: Workflow status with execution details

**Example:**
```python
result = await get_workflow_status.ainvoke({
"workflow_name": "dpl-stream-visits",
"run_id": "12345"
})
```

---

## Documentation Tools

### explain_hdl_component

Explain DPL components, architecture, and concepts.

**Signature:**
```python
async def explain_hdl_component(
component_name: str,
include_examples: bool = False
) -> str
```

**Parameters:**
- `component_name` (str, required): Component to explain (e.g., "IngestionControl", "SCD2", "TableFactory")
- `include_examples` (bool, optional): Include code examples. Default: False

**Returns:**
- str: Detailed explanation with usage information

**Example:**
```python
result = await explain_hdl_component.ainvoke({
"component_name": "IngestionControl",
"include_examples": True
})
```

---

### get_hdl_best_practices

Get DPL best practices and recommendations.

**Signature:**
```python
async def get_hdl_best_practices(
topic: str = "general"
) -> str
```

**Parameters:**
- `topic` (str, optional): Specific topic for best practices
- Options: "error handling", "performance", "data quality", "monitoring", "general"
- Default: "general"

**Returns:**
- str: Best practices guidance

**Example:**
```python
result = await get_hdl_best_practices.ainvoke({
"topic": "error handling"
})
```

---

## Coordination Tools

### coordinate_hdl_reprocessing

Coordinate DPL reprocessing scenarios, including team notifications.

**Signature:**
```python
async def coordinate_hdl_reprocessing(
entity_name: str,
date_range: str,
urgency: str = "normal",
notify_kpi_team: bool = False
) -> str
```

**Parameters:**
- `entity_name` (str, required): DPL entity to reprocess
- `date_range` (str, required): Date or date range to reprocess (e.g., "2025-10-04", "2025-10-01 to 2025-10-04")
- `urgency` (str, optional): Urgency level ("low", "normal", "high"). Default: "normal"
- `notify_kpi_team` (bool, optional): Whether to notify KPI team. Default: False

**Returns:**
- str: Reprocessing plan with steps and coordination details

**Example:**
```python
result = await coordinate_hdl_reprocessing.ainvoke({
"entity_name": "tasks",
"date_range": "2025-10-04",
"urgency": "high",
"notify_kpi_team": True
})
```

---

## Collections

### ALL_DPL_TOOLS

List of all 10 DPL specialist tools.

```python
from data_pipeline_agent_lib.specialists import ALL_DPL_TOOLS

print(f"Total tools: {len(ALL_DPL_TOOLS)}")
for tool in ALL_DPL_TOOLS:
print(f" - {tool.name}")
```

---

### Tool Categories

**TROUBLESHOOTING_TOOLS** (3 tools):
- troubleshoot_hdl_error
- analyze_pipeline_health
- resolve_hdl_bug

**OPTIMIZATION_TOOLS** (2 tools):
- optimize_hdl_pipeline
- validate_hdl_data_quality

**OPERATIONAL_TOOLS** (3 tools):
- execute_hdl_workflow
- get_workflow_status
- coordinate_hdl_reprocessing

**DOCUMENTATION_TOOLS** (2 tools):
- explain_hdl_component
- get_hdl_best_practices

---

## Helper Functions

### get_tools_for_intent

Get specialist tools based on user intent.

**Signature:**
```python
def get_tools_for_intent(intent: str) -> List[Tool]
```

**Parameters:**
- `intent` (str): User intent category
- Options: "troubleshooting", "optimization", "operations", "documentation"

**Returns:**
- List[Tool]: List of relevant specialist tools

**Example:**
```python
from data_pipeline_agent_lib.specialists import get_tools_for_intent

troubleshooting_tools = get_tools_for_intent("troubleshooting")
print(f"Found {len(troubleshooting_tools)} tools")
```

---

## Usage Patterns

### Synchronous Usage (Not Recommended)

```python
# Don't do this - blocking call
result = troubleshoot_hdl_error.invoke({
"error_message": "error"
})
```

### Asynchronous Usage (Recommended)

```python
# Do this - non-blocking
result = await troubleshoot_hdl_error.ainvoke({
"error_message": "error"
})
```

### Batch Processing

```python
import asyncio

tasks = [
troubleshoot_hdl_error.ainvoke({"error_message": "error1"}),
troubleshoot_hdl_error.ainvoke({"error_message": "error2"}),
troubleshoot_hdl_error.ainvoke({"error_message": "error3"})
]

results = await asyncio.gather(*tasks)
```

---

## Error Handling

All specialist tools return structured error messages if something goes wrong:

```python
try:
result = await troubleshoot_hdl_error.ainvoke({
"error_message": "test"
})
except Exception as e:
print(f"Tool execution failed: {e}")
```

---

## Next Steps

- **[Basic Examples](../examples/basic.md)** - Practical usage examples
- **[Specialist Overview](../specialists/overview.md)** - All 7 specialists explained
- **[Architecture Diagrams](../architecture/agent-flow.md)** - Visual architecture
- **[Deployment Guide](../deployment/quickstart.md)** - Deploy to Databricks

