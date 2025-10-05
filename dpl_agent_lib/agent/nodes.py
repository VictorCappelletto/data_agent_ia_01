"""
DPL Agent v3.0 - LangGraph Nodes

Nodes are the processing units in the LangGraph workflow.
Each node is a function that takes state and returns state updates.
"""

from typing import Dict, Any, List
from datetime import datetime

from langchain.schema import HumanMessage, AIMessage

from .state import AgentState, add_reasoning_step, increment_iteration
from ..infrastructure.llm import create_anthropic_provider, get_system_prompt
from ..infrastructure.vector_store import (
    create_hdl_retriever,
    RetrievalContext,
)


# ============================================================================
# INTENT ANALYSIS NODE
# ============================================================================

async def analyze_intent_node(state: AgentState) -> Dict[str, Any]:
    """
    Analyze user query to determine intent.
    
    Intent categories:
    - troubleshooting: Error diagnosis, debugging
    - architecture: System design, structure questions
    - optimization: Performance improvements
    - best_practices: Guidelines, recommendations
    - workflow_management: Workflow operations
    - data_quality: Quality validation
    - general: General questions
    
    Args:
        state: Current agent state
        
    Returns:
        State updates with intent classification
    """
    query = state["query"]
    
    # Simple keyword-based intent classification
    # In production, could use LLM for better classification
    intent = "general"
    confidence = 0.5
    
    query_lower = query.lower()
    
    # Troubleshooting keywords
    if any(word in query_lower for word in [
        "error", "fail", "timeout", "debug", "fix", "resolve",
        "problem", "issue", "broken", "not working"
    ]):
        intent = "troubleshooting"
        confidence = 0.9
    
    # Architecture keywords
    elif any(word in query_lower for word in [
        "architecture", "structure", "design", "how does", "what is",
        "explain", "overview", "components"
    ]):
        intent = "architecture"
        confidence = 0.8
    
    # Optimization keywords
    elif any(word in query_lower for word in [
        "optimize", "improve", "performance", "slow", "faster",
        "efficiency", "throughput"
    ]):
        intent = "optimization"
        confidence = 0.85
    
    # Best practices keywords
    elif any(word in query_lower for word in [
        "best practice", "should i", "recommend", "guideline",
        "pattern", "standard"
    ]):
        intent = "best_practices"
        confidence = 0.8
    
    # Workflow management keywords
    elif any(word in query_lower for word in [
        "workflow", "trigger", "schedule", "execute", "run",
        "status", "monitor"
    ]):
        intent = "workflow_management"
        confidence = 0.85
    
    # Data quality keywords
    elif any(word in query_lower for word in [
        "quality", "validation", "scd2", "completeness", "accuracy",
        "consistency", "integrity"
    ]):
        intent = "data_quality"
        confidence = 0.85
    
    # Extract entity name if present
    entity_name = None
    common_entities = ["visits", "tasks", "userclientcatalog", "vendorgroups", "identity"]
    for entity in common_entities:
        if entity in query_lower:
            entity_name = entity
            break
    
    # Extract pipeline type if present
    pipeline_type = None
    if "streaming" in query_lower or "stream" in query_lower:
        pipeline_type = "streaming"
    elif "batch" in query_lower:
        pipeline_type = "batch"
    
    # Extract layer if present
    layer = None
    if "bronze" in query_lower:
        layer = "bronze"
    elif "silver" in query_lower:
        layer = "silver"
    
    # Add reasoning
    reasoning = [
        f"Analyzed query intent",
        f"Classified as: {intent} (confidence: {confidence})",
        f"Entity: {entity_name or 'none'}",
        f"Pipeline type: {pipeline_type or 'none'}"
    ]
    
    return {
        "intent": intent,
        "confidence": confidence,
        "entity_name": entity_name,
        "pipeline_type": pipeline_type,
        "layer": layer,
        "reasoning": state.get("reasoning", []) + reasoning,
        "current_step": "intent_analyzed"
    }


# ============================================================================
# KNOWLEDGE RETRIEVAL NODE
# ============================================================================

async def retrieve_knowledge_node(
    state: AgentState,
    vector_store
) -> Dict[str, Any]:
    """
    Retrieve relevant knowledge from vector store.
    
    Args:
        state: Current agent state
        vector_store: Vector store instance
        
    Returns:
        State updates with retrieved documents
    """
    # Create retriever
    retriever = create_hdl_retriever(vector_store)
    
    # Build retrieval context
    context = RetrievalContext(
        query=state["query"],
        entity_name=state.get("entity_name"),
        pipeline_type=state.get("pipeline_type"),
        layer=state.get("layer"),
        category=state.get("intent") if state.get("intent") != "general" else None,
        top_k=5
    )
    
    # Retrieve documents
    result = await retriever.retrieve(context)
    
    # Format documents for LLM context
    formatted_context = retriever.format_documents_for_llm(
        result.documents,
        max_chars=4000
    )
    
    # Convert documents to dict format
    doc_dicts = [
        {
            "content": doc.page_content,
            "metadata": doc.metadata
        }
        for doc in result.documents
    ]
    
    # Add reasoning
    reasoning = [
        f"Retrieved {len(result.documents)} relevant documents",
        f"Context: {result.context_summary}"
    ]
    
    return {
        "retrieved_documents": doc_dicts,
        "retrieval_context": formatted_context,
        "reasoning": state.get("reasoning", []) + reasoning,
        "current_step": "knowledge_retrieved"
    }


# ============================================================================
# RESPONSE GENERATION NODE
# ============================================================================

async def generate_response_node(state: AgentState) -> Dict[str, Any]:
    """
    Generate final response using LLM.
    
    Args:
        state: Current agent state
        
    Returns:
        State updates with generated response
    """
    # Create LLM provider
    llm = create_anthropic_provider()
    
    # Get appropriate system prompt based on intent
    intent = state.get("intent", "general")
    system_prompt = get_system_prompt(intent)
    
    # Build prompt with context
    user_query = state["query"]
    retrieved_context = state.get("retrieval_context", "")
    reasoning = state.get("reasoning", [])
    
    prompt = f"""Based on the following DPL documentation context, please answer the user's question.

CONTEXT:
{retrieved_context}

REASONING SO FAR:
{chr(10).join(f"- {r}" for r in reasoning)}

USER QUESTION:
{user_query}

Please provide a helpful, accurate, and actionable response."""
    
    # Generate response
    response = await llm.generate(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.1,
        max_tokens=2048
    )
    
    # Add reasoning
    reasoning_update = [
        "Generated response using retrieved DPL knowledge",
        f"Used intent: {intent}"
    ]
    
    # Create AI message
    ai_message = AIMessage(content=response)
    
    return {
        "final_response": response,
        "messages": [ai_message],
        "reasoning": state.get("reasoning", []) + reasoning_update,
        "current_step": "response_generated"
    }


# ============================================================================
# TOOL EXECUTION NODE (Placeholder)
# ============================================================================

async def execute_tools_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute DPL tools if needed.
    
    This is a placeholder for future tool integration.
    Tools will include DPL specialists.
    
    Args:
        state: Current agent state
        
    Returns:
        State updates with tool results
    """
    tools_to_call = state.get("tools_to_call", [])
    
    if not tools_to_call:
        return {
            "current_step": "no_tools_needed"
        }
    
    # Placeholder: Tool execution will be implemented with DPL specialists
    tool_results = []
    
    for tool_name in tools_to_call:
        tool_results.append({
            "tool": tool_name,
            "result": f"Tool '{tool_name}' execution pending implementation"
        })
    
    return {
        "tool_results": tool_results,
        "reasoning": state.get("reasoning", []) + [f"Executed {len(tools_to_call)} tools"],
        "current_step": "tools_executed"
    }


# ============================================================================
# VALIDATION NODE
# ============================================================================

async def validate_response_node(state: AgentState) -> Dict[str, Any]:
    """
    Validate generated response before returning.
    
    Checks:
    - Response is not empty
    - Response is relevant to query
    - Response doesn't contain errors
    
    Args:
        state: Current agent state
        
    Returns:
        State updates with validation results
    """
    response = state.get("final_response", "")
    
    is_valid = True
    validation_errors = []
    
    # Check if response is empty
    if not response or len(response.strip()) < 10:
        is_valid = False
        validation_errors.append("Response is too short or empty")
    
    # Check for error indicators in response
    if "i don't know" in response.lower() or "cannot answer" in response.lower():
        # This might be valid, but flag for review
        validation_errors.append("Response indicates uncertainty")
    
    reasoning = []
    
    if is_valid:
        reasoning.append("Response validated successfully")
    else:
        reasoning.append(f"Response validation failed: {', '.join(validation_errors)}")
    
    return {
        "errors": state.get("errors", []) + validation_errors if not is_valid else state.get("errors", []),
        "reasoning": state.get("reasoning", []) + reasoning,
        "current_step": "response_validated"
    }


# ============================================================================
# HELPER NODES
# ============================================================================

async def increment_iteration_node(state: AgentState) -> Dict[str, Any]:
    """
    Increment iteration counter.
    
    Args:
        state: Current agent state
        
    Returns:
        State updates with incremented counter
    """
    return {
        "iteration_count": state.get("iteration_count", 0) + 1
    }


async def log_state_node(state: AgentState) -> Dict[str, Any]:
    """
    Log current state (for debugging).
    
    Args:
        state: Current agent state
        
    Returns:
        Empty state updates (no changes)
    """
    logger.debug(
        "Agent state checkpoint",
        current_step=state.get('current_step'),
        intent=state.get('intent'),
        iteration=f"{state.get('iteration_count')}/{state.get('max_iterations')}",
        retrieved_docs_count=len(state.get('retrieved_documents', []))
    )
    
    return {}

