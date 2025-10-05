# Workflow: dpl-stream-tasks

## Overview

**Type:** Streaming  
**Entity:** tasks  
**Purpose:** Real-time ingestion and processing of tasks data from Event Hub to silver layer

---

## Configuration

**Workflow Name:** dpl-stream-tasks  
**Timeout:** 10800 seconds (3.0 hours)  
**Max Concurrent Runs:** Not limited (streaming)  
**Queue:** Enabled

### Trigger Configuration

**Type:** file_arrival  
**Event Hub Path:** `<EVENTHUB_BASE_PATH>evh<ENVIRONMENT>am-ldz012-Operations-Platform-tasks/`  
**Min Time Between Triggers:** `<MIN_TIME_BETWEEN_TRIGGERS_STREAM_SECONDS>`  
**Pause Status:** Configurable via `<PAUSE_STATUS>`

### Health Check Rules

**Metric:** RUN_DURATION_SECONDS  
**Operator:** GREATER_THAN  
**Threshold:** 3600 seconds (1.0 hour)


---

## Orders

### Task 1: bronze_ingestion_streaming

**Purpose:** Ingest from Event Hub to Bronze  
**Notebook:** `/Workspace/Shared/hdl_stm/layers/bronze/bronze_ingestion`  
**Cluster:** CLUSTER_MEMORY_OPTIMIZED_MEDIUM  
**Timeout:** No limit (streaming continuous)

**Parameters:**
- `event_hub_entity_name`: tasks
- `table_name`: frt_am.bronze_Platform.tasks__tasks_stream

**Dependencies:** None (first task)

---

### Task 2: silver_ingestion_streaming

**Purpose:** Process bronze data to silver harmonized layer  
**Notebook:** `/Workspace/Shared/hdl_stm/layers/silver/tasks`  
**Cluster:** CLUSTER_MEMORY_OPTIMIZED_MEDIUM  
**Timeout:** No limit (streaming continuous)

**Parameters:**
None (inherits from state)

**Dependencies:** bronze_ingestion_streaming (must succeed)

---

---

## Data Flow

```
Event Hub (tasks) 
  → bronze_ingestion.py 
  → frt_am.bronze_Platform.tasks__tasks_stream
  → tasks (silver processing)
  → frt_am.bronze_Platform.tasks__tasks_stream_harmonized
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

**team:** hdl
**DataStreamProcessor:** 
**entity:** tasks

---

## Monitoring

**Key Metrics:**
- Execution duration (alert if > 3600s)
- Records processed per run
- Success/failure rate
- Checkpoint lag

**Alerts:**
- Configured via notification_settings
- No alerts for skipped/canceled runs disabled

---

## Related Documentation

- Bronze Ingestion: `hdl_stm/layers/bronze/bronze_ingestion.py`
- Silver Processing: `hdl_stm/layers/silver/tasks.py`
- Entity Documentation: `hdl_Orders.md`
- Streaming Architecture: `DPL_COMPLETE_KNOWLEDGE.md`

---

**Last Updated:** 2025-10-05  
**Source:** workflow_hdl/dpl-stream-tasks.json
