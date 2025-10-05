# Project Requirements & Context

This page documents the original requirements and context needed to adapt this agent for your specific environment.

---

## Overview

This Data Pipeline Agent was originally developed for a **real-world enterprise data platform** serving a large-scale B2B operations system. The code has been anonymized for public release, but the underlying architecture and patterns are production-tested.

---

## What Was Anonymized

To make this project publicly shareable, the following elements were replaced with generic equivalents:

### Company & Product Names

| Original (Real System) | Anonymized (Public Code) | Description |
|------------------------|--------------------------|-------------|
| AB InBev | TechCorp Inc | Company name |
| BEES Platform | DataHub | Product platform name |
| Frontline Strategy | Operations Platform | Project area |
| Force Data Platform | Platform Data Platform | System name |

### Technical System Names

| Original | Anonymized | Purpose |
|----------|------------|---------|
| HDL (High-Level Data) | DPL (Data Pipeline Layer) | Core data layer name |
| GHQ_B2B_Delta | enterprise_data_platform | Production catalog name |

### Data Entities

| Original Entity | Anonymized | Business Context |
|----------------|------------|------------------|
| Tasks | Orders | Sales representative tasks |
| Visits | Sessions | Customer visit records |
| VendorGroups | PartnerGroups | Vendor/supplier groupings |
| UserClientCatalog | UserProductCatalog | User-client product catalog |
| ActivityStaging | EventStaging | Activity staging area |
| OnTapUserVisits | UserSessions | On-premise user visit tracking |
| OfflineOrders | LocalTransactions | Offline order synchronization |
| OrdersCartSuggestion | CartRecommendations | AI-powered cart suggestions |

### Infrastructure

| Original | Anonymized | Notes |
|----------|------------|-------|
| Azure DevOps | GitHub | Repository hosting |
| Internal email domains | example.com | Contact information |
| Specific Azure regions | Generic cloud | Regional deployments |

---

## What You Need to Adapt

To make this agent work in **your environment**, you'll need to configure:

### 1. Databricks Environment

**Required**:
- Databricks workspace (AWS, Azure, or GCP)
- Unity Catalog enabled
- Databricks Model Serving endpoint for Claude or similar LLM

**Configuration**:
```python
# In your Databricks notebook or environment
DATABRICKS_HOST = "https://your-workspace.cloud.databricks.com"
DATABRICKS_TOKEN = dbutils.secrets.get(scope="your-scope", key="token")
MODEL_SERVING_ENDPOINT = "your-claude-endpoint"  # or GPT-4, Llama, etc.
```

### 2. Data Layer Architecture

The agent expects a **medallion architecture** with these layers:

```
Bronze Layer (Raw Data)
└── Streaming tables from event sources
└── Batch tables from APIs/databases

Silver Layer (Harmonized)
└── Cleaned and validated data
└── Business rules applied

Gold Layer (Analytics-Ready)
└── Aggregated metrics
└── Business KPIs
└── Sharing layer for consumption
```

**Your Equivalent**:
- Map your data layers to the expected structure
- Update catalog names in `hdl_agent_lib/knowledge/` docs
- Modify entity names in specialist tools

### 3. Data Entities

The agent knowledge base references these entity types. **Map to your entities**:

**Streaming Entities** (Real-time event processing):
- User activity events
- Transaction events
- Sensor/IoT data
- Application logs

**Batch Entities** (Scheduled processing):
- Master data (products, customers, vendors)
- Historical transactions
- Reference data
- External API data

**Example Mapping**:
```yaml
# Your entities → Agent entities
your_sales_orders: Orders
your_customer_visits: Sessions
your_supplier_groups: PartnerGroups
your_product_catalog: UserProductCatalog
```

### 4. Workflow Patterns

The agent understands **Databricks Workflows** with:

**Streaming Workflows**:
- Event Hub / Kafka source
- Auto Loader ingestion
- Bronze → Silver pipelines
- File arrival triggers

**Batch Workflows**:
- Scheduled CRON execution
- MongoDB/CosmosDB sources
- Bronze → Silver → Gold pipelines
- Dependency management

**Your Equivalent**:
- Document your workflow JSONs in `workflow_hdl/`
- Update workflow names and triggers
- Adjust task dependencies

### 5. Secret Management

The agent expects secrets in **Databricks Secret Scopes**:

```python
# Default pattern
scope_name = "your-secret-scope"
api_key = dbutils.secrets.get(scope=scope_name, key="api-key")
db_password = dbutils.secrets.get(scope=scope_name, key="db-password")
```

**Your Setup**:
```bash
# Create secret scope
databricks secrets create-scope --scope your-secret-scope

# Add secrets
databricks secrets put --scope your-secret-scope --key api-key
databricks secrets put --scope your-secret-scope --key db-password
```

### 6. RAG Knowledge Base

The agent uses **ChromaDB** for RAG. You need to:

1. **Update Knowledge Base**:
   - Edit files in `hdl_agent_lib/knowledge/`
   - Replace generic workflows with your actual workflows
   - Document your data entities and pipelines

2. **Load Knowledge**:
   ```bash
   python scripts/load_knowledge_base.py
   ```

3. **Embeddings**:
   - Default: OpenAI embeddings (requires API key)
   - Alternative: Databricks embeddings, local models, etc.

**Configuration**:
```python
# Option 1: OpenAI embeddings (default)
OPENAI_API_KEY = "your-key"

# Option 2: Databricks embeddings
from databricks_genai import embeddings
embeddings_model = embeddings.get_model("your-embedding-model")

# Option 3: Local embeddings (sentence-transformers)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
```

---

## Real-World Context

### Original Use Case

The agent was built for a **global B2B beverage distribution platform** serving:
- 50,000+ sales representatives
- 1M+ customers
- 13 streaming pipelines (real-time)
- 13 batch pipelines (scheduled)
- Processing 500GB+ daily data

### Problems It Solves

1. **Pipeline Troubleshooting**: Diagnose streaming/batch failures
2. **Performance Optimization**: Identify bottlenecks, suggest improvements
3. **Quality Assurance**: Validate data completeness, detect anomalies
4. **Ecosystem Navigation**: Understand dependencies, workflows
5. **Operational Support**: Fix bugs, coordinate reprocessing

### Production Patterns

**What Works**:
- RAG for workflow-specific knowledge
- Specialist tools for focused tasks
- LangGraph for complex orchestration
- Clean Architecture for maintainability

**What to Adapt**:
- Entity names and business logic
- Workflow structures and dependencies
- Error patterns and alerting
- Integration points and APIs

---

## Minimal Working Example

To get the agent working with **minimal changes**:

### Step 1: Environment Setup

```bash
# Clone and setup
git clone https://github.com/your-username/data-pipeline-agent
cd data-pipeline-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Configure Credentials

```bash
# Create .env file
cat > .env << EOF
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your-token
MODEL_SERVING_ENDPOINT=your-claude-endpoint
OPENAI_API_KEY=your-openai-key  # Optional, for RAG embeddings
EOF
```

### Step 3: Update Knowledge Base

```bash
# Edit your workflows
vim hdl_agent_lib/knowledge/workflows/streaming/your-pipeline.md
vim hdl_agent_lib/knowledge/workflows/batch/your-batch-job.md

# Load into vector store
python scripts/load_knowledge_base.py
```

### Step 4: Test Locally

```python
# test_local.py
from dpl_agent_lib.specialists import diagnose_pipeline_error

result = diagnose_pipeline_error(
    error_message="Your actual error message",
    pipeline_name="your-pipeline-name",
    context="Additional context about the failure"
)

print(result)
```

### Step 5: Deploy to Databricks

```python
# Upload wheel package
databricks fs cp dist/dpl_agent_lib-3.1.0-py3-none-any.whl dbfs:/FileStore/wheels/

# Install in cluster
%pip install /dbfs/FileStore/wheels/dpl_agent_lib-3.1.0-py3-none-any.whl

# Use in notebook
from dpl_agent_lib.specialists import *
result = diagnose_pipeline_error(...)
```

---

## Custom Integration Guide

### For Your Specific Environment

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/data-pipeline-agent
   cd data-pipeline-agent
   ```

2. **Global Find & Replace**
   ```bash
   # Replace generic names with your actual names
   find . -type f -name "*.py" -exec sed -i 's/DataHub/YourPlatform/g' {} +
   find . -type f -name "*.md" -exec sed -i 's/DPL/YourDataLayer/g' {} +
   ```

3. **Update Entity Mappings**
   ```python
   # In dpl_agent_lib/domain/entities/
   # Rename or extend entity classes to match your data model
   ```

4. **Document Your Workflows**
   ```bash
   # Copy your workflow JSONs
   cp /path/to/your/workflows/*.json workflow_hdl/
   
   # Generate documentation
   python scripts/generate_workflow_docs.py
   ```

5. **Customize Specialists**
   ```python
   # In dpl_agent_lib/specialists/
   # Adjust error patterns, validation rules, and business logic
   ```

6. **Rebuild Package**
   ```bash
   python setup.py bdist_wheel
   ```

---

## FAQ

### Q: Do I need the exact same data structure?

**A**: No. The agent is flexible. Just update the entity names and knowledge base to match your structure.

### Q: Can I use a different LLM?

**A**: Yes. The agent supports any LLM accessible via Databricks Model Serving or LangChain integrations (OpenAI, Anthropic, Azure, etc.).

### Q: What if I don't use Databricks?

**A**: The core specialist tools work anywhere. You'll need to adapt:
- LLM integration (replace `databricks_claude.py`)
- Secret management (replace `dbutils.secrets`)
- Deployment strategy (Docker, Kubernetes, etc.)

### Q: How much effort to adapt?

**A**: Depends on similarity to original system:
- **Similar architecture**: 1-2 days (update names, knowledge base)
- **Different architecture**: 1-2 weeks (restructure entities, workflows)
- **Complete rewrite**: Use as reference architecture only

### Q: Is the anonymization reversible?

**A**: No. All company-specific details were permanently removed. You'll configure YOUR environment.

---

## Support

For questions about adapting this to your environment:

1. **GitHub Issues**: Technical questions and bugs
2. **GitHub Discussions**: Architecture and design questions
3. **Documentation**: Read through all docs in `docs/` folder

---

## License

This project is open-source under MIT License. You're free to adapt it for any purpose, commercial or non-commercial.

---

**Last Updated**: October 5, 2025  
**Version**: 3.1.0

