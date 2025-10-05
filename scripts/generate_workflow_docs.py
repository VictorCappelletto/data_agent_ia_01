"""
Automated Workflow Documentation Generator

Generates markdown documentation from workflow JSON files.
"""

import json
from pathlib import Path
from typing import Dict, Any


STREAMING_TEMPLATE = """# Workflow: {name}

## Overview

**Type:** Streaming  
**Entity:** {entity}  
**Purpose:** Real-time ingestion and processing of {entity} data from Event Hub to silver layer

---

## Configuration

**Workflow Name:** {name}  
**Timeout:** {timeout} seconds ({timeout_hours})  
**Max Concurrent Runs:** Not limited (streaming)  
**Queue:** {queue_enabled}

### Trigger Configuration

**Type:** file_arrival  
**Event Hub Path:** `{event_hub_path}`  
**Min Time Between Triggers:** `<MIN_TIME_BETWEEN_TRIGGERS_STREAM_SECONDS>`  
**Pause Status:** Configurable via `<PAUSE_STATUS>`

### Health Check Rules

{health_rules}

---

## Orders

{tasks_section}

---

## Data Flow

```
Event Hub ({entity}) 
  → bronze_ingestion.py 
  → {bronze_table}
  → {silver_notebook} (silver processing)
  → {silver_table}
```

---

## Troubleshooting

### Common Issues

**1. Timeout Errors (> 1 hour)**
- **Root Cause:** Large data volume, checkpoint corruption, resource constraints
- **Investigation:**
  - Check Event Hub message backlog
  - Verify checkpoint location integrity
  - Review cluster resource utilization
  - Inspect data volume in time window
- **Tools:** GetLastUpdatedAt.py, Databricks Workflows tab

**2. Checkpoint Corruption**
- **Root Cause:** Interrupted streaming job, DBFS issues
- **Solution:** 
  - Stop streaming pipeline
  - Delete checkpoint directory
  - Restart with clean checkpoint
- **Tools:** DBFS file browser

**3. Data Quality Issues**
- **Root Cause:** Schema changes, invalid data from Event Hub
- **Investigation:**
  - Check Event Hub message format
  - Verify schema compatibility
  - Review data validation rules
- **Tools:** DebugIngestion.py, data profiling queries

---

## Tags

{tags}

---

## Monitoring

**Key Metrics:**
- Execution duration (alert if > {health_threshold}s)
- Records processed per run
- Success/failure rate
- Checkpoint lag

**Alerts:**
- Configured via notification_settings
- No alerts for skipped/canceled runs disabled

---

## Related Documentation

- Bronze Ingestion: `hdl_stm/layers/bronze/bronze_ingestion.py`
- Silver Processing: `hdl_stm/layers/silver/{entity_lower}.py`
- Entity Documentation: `hdl_{entity_class}.md`
- Streaming Architecture: `DPL_COMPLETE_KNOWLEDGE.md`

---

**Last Updated:** 2025-10-05  
**Source:** workflow_hdl/{name}.json
"""


def parse_streaming_workflow(json_file: Path) -> Dict[str, Any]:
    """Parse streaming workflow JSON and extract key information."""
    with open(json_file) as f:
        data = json.load(f)
    
    # Extract entity from first task or workflow name
    entity = data.get("tags", {}).get("entity", "unknown")
    if entity == "unknown":
        # Try to extract from name
        name = data.get("name", "")
        if "visits" in name:
            entity = "visits"
        elif "tasks" in name:
            entity = "tasks"
        elif "vendorgroups" in name:
            entity = "vendorgroups"
        elif "userclientcatalog" in name:
            entity = "userclientcatalog"
        elif "activitystaging" in name:
            entity = "activitystaging"
    
    # Parse tasks
    tasks = data.get("tasks", [])
    tasks_section = ""
    bronze_table = "N/A"
    silver_table = "N/A"
    silver_notebook = "N/A"
    
    for i, task in enumerate(tasks, 1):
        task_key = task.get("task_key", f"task_{i}")
        notebook_path = task.get("notebook_task", {}).get("notebook_path", "N/A")
        cluster = task.get("job_cluster_key", "N/A")
        params = task.get("notebook_task", {}).get("base_parameters", {})
        
        # Extract table names
        if "bronze" in task_key.lower():
            bronze_table = params.get("table_name", "N/A")
        elif "silver" in task_key.lower():
            silver_notebook = notebook_path.split("/")[-1] if notebook_path != "N/A" else "N/A"
            silver_table = bronze_table.replace("_stream", "_stream_harmonized") if bronze_table != "N/A" else "N/A"
        
        tasks_section += f"""### Task {i}: {task_key}

**Purpose:** {"Ingest from Event Hub to Bronze" if "bronze" in task_key.lower() else "Process bronze data to silver harmonized layer"}  
**Notebook:** `{notebook_path}`  
**Cluster:** {cluster}  
**Timeout:** No limit (streaming continuous)

**Parameters:**
{chr(10).join(f"- `{k}`: {v}" for k, v in params.items()) if params else "None (inherits from state)"}

**Dependencies:** {"None (first task)" if i == 1 else f"{tasks[i-2].get('task_key', 'previous')} (must succeed)"}

---

"""
    
    # Parse health rules
    health_rules = data.get("health", {}).get("rules", [])
    health_section = ""
    health_threshold = 3600
    
    if health_rules:
        for rule in health_rules:
            metric = rule.get("metric", "N/A")
            op = rule.get("op", "N/A")
            value = rule.get("value", 0)
            health_threshold = value
            health_section += f"""**Metric:** {metric}  
**Operator:** {op}  
**Threshold:** {value} seconds ({value/3600:.1f} hour{"s" if value/3600 > 1 else ""})
"""
    else:
        health_section = "No health check rules configured"
    
    # Parse event hub path
    trigger = data.get("trigger", {})
    event_hub = trigger.get("file_arrival", {}).get("url", "N/A")
    
    # Parse tags
    tags_data = data.get("tags", {})
    tags_section = "\n".join(f"**{k}:** {v}" for k, v in tags_data.items())
    
    return {
        "name": data.get("name", "Unknown"),
        "entity": entity,
        "entity_lower": entity.lower(),
        "entity_class": entity.replace("_", "").title(),
        "timeout": data.get("timeout_seconds", 10800),
        "timeout_hours": f"{data.get('timeout_seconds', 10800)/3600:.1f} hours",
        "queue_enabled": "Enabled" if data.get("queue", {}).get("enabled", False) else "Disabled",
        "event_hub_path": event_hub,
        "health_rules": health_section,
        "health_threshold": health_threshold,
        "tasks_section": tasks_section.strip(),
        "bronze_table": bronze_table,
        "silver_table": silver_table,
        "silver_notebook": silver_notebook,
        "tags": tags_section
    }


def generate_streaming_doc(json_file: Path, output_dir: Path):
    """Generate markdown documentation for streaming workflow."""
    data = parse_streaming_workflow(json_file)
    doc_content = STREAMING_TEMPLATE.format(**data)
    
    output_file = output_dir / f"{data['name']}.md"
    output_file.write_text(doc_content)
    print(f"  ✅ Generated: {output_file.name}")


if __name__ == "__main__":
    # Directories
    workflow_dir = Path(__file__).parent.parent / "workflow_hdl"
    output_dir = Path(__file__).parent.parent / "data_pipeline_agent_lib" / "knowledge" / "workflows" / "streaming"
    
    # Find streaming workflows
    streaming_files = list(workflow_dir.glob("dpl-stream-*.json"))
    
    print(f"Workflow Documentation Generator")
    print("=" * 70)
    print(f"\nFound {len(streaming_files)} streaming workflows")
    print(f"Output directory: {output_dir}")
    print("")
    
    # Generate docs
    for json_file in streaming_files:
        try:
            generate_streaming_doc(json_file, output_dir)
        except Exception as e:
            print(f"  ❌ Error processing {json_file.name}: {e}")
    
    print(f"\n{'=' * 70}")
    print(f"Generated {len(list(output_dir.glob('*.md')))} documentation files")

