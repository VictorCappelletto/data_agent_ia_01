# Production Deployment Guide

**Package:** `data_pipeline_agent_lib-3.0.0-py3-none-any.whl` 
**Target:** Databricks Clusters 
**Status:** Production Ready

---

## Pre-Deployment Checklist

### Quality Validation 
- [x] All unit tests passing (113/113)
- [x] Code coverage acceptable (51%)
- [x] Specialists thoroughly tested (91%)
- [x] No emojis in output
- [x] Clean Architecture validated
- [x] Package built successfully

### Required Permissions
- [ ] DBFS write access
- [ ] Cluster library install permissions
- [ ] Secret scope read access (for API keys)
- [ ] Workspace admin approval (if needed)

---

## Deployment Steps

### Step 1: Upload Package to DBFS

#### Option A: Using Databricks CLI
```bash
# Install Databricks CLI (if not already installed)
pip install databricks-cli

# Configure authentication
databricks configure --token

# Upload .whl to DBFS
databricks fs cp \
dist/data_pipeline_agent_lib-3.0.0-py3-none-any.whl \
dbfs:/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
```

#### Option B: Using Databricks UI
1. Navigate to **Data** → **DBFS** → **FileStore**
2. Create folder: `libraries/` (if not exists)
3. Click **Upload**
4. Select: `data_pipeline_agent_lib-3.0.0-py3-none-any.whl`
5. Confirm upload

#### Option C: Using Python API
```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Upload file
with open("dist/data_pipeline_agent_lib-3.0.0-py3-none-any.whl", "rb") as f:
w.dbfs.upload(
"/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl",
f.read()
)
```

---

### Step 2: Install on Databricks Cluster

#### Option A: Install via Cluster UI
1. Navigate to **Compute** → Select your cluster
2. Click **Libraries** tab
3. Click **Install new**
4. Select **Library Source:** "DBFS/ADLS"
5. Select **Library Type:** "Python Whl"
6. Enter path: `dbfs:/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl`
7. Click **Install**
8. Wait for status: **Installed**

#### Option B: Install via Notebook
```python
# Install the library
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl

# Restart Python kernel to use the library
dbutils.library.restartPython()
```

#### Option C: Install via Cluster Init Script
Create file: `dbfs:/databricks/init-scripts/install-hdl-agent.sh`
```bash
#!/bin/bash
/databricks/python/bin/pip install \
/dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
```

Add to cluster configuration:
- **Cluster** → **Advanced Options** → **Init Scripts**
- Add path: `dbfs:/databricks/init-scripts/install-hdl-agent.sh`

---

### Step 3: Configure API Keys (Secure)

#### Create Secret Scope (One-Time Setup)
```bash
# Using Databricks CLI
databricks secrets create-scope --scope hdl-agent-secrets

# Add Anthropic API Key
databricks secrets put-secret \
--scope hdl-agent-secrets \
--key anthropic-api-key \
--string-value "sk-ant-api03-your-key-here"
```

#### Access Secrets in Notebook
```python
# Retrieve API key from secret scope
anthropic_api_key = dbutils.secrets.get(
scope="hdl-agent-secrets",
key="anthropic-api-key"
)

# Set environment variable
import os
os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
```

---

### Step 4: Validate Installation

#### Test 1: Import Package
```python
# Test basic import
try:
import data_pipeline_agent_lib
print(" Package imported successfully")
print(f"Version: {data_pipeline_agent_lib.__version__}")
except ImportError as e:
print(f" Import failed: {e}")
```

#### Test 2: Test Specialists (No API Required)
```python
from data_pipeline_agent_lib.specialists import (
troubleshoot_hdl_error,
resolve_hdl_bug,
optimize_hdl_pipeline
)

# Test troubleshooter
result = troubleshoot_hdl_error("Test timeout error in streaming pipeline")
print(" Troubleshooter working:")
print(result[:200])

# Test bug resolver
result = resolve_hdl_bug("SCD2 is_current corruption issue")
print("\n Bug Resolver working:")
print(result[:200])

# Test performance advisor
result = optimize_hdl_pipeline("Slow batch pipeline taking 2 hours")
print("\n Performance Advisor working:")
print(result[:200])
```

#### Test 3: Test Full Agent (Requires API)
```python
import os
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph, create_initial_state
from data_pipeline_agent_lib.utils import create_conversation_config

# Set API key (from secrets)
os.environ["ANTHROPIC_API_KEY"] = dbutils.secrets.get(
scope="hdl-agent-secrets",
key="anthropic-api-key"
)

# Create agent
graph = create_data_pipeline_agent_graph()
config = create_conversation_config("test_session")

# Test query
query = "What is the bronze layer in DPL?"
state = create_initial_state(query)

# Execute
result = graph.invoke(state, config)
print(" Full agent working:")
print(result["final_response"])
```

---

## Security Best Practices

### API Key Management
- **Never hardcode** API keys in notebooks
- **Always use** Databricks secrets
- **Restrict access** to secret scopes
- **Rotate keys** regularly
- **Monitor usage** for anomalies

### Secret Scope Permissions
```bash
# Grant read access to specific users
databricks secrets put-acl \
--scope hdl-agent-secrets \
--principal user@company.com \
--permission READ

# List permissions
databricks secrets list-acl --scope hdl-agent-secrets
```

---

## Monitoring & Observability

### Log Monitoring
```python
from data_pipeline_agent_lib.utils import get_logger, setup_logging

# Configure logging for production
setup_logging(level="INFO", format_type="json")

# Use logger in your code
logger = get_logger(__name__)
logger.info("Agent query started", query=query, session_id=session_id)
```

### Performance Tracking
```python
import time
from datetime import datetime

def track_agent_performance(query: str):
"""Track agent query performance."""
start_time = datetime.utcnow()

try:
# Execute agent
result = graph.invoke(state, config)

# Log success
duration = (datetime.utcnow() - start_time).total_seconds()
logger.info(
"Agent query completed",
query=query,
duration_seconds=duration,
response_length=len(result["final_response"]),
status="success"
)

return result

except Exception as e:
# Log failure
duration = (datetime.utcnow() - start_time).total_seconds()
logger.error(
"Agent query failed",
query=query,
duration_seconds=duration,
error=str(e),
status="failure"
)
raise
```

### Cost Tracking
```python
def estimate_token_cost(input_text: str, output_text: str):
"""Estimate cost of LLM call."""
# Rough estimation: ~4 chars per token
input_tokens = len(input_text) / 4
output_tokens = len(output_text) / 4

# Claude 3.5 Sonnet pricing (example)
input_cost_per_1k = 0.003 # $3 per 1M tokens
output_cost_per_1k = 0.015 # $15 per 1M tokens

cost = (input_tokens / 1000 * input_cost_per_1k +
output_tokens / 1000 * output_cost_per_1k)

logger.info(
"LLM cost estimated",
input_tokens=input_tokens,
output_tokens=output_tokens,
estimated_cost_usd=cost
)

return cost
```

---

## Troubleshooting

### Issue 1: Import Errors
**Symptom:** `ModuleNotFoundError: No module named 'data_pipeline_agent_lib'`

**Solutions:**
```python
# 1. Verify installation
%pip list | grep hdl-agent

# 2. Reinstall
%pip install --Platform-reinstall \
/dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl

# 3. Restart Python
dbutils.library.restartPython()
```

### Issue 2: API Key Not Found
**Symptom:** `KeyError: 'ANTHROPIC_API_KEY'`

**Solutions:**
```python
# 1. Verify secret scope exists
try:
api_key = dbutils.secrets.get("hdl-agent-secrets", "anthropic-api-key")
print(" API key retrieved")
except Exception as e:
print(f" Failed to get API key: {e}")

# 2. Check permissions
# Contact workspace admin to grant READ access

# 3. Verify environment variable
import os
print(f"ANTHROPIC_API_KEY set: {'ANTHROPIC_API_KEY' in os.environ}")
```

### Issue 3: Agent Timeouts
**Symptom:** `TimeoutError` during agent execution

**Solutions:**
```python
# 1. Increase timeout for LLM calls
from data_pipeline_agent_lib.infrastructure.llm import AnthropicLLMProvider

llm = AnthropicLLMProvider(
model_name="claude-3-5-sonnet-20241022",
temperature=0.7,
max_tokens=4000,
timeout=120 # Increase timeout to 120 seconds
)

# 2. Check network connectivity
import requests
try:
response = requests.get("https://api.anthropic.com", timeout=10)
print(f" Anthropic API reachable: {response.status_code}")
except Exception as e:
print(f" Network issue: {e}")
```

### Issue 4: Vector Store Errors
**Symptom:** ChromaDB initialization failures

**Solutions:**
```python
# 1. Verify ChromaDB path
import os
chroma_path = "/dbfs/FileStore/chroma_db"
os.makedirs(chroma_path, exist_ok=True)

# 2. Initialize with explicit path
from data_pipeline_agent_lib.infrastructure.vector_store import ChromaVectorStore

vector_store = ChromaVectorStore(
collection_name="hdl_knowledge",
persist_directory=chroma_path
)
```

---

## Performance Optimization

### Caching Strategies
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_agent_response(query: str):
"""Cache agent responses for common queries."""
state = create_initial_state(query)
result = graph.invoke(state, config)
return result["final_response"]
```

### Batch Processing
```python
def process_queries_batch(queries: list[str], batch_size: int = 10):
"""Process multiple queries in batches."""
results = []

for i in range(0, len(queries), batch_size):
batch = queries[i:i+batch_size]

# Process batch
batch_results = [
graph.invoke(create_initial_state(q), config)
for q in batch
]

results.extend(batch_results)

# Log progress
logger.info(
"Batch processed",
batch_num=i//batch_size + 1,
queries_processed=len(results)
)

return results
```

---

## Rollback Procedure

### If Issues Arise

#### Step 1: Uninstall Current Version
```python
%pip uninstall -y hdl-agent-lib
dbutils.library.restartPython()
```

#### Step 2: Install Previous Version (if available)
```python
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-2.0.0-py3-none-any.whl
dbutils.library.restartPython()
```

#### Step 3: Verify Rollback
```python
import data_pipeline_agent_lib
print(f"Rolled back to version: {data_pipeline_agent_lib.__version__}")
```

---

## Post-Deployment Checklist

### Validation
- [ ] Package installed on all target clusters
- [ ] API keys configured in secret scope
- [ ] Specialists tested (no API)
- [ ] Full agent tested (with API)
- [ ] Logging configured
- [ ] Monitoring dashboard updated

### Documentation
- [ ] Deployment documented
- [ ] Team notified of new version
- [ ] User guide updated
- [ ] Known issues documented

### Operations
- [ ] Support team briefed
- [ ] Runbook updated
- [ ] Escalation procedures reviewed
- [ ] Backup/rollback plan validated

---

## Support & Escalation

### For Issues Contact:
- **Technical Lead:** Victor Cappelleto
- **Databricks Admin:** [Admin contact]
- **Azure DevOps:** [Team channel]

### Escalation Path:
1. Check troubleshooting section above
2. Review agent logs in Databricks
3. Check Azure DevOps for known issues
4. Contact technical lead
5. Create incident ticket if needed

---

## Success Criteria

Deployment is successful when:
- Package installed without errors
- All 7 specialists functional
- Full agent responds to queries
- No emoji in output
- Logging working correctly
- API keys secure
- Performance acceptable (<5s per query)

---

**Deployment Status:** Ready for Production 
**Last Updated:** 2025-10-04 
**Version:** 3.0.0

