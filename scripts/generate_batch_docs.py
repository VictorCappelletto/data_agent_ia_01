"""
Automated Batch Workflow Documentation Generator

Generates markdown documentation from batch workflow JSON files.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


BATCH_TEMPLATE = """# Workflow: {name}

## Overview

**Type:** Batch  
**Entity:** {entity}  
**Purpose:** Scheduled batch ingestion of {entity_lower} data from CosmosDB to bronze and silver layers

---

## Configuration

**Workflow Name:** {name}  
**Timeout:** {workflow_timeout}  
**Max Concurrent Runs:** {max_concurrent}

### Schedule Configuration

**Type:** CRON  
**Expression:** `{cron_expression}`  
**Timezone:** {timezone}  
**Pause Status:** {pause_status}

---

## Orders

{tasks_section}

---

## Data Flow

```
CosmosDB ({document_store_collection})
  → {entry_notebook}
  → {entity_class}.py (entity class inherits from BaseTable)
  → {bronze_table}
  → {silver_table} (via SCD2)
```

---

## Implementation Details

### Entity Class

**Class:** {entity_class}  
**Parent:** BaseTable  
**Location:** hdl/process/tables/{entity_class}.py

**Key Methods:**
- Bronze to Silver transformation
- SCD2 merge logic
- Data type adjustments
- Harmonization transformations

---

## Troubleshooting

### Common Issues

**1. Timeout Errors**
- **Root Cause:** Large data volume, slow CosmosDB queries, resource constraints
- **Investigation:**
  - Check CosmosDB query performance
  - Verify data volume for time window
  - Review cluster resource utilization
  - Inspect SCD2 merge performance
- **Immediate Action:** 
  - Reprocess manually for specific date
  - Coordinate with KPI team before reprocessing
- **Tools:** GetLastUpdatedAt.py, run_ingestion manual execution

**2. CosmosDB Connection Issues**
- **Root Cause:** Invalid credentials, network issues, firewall blocking
- **Investigation:**
  - Test CosmosDB connection
  - Verify connection string validity
  - Check credential expiration
- **Tools:** DatabaseConnection.py, connection test scripts

**3. SCD2 Merge Problems**
- **Root Cause:** is_current flags incorrect, hash key collisions
- **Investigation:**
  - Check is_current distribution in silver table
  - Verify hash_key uniqueness
  - Review merge logic
- **Solution:** Run AdjustIsCurrent.py tool
- **Tools:** AdjustIsCurrent.py, SCD2 validation queries

**4. Data Quality Issues**
- **Root Cause:** Missing required fields, invalid data types
- **Investigation:**
  - Review data profiling results
  - Check schema compatibility
  - Verify transformation logic
- **Tools:** Data profiling queries, DebugIngestion.py

---

## Tags

{tags}

---

## Monitoring

**Key Metrics:**
- Execution duration (alert if > {health_threshold}s)
- Records processed
- Success/failure rate
- Retry occurrences

**Critical Thresholds:**
{health_monitoring}

---

## Related Documentation

- run_ingestion: `hdl_run_ingestion.md`
- {entity_class} Entity: `hdl_{entity_class}.md`
- BaseTable: `hdl_BaseTable.md`
- IngestionControl: `hdl_IngestionControl.md`
- Batch Architecture: `DPL_COMPLETE_KNOWLEDGE.md`

---

**Last Updated:** 2025-10-05  
**Source:** workflow_hdl/{name}.json
"""


MULTI_ENTITY_TEMPLATE = """# Workflow: {name}

## Overview

**Type:** Batch (Multi-Entity)  
**Entities:** {entities}  
**Purpose:** Scheduled batch ingestion of multiple entities from CosmosDB

---

## Configuration

**Workflow Name:** {name}  
**Timeout:** {workflow_timeout}  
**Max Concurrent Runs:** {max_concurrent}

### Schedule Configuration

**Type:** CRON  
**Expression:** `{cron_expression}`  
**Timezone:** {timezone}  
**Pause Status:** {pause_status}

---

## Orders

{tasks_section}

---

## Data Flow

```
CosmosDB (Multiple Collections)
  ↓
{entry_notebook}
  ↓
{parallel_tasks} Parallel Orders:
{parallel_flow}
  ↓
Silver Layer (SCD2 processing)
```

---

## Execution Pattern

**Parallel Execution:**
- All {task_count} tasks run simultaneously
- No task dependencies
- Independent failure handling
- Efficient resource utilization

**Task Independence:**
- Each task can succeed/fail independently
- No cascading failures
- Isolated error handling

---

## Troubleshooting

### Common Issues

**1. Partial Failure (some tasks succeed, others fail)**
- **Root Cause:** Entity-specific issues (connection, schema, data)
- **Investigation:**
  - Identify which tasks failed
  - Review logs for failed entities
  - Check CosmosDB connection per entity
- **Action:** Rerun failed tasks only

**2. Complete Workflow Failure**
- **Root Cause:** Common infrastructure issue (network, credentials)
- **Investigation:**
  - Check CosmosDB connection health
  - Verify cluster availability
  - Review network connectivity
- **Tools:** DatabaseConnection.py, connection test

**3. Slow Execution**
- **Root Cause:** Large data volumes, resource constraints
- **Investigation:**
  - Check data volume per entity
  - Review cluster resource allocation
  - Verify parallel execution working
- **Optimization:** Consider increasing cluster size

---

## Tags

{tags}

---

## Monitoring

**Key Metrics:**
- Overall workflow success rate
- Per-task execution time
- Parallel execution efficiency
- Data volume per entity

---

## Related Documentation

- Ingestion: `hdl_Ingestion.md`
- Entity Documentation: See individual entity docs
- Batch Architecture: `DPL_COMPLETE_KNOWLEDGE.md`

---

**Last Updated:** 2025-10-05  
**Source:** workflow_hdl/{name}.json
"""


def parse_batch_workflow(json_file: Path) -> Dict[str, Any]:
    """Parse batch workflow JSON and extract key information."""
    with open(json_file) as f:
        data = json.load(f)
    
    # Check if multi-entity workflow
    tasks = data.get("tasks", [])
    is_multi_entity = len(tasks) > 1
    
    # Parse schedule
    schedule = data.get("schedule", {})
    cron = schedule.get("quartz_cron_expression", "<CRON_EXPRESSION_INGESTION_JOBS>")
    timezone = schedule.get("timezone_id", "UTC")
    pause = schedule.get("pause_status", "<PAUSE_STATUS>")
    
    # Parse tasks
    tasks_section = ""
    entities = []
    parallel_flow = []
    
    for i, task in enumerate(tasks, 1):
        task_key = task.get("task_key", f"task_{i}")
        entities.append(task_key)
        notebook_path = task.get("notebook_task", {}).get("notebook_path", "N/A")
        cluster = task.get("job_cluster_key", "N/A")
        params = task.get("notebook_task", {}).get("base_parameters", {})
        timeout = task.get("timeout_seconds", 0)
        max_retries = task.get("max_retries", 0)
        retry_interval = task.get("min_retry_interval_millis", 0)
        health = task.get("health", {})
        
        # Task documentation
        tasks_section += f"""### Task {i}: {task_key}

**Purpose:** {"Batch ingestion from CosmosDB to Bronze and Silver layers" if not is_multi_entity else f"Ingest {params.get('entity', 'N/A')} data"}  
**Notebook:** `{notebook_path}`  
**Cluster:** {cluster}  
**Timeout:** {timeout} seconds ({timeout/60:.0f} minutes)

**Parameters:**
{chr(10).join(f"- `{k}`: {v}" for k, v in params.items()) if params else "None"}

"""
        
        if max_retries > 0:
            tasks_section += f"""**Retry Configuration:**
- Max Retries: {max_retries}
- Min Retry Interval: {retry_interval} ms ({retry_interval/60000:.0f} minutes)
- Retry on Timeout: {task.get('retry_on_timeout', False)}

"""
        
        if health.get("rules"):
            rule = health["rules"][0]
            tasks_section += f"""**Health Check:**
- Metric: {rule.get("metric", "N/A")}
- Operator: {rule.get("op", "N/A")}
- Threshold: {rule.get("value", 0)} seconds ({rule.get("value", 0)/3600:.1f} hour)

"""
        
        tasks_section += f"""**Dependencies:** {"None (single task workflow)" if not is_multi_entity and i == 1 else "None (parallel task)" if is_multi_entity else "Previous task"}

---

"""
        
        # Build parallel flow
        if is_multi_entity:
            entity_name = params.get("entity", task_key)
            parallel_flow.append(f"  - {entity_name} → frt_am.bronze_Platform.{entity_name.lower().replace('-', '_')}")
    
    # Extract entity info
    if is_multi_entity:
        entity = "Multiple"
        entity_class = "Various"
        document_store_collection = "Multiple Collections"
        bronze_table = "Multiple tables (see parallel flow)"
        silver_table = "Multiple tables (see parallel flow)"
    else:
        entity_name = tasks[0].get("task_key", "Unknown")
        params = tasks[0].get("notebook_task", {}).get("base_parameters", {})
        database = params.get("database", entity_name)
        table = params.get("table", entity_name)
        
        entity = database
        entity_class = database.replace("_", "")
        document_store_collection = f"{database} collection"
        bronze_table = f"frt_am.bronze_Platform.{table.lower()}"
        silver_table = f"frt_am.silver_Platform.{table.lower()}_harmonized"
    
    # Health threshold
    health_threshold = 3600
    health_monitoring = "Duration > 3600s triggers health alert"
    
    if tasks[0].get("health", {}).get("rules"):
        rule = tasks[0]["health"]["rules"][0]
        health_threshold = rule.get("value", 3600)
        health_monitoring = f"Duration > {health_threshold}s triggers health alert\nTimeout at {tasks[0].get('timeout_seconds', 5400)}s"
    
    # Parse tags
    tags_data = data.get("tags", {})
    tags_section = "\n".join(f"**{k}:** {v if v else '(marker)'}" for k, v in tags_data.items())
    
    # Entry notebook
    entry_notebook = tasks[0].get("notebook_task", {}).get("notebook_path", "N/A").split("/")[-1]
    
    return {
        "is_multi_entity": is_multi_entity,
        "name": data.get("name", "Unknown"),
        "entity": entity,
        "entity_lower": entity.lower(),
        "entity_class": entity_class,
        "workflow_timeout": f"No limit (task-level timeout: {tasks[0].get('timeout_seconds', 0)}s)" if tasks[0].get('timeout_seconds') else "No limit",
        "max_concurrent": data.get("max_concurrent_runs", 1),
        "cron_expression": cron,
        "timezone": timezone,
        "pause_status": pause if pause != "<PAUSE_STATUS>" else "Configurable via <PAUSE_STATUS>",
        "tasks_section": tasks_section.strip(),
        "document_store_collection": document_store_collection,
        "bronze_table": bronze_table,
        "silver_table": silver_table,
        "entry_notebook": entry_notebook,
        "tags": tags_section,
        "health_threshold": health_threshold,
        "health_monitoring": health_monitoring,
        # Multi-entity specific
        "entities": ", ".join(entities),
        "task_count": len(tasks),
        "parallel_tasks": len(tasks),
        "parallel_flow": "\n".join(parallel_flow)
    }


def generate_batch_doc(json_file: Path, output_dir: Path):
    """Generate markdown documentation for batch workflow."""
    data = parse_batch_workflow(json_file)
    
    if data["is_multi_entity"]:
        doc_content = MULTI_ENTITY_TEMPLATE.format(**data)
    else:
        doc_content = BATCH_TEMPLATE.format(**data)
    
    output_file = output_dir / f"{data['name']}.md"
    output_file.write_text(doc_content)
    print(f"  ✅ Generated: {output_file.name}")


if __name__ == "__main__":
    # Directories
    workflow_dir = Path(__file__).parent.parent / "workflow_hdl"
    output_dir = Path(__file__).parent.parent / "data_pipeline_agent_lib" / "knowledge" / "workflows" / "batch"
    
    # Find batch workflows
    batch_files = list(workflow_dir.glob("dpl-ingestion-*.json"))
    batch_files.extend(workflow_dir.glob("sharedtables-ingestion.json"))
    
    print(f"Batch Workflow Documentation Generator")
    print("=" * 70)
    print(f"\nFound {len(batch_files)} batch workflows")
    print(f"Output directory: {output_dir}")
    print("")
    
    # Generate docs
    for json_file in batch_files:
        try:
            generate_batch_doc(json_file, output_dir)
        except Exception as e:
            print(f"  ❌ Error processing {json_file.name}: {e}")
    
    print(f"\n{'=' * 70}")
    print(f"Generated {len(list(output_dir.glob('*.md')))} documentation files")

