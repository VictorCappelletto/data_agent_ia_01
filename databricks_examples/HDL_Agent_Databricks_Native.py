# Databricks notebook source
# MAGIC %md
# MAGIC # DPL Agent - Databricks Native Deployment
# MAGIC
# MAGIC Production-ready DPL Agent using Databricks Serving Endpoints (Claude).
# MAGIC No external API keys required - uses Databricks-managed LLM endpoints.
# MAGIC
# MAGIC **Features:**
# MAGIC - Databricks Claude integration (no API keys)
# MAGIC - RAG-enhanced specialists with knowledge base
# MAGIC - Full DPL troubleshooting, optimization, coordination
# MAGIC - Production logging and monitoring

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Install DPL Agent Library

# COMMAND ----------

# Install from .whl package
!pip install /dbfs/FileStore/shared_uploads/data_pipeline_agent_lib-3.0.0-py3-none-any.whl --quiet

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Initialize Agent with Databricks Claude

# COMMAND ----------

from data_pipeline_agent_lib.infrastructure.llm import create_databricks_claude
from data_pipeline_agent_lib.application.services import get_hdl_retriever_service
from data_pipeline_agent_lib.specialists import (
    troubleshoot_hdl_error,
    resolve_hdl_bug,
    analyze_pipeline_performance,
)

# Initialize Databricks Claude provider
llm = create_databricks_claude(
    endpoint_name="databricks-claude-sonnet-4",
    temperature=0.1
)

print("Databricks Claude Status:")
status = llm.get_status()
for key, value in status.items():
    print(f"  {key}: {value}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Test RAG Service

# COMMAND ----------

# Initialize RAG service (loads knowledge base automatically)
rag_service = get_hdl_retriever_service()

# Test semantic search
results = rag_service.search_workflow_knowledge("dpl-stream-visits timeout")

print("RAG Search Results:")
print(f"Found {len(results)} relevant documents")
for i, result in enumerate(results[:3], 1):
    print(f"\n{i}. {result.metadata.get('source', 'Unknown')}")
    print(f"   Content: {result.page_content[:150]}...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Troubleshoot DPL Error

# COMMAND ----------

# Real-world troubleshooting scenario
error_response = troubleshoot_hdl_error.invoke(
    "Timeout error in dpl-stream-visits pipeline after 90 minutes | entity: visits | type: streaming"
)

print("Troubleshooting Response:")
print(error_response)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Analyze Pipeline Performance

# COMMAND ----------

performance_response = analyze_pipeline_performance.invoke(
    "dpl-ingestion-Orders pipeline taking 2 hours | entity: Orders | type: batch"
)

print("Performance Analysis:")
print(performance_response)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Bug Resolution

# COMMAND ----------

bug_response = resolve_hdl_bug.invoke(
    "SCD2 merge producing duplicate records in Orders silver table | entity: tasks"
)

print("Bug Resolution:")
print(bug_response)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Custom Query with Claude

# COMMAND ----------

# Direct LLM query for complex questions
custom_query = """
I need to understand the difference between streaming and batch workflows in DPL.
Specifically:
1. When to use each approach?
2. What are the key architectural differences?
3. How do they handle data freshness?
"""

response = llm.generate(
    prompt=custom_query,
    system_prompt="You are an DPL specialist. Provide technical, specific answers based on DPL architecture."
)

print("Claude Response:")
print(response)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Conversational Mode

# COMMAND ----------

# Multi-turn conversation
messages = [
    {"role": "user", "content": "What's the best way to debug a timeout in dpl-stream-tasks?"},
]

response = llm.chat(messages)
print("Response:", response)

# Continue conversation
messages.append({"role": "assistant", "content": response})
messages.append({"role": "user", "content": "What tools should I use?"})

response = llm.chat(messages)
print("\nFollow-up Response:", response)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Production Monitoring

# COMMAND ----------

# Check system health
print("DPL Agent System Status:")
print("-" * 50)
print(f"LLM Provider: {status['provider']}")
print(f"Endpoint: {status['endpoint']}")
print(f"Connected: {status['connected']}")
print(f"Features: {', '.join(status['features'])}")

# RAG service stats
print("\nRAG Service Status:")
print(f"Knowledge documents loaded: {len(rag_service._vector_store._collection.get()['ids']) if hasattr(rag_service, '_vector_store') else 'N/A'}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC
# MAGIC DPL Agent deployed successfully in Databricks with:
# MAGIC - Databricks Claude integration (no API keys)
# MAGIC - RAG-enhanced knowledge retrieval
# MAGIC - 7 specialized tools for DPL operations
# MAGIC - Production-ready logging and monitoring
# MAGIC
# MAGIC **Next Steps:**
# MAGIC - Configure Databricks secrets if needed
# MAGIC - Set up monitoring dashboards
# MAGIC - Schedule agent for automated workflows

