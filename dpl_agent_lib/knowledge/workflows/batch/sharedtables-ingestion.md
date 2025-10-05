# Workflow: sharedtables-ingestion

## Overview

**Type:** Batch (Multi-Entity)  
**Entities:** AccessRule, AuthUserHierarchy, PartnerGroups  
**Purpose:** Scheduled batch ingestion of multiple entities from CosmosDB

---

## Configuration

**Workflow Name:** sharedtables-ingestion  
**Timeout:** No limit  
**Max Concurrent Runs:** 1

### Schedule Configuration

**Type:** CRON  
**Expression:** `0 0/30 * 1/1 * ? *`  
**Timezone:** UTC  
**Pause Status:** PAUSED

---

## Orders

### Task 1: AccessRule

**Purpose:** Ingest identity-authorization data  
**Notebook:** `/Shared/Operations-Platform-dm-app/hdl/Ingestion`  
**Cluster:** CLUSTER_GENERAL_PURPOSE_MEDIUM  
**Timeout:** 0 seconds (0 minutes)

**Parameters:**
- `entity`: identity-authorization
- `region`: am
- `domain`: frt
- `source`: document_store

**Dependencies:** None (parallel task)

---

### Task 2: AuthUserHierarchy

**Purpose:** Ingest identity-user data  
**Notebook:** `/Shared/Operations-Platform-dm-app/hdl/Ingestion`  
**Cluster:** CLUSTER_GENERAL_PURPOSE_MEDIUM  
**Timeout:** 0 seconds (0 minutes)

**Parameters:**
- `entity`: identity-user
- `region`: am
- `domain`: frt
- `source`: document_store

**Dependencies:** None (parallel task)

---

### Task 3: PartnerGroups

**Purpose:** Ingest vendorgroups data  
**Notebook:** `/Shared/Operations-Platform-dm-app/hdl/Ingestion`  
**Cluster:** CLUSTER_GENERAL_PURPOSE_MEDIUM  
**Timeout:** 0 seconds (0 minutes)

**Parameters:**
- `entity`: vendorgroups
- `region`: am
- `domain`: frt
- `source`: document_store

**Dependencies:** None (parallel task)

---

---

## Data Flow

```
CosmosDB (Multiple Collections)
  ↓
Ingestion
  ↓
3 Parallel Orders:
  - identity-authorization → frt_am.bronze_Platform.identity_authorization
  - identity-user → frt_am.bronze_Platform.identity_user
  - vendorgroups → frt_am.bronze_Platform.vendorgroups
  ↓
Silver Layer (SCD2 processing)
```

---

## Execution Pattern

**Parallel Execution:**
- All 3 tasks run simultaneously
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

**team:** hdl
**type:** ingestion

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
**Source:** workflow_hdl/sharedtables-ingestion.json
