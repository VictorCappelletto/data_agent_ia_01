"""
DPL Agent v3.0 - Tools Integration with LangGraph

Integrates DPL specialist tools into the LangGraph workflow.
Provides tool calling nodes and routing logic.
"""

from typing import Dict, Any, List
from langchain.schema import AIMessage

from .state import AgentState
from ..specialists import (
    ALL_DPL_TOOLS,
    get_tools_for_intent,
    get_tool_descriptions,
)


# ============================================================================
# TOOL DECISION NODE
# ============================================================================

async def decide_tools_node(state: AgentState) -> Dict[str, Any]:
    """
    Decide which tools to call based on intent and query.
    
    Args:
        state: Current agent state
        
    Returns:
        State updates with tools_to_call
    """
    intent = state.get("intent", "general")
    query = state["query"]
    query_lower = query.lower()
    
    # Get relevant tools for intent
    relevant_tools = get_tools_for_intent(intent)
    
    # Determine specific tools to call based on query keywords
    tools_to_call = []
    
    # Troubleshooting keywords
    if any(word in query_lower for word in ["error", "fail", "debug", "timeout"]):
        tools_to_call.append("troubleshoot_hdl_error")
    
    # Bug resolution keywords
    if any(word in query_lower for word in ["fix", "resolve", "bug", "issue"]):
        tools_to_call.append("resolve_hdl_bug")
    
    # Performance keywords
    if any(word in query_lower for word in ["slow", "optimize", "performance"]):
        tools_to_call.append("optimize_hdl_pipeline")
    
    # Quality keywords
    if any(word in query_lower for word in ["quality", "validate", "completeness"]):
        tools_to_call.append("validate_hdl_data_quality")
    
    # Workflow execution keywords
    if any(word in query_lower for word in ["execute", "run", "trigger", "workflow"]):
        tools_to_call.append("execute_hdl_workflow")
    
    # Status check keywords
    if any(word in query_lower for word in ["status", "health", "monitor"]):
        tools_to_call.append("analyze_pipeline_health")
    
    # Documentation keywords
    if any(word in query_lower for word in ["explain", "what is", "how does"]):
        tools_to_call.append("explain_hdl_component")
    
    # Best practices keywords
    if any(word in query_lower for word in ["best practice", "should i", "recommend"]):
        tools_to_call.append("get_hdl_best_practices")
    
    # Reprocessing keywords
    if any(word in query_lower for word in ["reprocess", "rerun", "backfill"]):
        tools_to_call.append("coordinate_hdl_reprocessing")
    
    # Add reasoning
    reasoning = [
        f"Intent: {intent}",
        f"Identified {len(tools_to_call)} relevant tools",
        f"Tools: {', '.join(tools_to_call) if tools_to_call else 'None (will use RAG only)'}"
    ]
    
    return {
        "tools_to_call": tools_to_call,
        "reasoning": state.get("reasoning", []) + reasoning,
        "current_step": "tools_decided"
    }


# ============================================================================
# TOOL EXECUTION NODE
# ============================================================================

async def execute_tools_with_specialists_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute DPL specialist tools.
    
    Args:
        state: Current agent state
        
    Returns:
        State updates with tool results
    """
    tools_to_call = state.get("tools_to_call", [])
    
    if not tools_to_call:
        return {
            "current_step": "no_tools_executed",
            "tool_results": []
        }
    
    # Create tool lookup
    tool_lookup = {tool.name: tool for tool in ALL_DPL_TOOLS}
    
    # Execute tools
    tool_results = []
    
    for tool_name in tools_to_call:
        tool = tool_lookup.get(tool_name)
        
        if tool is None:
            tool_results.append({
                "tool": tool_name,
                "status": "error",
                "result": f"Tool '{tool_name}' not found"
            })
            continue
        
        try:
            # Extract parameters from state
            kwargs = _extract_tool_params(tool_name, state)
            
            # Execute tool
            result = await tool.ainvoke(kwargs) if hasattr(tool, 'ainvoke') else tool.invoke(kwargs)
            
            tool_results.append({
                "tool": tool_name,
                "status": "success",
                "result": result
            })
            
        except Exception as e:
            tool_results.append({
                "tool": tool_name,
                "status": "error",
                "result": f"Error executing tool: {str(e)}"
            })
    
    # Add reasoning
    reasoning = [
        f"Executed {len(tool_results)} tools",
        f"Successful: {sum(1 for r in tool_results if r['status'] == 'success')}",
        f"Failed: {sum(1 for r in tool_results if r['status'] == 'error')}"
    ]
    
    return {
        "tool_results": tool_results,
        "reasoning": state.get("reasoning", []) + reasoning,
        "current_step": "tools_executed"
    }


def _extract_tool_params(tool_name: str, state: AgentState) -> Dict[str, Any]:
    """Extract parameters for tool from state."""
    params = {}
    
    # Common parameters
    query = state["query"]
    entity_name = state.get("entity_name")
    pipeline_type = state.get("pipeline_type")
    
    # Tool-specific parameter extraction
    if tool_name == "troubleshoot_hdl_error":
        params = {
            "error_message": query,
            "entity_name": entity_name,
            "pipeline_type": pipeline_type
        }
    
    elif tool_name == "resolve_hdl_bug":
        params = {
            "bug_description": query,
            "entity_name": entity_name
        }
    
    elif tool_name == "optimize_hdl_pipeline":
        params = {
            "pipeline_name": entity_name or "hdl_pipeline",
            "performance_issue": query
        }
    
    elif tool_name == "validate_hdl_data_quality":
        params = {
            "entity_name": entity_name or "unknown",
            "quality_dimension": "all"
        }
    
    elif tool_name == "execute_hdl_workflow":
        params = {
            "workflow_name": entity_name or "hdl_workflow",
            "environment": "PRD"
        }
    
    elif tool_name == "analyze_pipeline_health":
        params = {
            "pipeline_name": entity_name or "hdl_pipeline",
            "check_metrics": True
        }
    
    elif tool_name == "explain_hdl_component":
        # Extract component name from query
        component = entity_name or _extract_component_from_query(query)
        params = {"component_name": component}
    
    elif tool_name == "get_hdl_best_practices":
        topic = _extract_topic_from_query(query)
        params = {"topic": topic}
    
    elif tool_name == "coordinate_hdl_reprocessing":
        params = {
            "entity_name": entity_name or "unknown",
            "date_range": "today",
            "notify_kpi_team": True
        }
    
    return params


def _extract_component_from_query(query: str) -> str:
    """Extract component name from query."""
    query_lower = query.lower()
    
    components = ["basetable", "scd2", "ingestioncontrol", "deltatableutils"]
    for component in components:
        if component in query_lower:
            return component
    
    return "hdl_component"


def _extract_topic_from_query(query: str) -> str:
    """Extract topic from query."""
    query_lower = query.lower()
    
    topics = ["scd2", "streaming", "batch", "performance", "quality"]
    for topic in topics:
        if topic in query_lower:
            return topic
    
    return "general"


# ============================================================================
# TOOL-ENHANCED RESPONSE NODE
# ============================================================================

async def generate_response_with_tools_node(
    state: AgentState,
    llm
) -> Dict[str, Any]:
    """
    Generate response incorporating tool results.
    
    Args:
        state: Current agent state
        llm: LLM provider instance
        
    Returns:
        State updates with generated response
    """
    from ..infrastructure.llm import get_system_prompt
    
    # Get base context
    query = state["query"]
    retrieved_context = state.get("retrieval_context", "")
    tool_results = state.get("tool_results", [])
    reasoning = state.get("reasoning", [])
    intent = state.get("intent", "general")
    
    # Format tool results
    tool_results_formatted = ""
    if tool_results:
        tool_results_formatted = "\n\n**SPECIALIST TOOL RESULTS**:\n"
        for result in tool_results:
            tool_results_formatted += f"\n[{result['tool']}]:\n{result['result']}\n"
    
    # Build prompt
    prompt = f"""Based on the DPL documentation context and specialist tool results, answer the user's question.

RETRIEVED CONTEXT:
{retrieved_context}
{tool_results_formatted}

REASONING:
{chr(10).join(f"- {r}" for r in reasoning)}

USER QUESTION:
{query}

Please provide a comprehensive, actionable response that synthesizes the retrieved context and tool results."""
    
    # Get system prompt
    system_prompt = get_system_prompt(intent)
    
    # Generate response
    response = await llm.generate(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.1,
        max_tokens=2048
    )
    
    # Create AI message
    ai_message = AIMessage(content=response)
    
    return {
        "final_response": response,
        "messages": [ai_message],
        "reasoning": reasoning + ["Generated response with tool results"],
        "current_step": "response_with_tools_generated"
    }


__all__ = [
    "decide_tools_node",
    "execute_tools_with_specialists_node",
    "generate_response_with_tools_node",
]

