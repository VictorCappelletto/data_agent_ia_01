"""
DPL Agent v3.0 - Databricks Notebook Example
Example of using DPL Agent in Databricks notebook after installing the wheel
"""

# COMMAND ----------
# MAGIC %md
# MAGIC # DPL Agent v3.0 - Databricks Integration
# MAGIC 
# MAGIC This notebook demonstrates how to use DPL Agent in Databricks after installing the wheel package.
# MAGIC 
# MAGIC **Prerequisites:**
# MAGIC 1. Install `hdl-agent-lib-3.0.0-py3-none-any.whl` in cluster libraries
# MAGIC 2. Restart cluster
# MAGIC 3. Configure environment variables (secrets)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Setup & Configuration

# COMMAND ----------

# Import DPL Agent
from data_pipeline_agent_lib import create_data_pipeline_agent_graph

# Optional: Configure logging
import logging
logging.basicConfig(level=logging.INFO)

print("✅ DPL Agent library imported successfully!")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Initialize Agent

# COMMAND ----------

# Create agent instance
agent = create_data_pipeline_agent_graph()

print("✅ DPL Agent initialized and ready!")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Basic Query Example

# COMMAND ----------

# Simple query
query = "What is the DPL architecture?"

result = agent.invoke({
    "messages": [{"role": "user", "content": query}]
})

# Display response
response = result["messages"][-1]["content"]
print(f"Query: {query}\n")
print(f"Response:\n{response}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Troubleshooting Example

# COMMAND ----------

# Troubleshooting query
troubleshoot_query = "Why might the visits streaming pipeline fail?"

result = agent.invoke({
    "messages": [{"role": "user", "content": troubleshoot_query}]
})

response = result["messages"][-1]["content"]
print(f"Query: {troubleshoot_query}\n")
print(f"Response:\n{response}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Performance Optimization Example

# COMMAND ----------

# Optimization query
optimization_query = "How can I optimize the tasks batch pipeline?"

result = agent.invoke({
    "messages": [{"role": "user", "content": optimization_query}]
})

response = result["messages"][-1]["content"]
print(f"Query: {optimization_query}\n")
print(f"Response:\n{response}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 6. Data Quality Check Example

# COMMAND ----------

# Data quality query
quality_query = "What data quality checks should I implement for DPL?"

result = agent.invoke({
    "messages": [{"role": "user", "content": quality_query}]
})

response = result["messages"][-1]["content"]
print(f"Query: {quality_query}\n")
print(f"Response:\n{response}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 7. Workflow Status Check Example

# COMMAND ----------

# Workflow status query (will use Databricks integration)
workflow_query = "Check the status of DPL workflows"

result = agent.invoke({
    "messages": [{"role": "user", "content": workflow_query}]
})

response = result["messages"][-1]["content"]
print(f"Query: {workflow_query}\n")
print(f"Response:\n{response}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 8. Multi-turn Conversation Example

# COMMAND ----------

# Configure conversation with thread_id
config = {"configurable": {"thread_id": "databricks-session-001"}}

# First question
result1 = agent.invoke(
    {"messages": [{"role": "user", "content": "What are DPL specialists?"}]},
    config=config
)
print("Q1: What are DPL specialists?")
print(f"A1: {result1['messages'][-1]['content']}\n")

# Follow-up question (uses conversation context)
result2 = agent.invoke(
    {"messages": [{"role": "user", "content": "Which one handles performance?"}]},
    config=config
)
print("Q2: Which one handles performance?")
print(f"A2: {result2['messages'][-1]['content']}\n")

# Another follow-up
result3 = agent.invoke(
    {"messages": [{"role": "user", "content": "Give me an example of its usage"}]},
    config=config
)
print("Q3: Give me an example of its usage")
print(f"A3: {result3['messages'][-1]['content']}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 9. Batch Processing Example

# COMMAND ----------

# Process multiple queries in batch
queries = [
    "What is SCD2?",
    "Explain streaming vs batch",
    "List DPL monitoring tools"
]

results = []
for query in queries:
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    results.append({
        "query": query,
        "response": result["messages"][-1]["content"]
    })

# Display results
for i, item in enumerate(results, 1):
    print(f"\n{'=' * 50}")
    print(f"Query {i}: {item['query']}")
    print("=" * 50)
    print(f"Response:\n{item['response']}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 10. Error Handling Example

# COMMAND ----------

try:
    # Query that might fail
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Debug non-existent pipeline"}]
    })
    
    response = result["messages"][-1]["content"]
    print(f"Response:\n{response}")
    
except Exception as e:
    print(f"❌ Error occurred: {e}")
    print("⚠️  Check agent configuration and API keys")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Summary
# MAGIC 
# MAGIC This notebook demonstrated:
# MAGIC - ✅ Agent initialization in Databricks
# MAGIC - ✅ Basic queries
# MAGIC - ✅ Troubleshooting scenarios
# MAGIC - ✅ Performance optimization
# MAGIC - ✅ Data quality checks
# MAGIC - ✅ Multi-turn conversations
# MAGIC - ✅ Batch processing
# MAGIC - ✅ Error handling
# MAGIC 
# MAGIC For more examples, see the DPL Agent documentation.

