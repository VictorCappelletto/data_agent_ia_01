# Databricks notebook source
# MAGIC %md
# MAGIC # DPL Agent v3.0 - Quick Start
# MAGIC 
# MAGIC **Version**: 3.0.0  
# MAGIC **Purpose**: DPL pipeline troubleshooting, optimization, and management
# MAGIC 
# MAGIC ## Installation
# MAGIC 
# MAGIC ```python
# MAGIC %pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
# MAGIC dbutils.library.restartPython()
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## API Configuration
# MAGIC 
# MAGIC **Specialists**: No API key required  
# MAGIC **Full Agent**: Requires Anthropic API key

# COMMAND ----------

import os

# Load API keys from Databricks Secrets (recommended)
try:
    os.environ["ANTHROPIC_API_KEY"] = dbutils.secrets.get("hdl-agent-secrets", "anthropic-api-key")
    print("API keys configured from secrets")
except Exception as e:
    print(f"Warning: API keys not configured - {e}")
    print("Specialists will work without API keys")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import Specialists

# COMMAND ----------

from data_pipeline_agent_lib.specialists import (
    troubleshoot_hdl_error,
    resolve_hdl_bug,
    optimize_hdl_pipeline,
    validate_hdl_data_quality,
    execute_hdl_workflow,
    get_workflow_status,
    explain_hdl_component,
    get_hdl_best_practices,
    coordinate_hdl_reprocessing,
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Troubleshooting Examples

# COMMAND ----------

# Example 1: Pipeline timeout
result = troubleshoot_hdl_error(
    "Sessions streaming pipeline dpl-stream-visits timed out after 90 minutes"
)
print(result)

# COMMAND ----------

# Example 2: SCD2 bug
resolution = resolve_hdl_bug(
    "SCD2 is_current column has incorrect values in silver layer"
)
print(resolution)

# COMMAND ----------

# Example 3: Urgent reprocessing
plan = coordinate_hdl_reprocessing(
    "URGENT: Reprocess tasks entity for October 4th. Client waiting. Notify KPI team."
)
print(plan)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Optimization & Quality Examples

# COMMAND ----------

# Example 4: Performance optimization
optimization = optimize_hdl_pipeline(
    "dpl-ingestion-Orders batch pipeline running slow - 3 hours instead of 30 minutes"
)
print(optimization)

# COMMAND ----------

# Example 5: Data quality validation
quality = validate_hdl_data_quality(
    "Check completeness and consistency for visits entity in silver layer"
)
print(quality)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Operations Examples

# COMMAND ----------

# Example 6: Execute workflow
execution = execute_hdl_workflow(
    "dpl-stream-visits in production environment"
)
print(execution)

# COMMAND ----------

# Example 7: Workflow status
status = get_workflow_status("dpl-stream-visits")
print(status)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Documentation Examples

# COMMAND ----------

# Example 8: Component explanation
explanation = explain_hdl_component("SCD2 merge process")
print(explanation)

# COMMAND ----------

# Example 9: Best practices
practices = get_hdl_best_practices("streaming pipeline optimization")
print(practices)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Full Agent (Requires API Key)

# COMMAND ----------

if os.getenv("ANTHROPIC_API_KEY"):
    from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph, create_initial_state
    from data_pipeline_agent_lib.utils import create_conversation_config
    
    # Create agent
    graph = create_data_pipeline_agent_graph()
    config = create_conversation_config("databricks_session")
    
    print("Agent initialized successfully")
else:
    print("API key not configured - using specialists only")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Single Query Example

# COMMAND ----------

if os.getenv("ANTHROPIC_API_KEY"):
    query = "What is the bronze layer in DPL architecture?"
    state = create_initial_state(query)
    result = graph.invoke(state, config)
    
    print("QUERY:", query)
    print("\nRESPONSE:")
    print(result["final_response"])

# COMMAND ----------

# MAGIC %md
# MAGIC ### Multi-Turn Conversation

# COMMAND ----------

if os.getenv("ANTHROPIC_API_KEY"):
    # Turn 1
    state1 = create_initial_state("Explain streaming pipelines in DPL")
    result1 = graph.invoke(state1, config)
    print("TURN 1:", result1["final_response"][:200] + "...")
    
    # Turn 2 (with memory)
    state2 = create_initial_state("What about batch pipelines?")
    state2["messages"] = result1["messages"]
    result2 = graph.invoke(state2, config)
    print("\nTURN 2:", result2["final_response"][:200] + "...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Available Tools

# COMMAND ----------

from data_pipeline_agent_lib.specialists import ALL_DPL_TOOLS

print(f"Total Specialist Tools: {len(ALL_DPL_TOOLS)}\n")

for i, tool in enumerate(ALL_DPL_TOOLS, 1):
    print(f"{i}. {tool.name}")
    print(f"   {tool.description[:80]}...\n")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validation

# COMMAND ----------

import sys

print("DPL Agent v3.0 - Validation")
print("=" * 60)

# Test imports
try:
    from data_pipeline_agent_lib.domain import Environment, PipelineType
    from data_pipeline_agent_lib.specialists import ALL_DPL_TOOLS
    from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph
    
    print("Domain layer: OK")
    print(f"Specialists: OK ({len(ALL_DPL_TOOLS)} tools)")
    print("Agent orchestration: OK")
    print(f"\nPython version: {sys.version.split()[0]}")
    print("Status: Ready")
    
except ImportError as e:
    print(f"Import failed: {e}")
    print("\nEnsure:")
    print("  1. Library installed correctly")
    print("  2. Cluster restarted after installation")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next Steps
# MAGIC 
# MAGIC 1. Test specialists with your DPL scenarios
# MAGIC 2. Configure API keys for full agent features
# MAGIC 3. Integrate with production workflows
# MAGIC 4. See documentation: docs/deployment/production-deployment.md
# MAGIC 
# MAGIC ---
# MAGIC 
# MAGIC **Last Updated**: 2025-10-04

