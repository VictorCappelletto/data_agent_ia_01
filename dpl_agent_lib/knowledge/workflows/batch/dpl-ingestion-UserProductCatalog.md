# Workflow: dpl-ingestion-UserProductCatalog

## Overview

**Type:** Batch  
**Entity:** UserProductCatalog  
**Purpose:** Scheduled batch ingestion of userclientcatalog data from CosmosDB to bronze and silver layers

---

## Configuration

**Workflow Name:** dpl-ingestion-UserProductCatalog  
**Timeout:** No limit (task-level timeout: 5400s)  
**Max Concurrent Runs:** 1

### Schedule Configuration

**Type:** CRON  
**Expression:** `<CRON_EXPRESSION_INGESTION_JOBS>`  
**Timezone:** UTC  
**Pause Status:** Configurable via <PAUSE_STATUS>

---

## Orders

### Task 1: UserAccounts

**Purpose:** Batch ingestion from CosmosDB to Bronze and Silver layers  
**Notebook:** `/Shared/Operations-Platform-dm-app/hdl/run_ingestion_ucc`  
**Cluster:** CLUSTER_GENERAL_PURPOSE_MEDIUM  
**Timeout:** 5400 seconds (90 minutes)

**Parameters:**
- `database`: UserProductCatalog
- `table`: UserAccounts

**Retry Configuration:**
- Max Retries: 1
- Min Retry Interval: 900000 ms (15 minutes)
- Retry on Timeout: False

**Health Check:**
- Metric: RUN_DURATION_SECONDS
- Operator: GREATER_THAN
- Threshold: 3600 seconds (1.0 hour)

**Dependencies:** None (single task workflow)

---

---

## Data Flow

```
CosmosDB (UserProductCatalog collection)
  → run_ingestion_ucc
  → UserProductCatalog.py (entity class inherits from BaseTable)
  → frt_am.bronze_Platform.useraccounts
  → frt_am.silver_Platform.useraccounts_harmonized (via SCD2)
```

---

## Implementation Details

### Entity Class

**Class:** UserProductCatalog  
**Parent:** BaseTable  
**Location:** hdl/process/tables/UserProductCatalog.py

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

**team:** hdl
**type:** ingestion

---

## Monitoring

**Key Metrics:**
- Execution duration (alert if > 3600s)
- Records processed
- Success/failure rate
- Retry occurrences

**Critical Thresholds:**
Duration > 3600s triggers health alert
Timeout at 5400s

---

## Related Documentation

- run_ingestion: `hdl_run_ingestion.md`
- UserProductCatalog Entity: `hdl_UserProductCatalog.md`
- BaseTable: `hdl_BaseTable.md`
- IngestionControl: `hdl_IngestionControl.md`
- Batch Architecture: `DPL_COMPLETE_KNOWLEDGE.md`

---

**Last Updated:** 2025-10-05  
**Source:** workflow_hdl/dpl-ingestion-UserProductCatalog.json
