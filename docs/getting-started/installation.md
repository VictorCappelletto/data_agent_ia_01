# Installation

Setup instructions for DPL Agent v3.0 in Databricks and local environments.

---

## Requirements

- **Python**: 3.9 or higher
- **Platform**: Databricks (primary) or local development
- **Memory**: Minimum 2GB RAM
- **Storage**: ~100MB for package and dependencies

---

## Databricks Installation

### Step 1: Upload Package to DBFS

**Option A: Databricks UI**
1. Navigate to **Data** → **DBFS** → **FileStore** → **libraries**
2. Click **Upload** and select `data_pipeline_agent_lib-3.0.0-py3-none-any.whl`
3. Wait for upload confirmation

**Option B: Databricks CLI**
```bash
databricks fs cp \
  dist/data_pipeline_agent_lib-3.0.0-py3-none-any.whl \
  dbfs:/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
```

### Step 2: Install on Cluster

**Option A: Cluster UI**
1. Navigate to **Compute** → Select cluster
2. Click **Libraries** tab → **Install new**
3. Select **DBFS/ADLS** → **Python Whl**
4. Path: `dbfs:/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl`
5. Click **Install** and wait for green checkmark

**Option B: Notebook**
```python
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
dbutils.library.restartPython()
```

### Step 3: Verify Installation

```python
import data_pipeline_agent_lib
from data_pipeline_agent_lib.specialists import ALL_DPL_TOOLS

print(f"DPL Agent v{data_pipeline_agent_lib.__version__}")
print(f"{len(ALL_DPL_TOOLS)} specialist tools available")
```

---

## API Key Configuration

### Databricks (Recommended)

**Create Secret Scope**:
```bash
databricks secrets create-scope --scope hdl-agent-secrets
```

**Add API Key**:
```bash
databricks secrets put-secret \
  --scope hdl-agent-secrets \
  --key anthropic-api-key \
  --string-value "sk-ant-api03-your-key-here"
```

**Use in Notebook**:
```python
import os

api_key = dbutils.secrets.get(
    scope="hdl-agent-secrets",
    key="anthropic-api-key"
)
os.environ["ANTHROPIC_API_KEY"] = api_key
```

### Local Development

**Create `.env` file**:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
OPENAI_API_KEY=sk-your-openai-key-optional
LOG_LEVEL=INFO
```

**Load in Python**:
```python
from dotenv import load_dotenv
import os

load_dotenv()
print(f"API Key set: {'ANTHROPIC_API_KEY' in os.environ}")
```

---

## Local Installation

### Install from Wheel
```bash
pip install dist/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
python -c "import data_pipeline_agent_lib; print(data_pipeline_agent_lib.__version__)"
```

### Development Setup
```bash
# Clone repository
git clone [repository-url]
cd data_pipeline_agent

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install in editable mode
pip install -e .
pip install -r requirements-dev.txt
```

---

## Verification

```python
# Test imports
from data_pipeline_agent_lib.specialists import (
    troubleshoot_hdl_error,
    resolve_hdl_bug,
    optimize_hdl_pipeline
)

# Test specialist (no API required)
result = troubleshoot_hdl_error("Test error message")
print("Installation successful!")
print(f"Sample output: {result[:100]}...")
```

---

## Troubleshooting

### ModuleNotFoundError
```python
# Restart kernel
dbutils.library.restartPython()

# Verify installation
%pip list | grep hdl-agent

# Reinstall if needed
%pip install --Platform-reinstall /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
```

### Dependency Conflicts
```python
# Install with no-deps flag
%pip install --no-deps /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl

# Install critical dependencies manually
%pip install langchain langgraph pydantic

# Restart
dbutils.library.restartPython()
```

### DBFS Path Not Found
```bash
# Verify file exists
databricks fs ls dbfs:/FileStore/libraries/

# Re-upload if needed
databricks fs cp dist/data_pipeline_agent_lib-3.0.0-py3-none-any.whl dbfs:/FileStore/libraries/
```

### API Key Issues
```python
# Verify secret exists
key = dbutils.secrets.get("hdl-agent-secrets", "anthropic-api-key")
print(f"Secret retrieved (length: {len(key)})")

# Check environment variable
import os
print(f"Env var set: {'ANTHROPIC_API_KEY' in os.environ}")
```

---

## Upgrade from v2.0

```python
# Uninstall old version
%pip uninstall -y hdl-agent-lib

# Install new version
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl

# Restart and verify
dbutils.library.restartPython()
```

**Breaking Changes**:
- New Clean Architecture structure
- API signature changes for specialists
- LangGraph orchestration replaces simple chains

---

## Next Steps

1. [Quick Start Guide](../deployment/quickstart.md)
2. [Configuration Reference](configuration.md)
3. [Specialists Overview](../specialists/overview.md)
4. [Code Examples](../examples/basic.md)

---

**Last Updated**: 2025-10-04
