"""
DPL Agent v3.0 - LangGraph StateGraph

Main agent orchestration using LangGraph StateGraph.
Defines the workflow, nodes, edges, and conditional routing.
"""

import os
from typing import Literal, Optional
from functools import partial

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .state import AgentState
from ..utils import get_logger

# Initialize logger
logger = get_logger(__name__)

from .nodes import (
    analyze_intent_node,
    retrieve_knowledge_node,
    generate_response_node,
    execute_tools_node,
    validate_response_node,
    increment_iteration_node,
    log_state_node,
)
from ..infrastructure.vector_store import create_chroma_store


# ============================================================================
# CONDITIONAL ROUTING FUNCTIONS
# ============================================================================

def route_after_intent(state: AgentState) -> Literal["retrieve_knowledge", "error"]:
    """
    Route after intent analysis.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node name
    """
    # Check if intent was classified with confidence
    if state.get("intent") and state.get("confidence", 0) > 0.5:
        return "retrieve_knowledge"
    else:
        # Low confidence, still retrieve but with general category
        return "retrieve_knowledge"


def route_after_retrieval(state: AgentState) -> Literal["execute_tools", "generate_response"]:
    """
    Route after knowledge retrieval.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node name
    """
    # Check if tools need to be called
    if state.get("tools_to_call"):
        return "execute_tools"
    else:
        # Go directly to response generation
        return "generate_response"


def route_after_tools(state: AgentState) -> Literal["generate_response"]:
    """
    Route after tool execution.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node name
    """
    # Always go to response generation after tools
    return "generate_response"


def route_after_validation(
    state: AgentState
) -> Literal["end", "retrieve_knowledge", "generate_response"]:
    """
    Route after response validation.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node name or END
    """
    # Check for validation errors
    if state.get("errors"):
        # If iteration count is low, retry
        if state["iteration_count"] < state["max_iterations"] - 1:
            return "retrieve_knowledge"  # Retry with different retrieval
        else:
            return "end"  # Give up and return what we have
    
    # Validation passed
    return "end"


def should_continue_workflow(state: AgentState) -> Literal["continue", "end"]:
    """
    Determine if workflow should continue.
    
    Args:
        state: Current agent state
        
    Returns:
        "continue" or "end"
    """
    if should_continue(state):
        return "continue"
    else:
        return "end"


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def create_data_pipeline_agent_graph(
    checkpointer: Optional[MemorySaver] = None,
    vector_store = None,
    enable_debug: bool = False
):
    """
    Create the DPL Agent LangGraph.
    
    Args:
        checkpointer: Optional checkpointer for memory
        vector_store: Optional vector store (creates default if None)
        enable_debug: Enable debug logging
        
    Returns:
        Compiled StateGraph
    """
    # Create vector store if not provided
    if vector_store is None:
        vector_store = create_chroma_store()
    
    # Create graph builder
    graph_builder = StateGraph(AgentState)
    
    # ========================================================================
    # ADD NODES
    # ========================================================================
    
    # Intent analysis node
    graph_builder.add_node("analyze_intent", analyze_intent_node)
    
    # Knowledge retrieval node (with vector store injected)
    retrieve_with_store = partial(retrieve_knowledge_node, vector_store=vector_store)
    graph_builder.add_node("retrieve_knowledge", retrieve_with_store)
    
    # Tool execution node
    graph_builder.add_node("execute_tools", execute_tools_node)
    
    # Response generation node
    graph_builder.add_node("generate_response", generate_response_node)
    
    # Validation node
    graph_builder.add_node("validate_response", validate_response_node)
    
    # Utility nodes
    graph_builder.add_node("increment_iteration", increment_iteration_node)
    
    if enable_debug:
        graph_builder.add_node("log_state", log_state_node)
    
    # ========================================================================
    # ADD EDGES
    # ========================================================================
    
    # Entry point: START -> analyze_intent
    graph_builder.set_entry_point("analyze_intent")
    
    # Intent -> Retrieval (conditional)
    graph_builder.add_conditional_edges(
        "analyze_intent",
        route_after_intent,
        {
            "retrieve_knowledge": "retrieve_knowledge",
            "error": END  # Should never happen with current logic
        }
    )
    
    # Retrieval -> Tools or Response (conditional)
    graph_builder.add_conditional_edges(
        "retrieve_knowledge",
        route_after_retrieval,
        {
            "execute_tools": "execute_tools",
            "generate_response": "generate_response"
        }
    )
    
    # Tools -> Response
    graph_builder.add_conditional_edges(
        "execute_tools",
        route_after_tools,
        {
            "generate_response": "generate_response"
        }
    )
    
    # Response -> Validation
    graph_builder.add_edge("generate_response", "validate_response")
    
    # Validation -> END or Retry (conditional)
    graph_builder.add_conditional_edges(
        "validate_response",
        route_after_validation,
        {
            "end": END,
            "retrieve_knowledge": "retrieve_knowledge",
            "generate_response": "generate_response"
        }
    )
    
    # Debug edges
    if enable_debug:
        graph_builder.add_edge("analyze_intent", "log_state")
        graph_builder.add_edge("retrieve_knowledge", "log_state")
    
    # ========================================================================
    # COMPILE GRAPH
    # ========================================================================
    
    # Use provided checkpointer or create default
    if checkpointer is None:
        checkpointer = MemorySaver()
    
    # Compile graph
    compiled_graph = graph_builder.compile(
        checkpointer=checkpointer
    )
    
    return compiled_graph


# ============================================================================
# SIMPLIFIED GRAPH (For Quick Start)
# ============================================================================

def create_simple_hdl_graph(vector_store=None):
    """
    Create a simplified DPL agent graph (fewer nodes).
    
    Workflow: analyze_intent -> retrieve_knowledge -> generate_response -> END
    
    Args:
        vector_store: Optional vector store
        
    Returns:
        Compiled StateGraph
    """
    # Create vector store if not provided
    if vector_store is None:
        vector_store = create_chroma_store()
    
    # Create graph builder
    graph_builder = StateGraph(AgentState)
    
    # Add nodes
    graph_builder.add_node("analyze_intent", analyze_intent_node)
    
    retrieve_with_store = partial(retrieve_knowledge_node, vector_store=vector_store)
    graph_builder.add_node("retrieve_knowledge", retrieve_with_store)
    
    graph_builder.add_node("generate_response", generate_response_node)
    
    # Add edges (linear flow)
    graph_builder.set_entry_point("analyze_intent")
    graph_builder.add_edge("analyze_intent", "retrieve_knowledge")
    graph_builder.add_edge("retrieve_knowledge", "generate_response")
    graph_builder.add_edge("generate_response", END)
    
    # Compile
    compiled_graph = graph_builder.compile(
        checkpointer=MemorySaver()
    )
    
    return compiled_graph


# ============================================================================
# GRAPH UTILITIES
# ============================================================================

def visualize_graph(graph, output_path: str = "workflow_graph.png"):
    """
    Visualize the graph structure.
    
    Args:
        graph: Compiled graph
        output_path: Output file path
    """
    try:
        graph_image = graph.get_graph().draw_mermaid_png()
        
        with open(output_path, "wb") as f:
            f.write(graph_image)
        
        logger.info("Graph visualization saved", output_path=output_path)
        
    except Exception as e:
        logger.warning("Could not generate graph visualization", error=str(e))


def get_graph_info(graph) -> dict:
    """
    Get information about the graph structure.
    
    Args:
        graph: Compiled graph
        
    Returns:
        Dictionary with graph information
    """
    try:
        graph_data = graph.get_graph()
        
        return {
            "nodes": list(graph_data.nodes.keys()) if hasattr(graph_data, 'nodes') else [],
            "edges": len(graph_data.edges) if hasattr(graph_data, 'edges') else 0,
            "entry_point": getattr(graph_data, 'entry_point', None),
        }
    except Exception as e:
        return {"error": str(e)}

