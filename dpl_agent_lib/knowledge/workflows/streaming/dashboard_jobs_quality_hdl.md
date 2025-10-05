# Workflow: dashboard_jobs_quality_hdl

## Overview

**Type:** Streaming  
**Entity:** unknown  
**Purpose:** Real-time ingestion and processing of unknown data from Event Hub to silver layer

---

## Configuration

**Workflow Name:** dashboard_jobs_quality_hdl  
**Timeout:** 0 seconds (0.0 hours)  
**Max Concurrent Runs:** Not limited (streaming)  
**Queue:** Disabled

### Trigger Configuration

**Type:** file_arrival  
**Event Hub Path:** `N/A`  
**Min Time Between Triggers:** `<MIN_TIME_BETWEEN_TRIGGERS_STREAM_SECONDS>`  
**Pause Status:** Configurable via `<PAUSE_STATUS>`

### Health Check Rules

No health check rules configured

---

## Orders

### Task 1: jobs_quality_hdl

**Purpose:** Process bronze data to silver harmonized layer  
**Notebook:** `/Workspace/Shared/hdl_stm/quality/extract/run_pbi_tables`  
**Cluster:** CLUSTER_GENERAL_PURPOSE_SMALL  
**Timeout:** No limit (streaming continuous)

**Parameters:**
- `process_name`: jobs_quality_hdl
- `job_id`: {{job.id}}
- `run_id`: {{job.run_id}}

**Dependencies:** None (first task)

---

---

## Data Flow

```
Event Hub (unknown) 
  → bronze_ingestion.py 
  → N/A
  → N/A (silver processing)
  → N/A
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
- Silver Processing: `hdl_stm/layers/silver/unknown.py`
- Entity Documentation: `hdl_Unknown.md`
- Streaming Architecture: `DPL_COMPLETE_KNOWLEDGE.md`

---

**Last Updated:** 2025-10-05  
**Source:** workflow_hdl/dashboard_jobs_quality_hdl.json
