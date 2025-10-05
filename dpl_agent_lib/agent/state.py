"""
DPL Agent v3.0 - Agent State Definition

Defines the state schema for LangGraph StateGraph.
The state represents all information that flows through the agent workflow.
"""

from typing import TypedDict, List, Dict, Any, Optional, Annotated
from datetime import datetime
from operator import add

from langchain.schema import BaseMessage


# ============================================================================
# STATE SCHEMA
# ============================================================================

class AgentState(TypedDict):
    """
    State schema for DPL Agent.
    
    This represents all information that flows through the agent graph.
    Each node can read from and write to this state.
    """
    
    # Messages (conversation history)
    messages: Annotated[List[BaseMessage], add]  # add_messages reducer
    
    # User query context
    query: str
    entity_name: Optional[str]
    pipeline_type: Optional[str]  # "streaming" or "batch"
    layer: Optional[str]  # "bronze" or "silver"
    
    # Intent classification
    intent: Optional[str]  # "troubleshooting", "architecture", "optimization", etc.
    confidence: Optional[float]  # Intent classification confidence
    
    # Retrieved knowledge
    retrieved_documents: List[Dict[str, Any]]
    retrieval_context: Optional[str]  # Summary of retrieved context
    
    # Tool execution
    tools_to_call: List[str]
    tool_results: List[Dict[str, Any]]
    
    # Agent reasoning
    reasoning: List[str]  # Chain of thought
    current_step: str  # Current workflow step
    
    # Response generation
    draft_response: Optional[str]
    final_response: Optional[str]
    
    # Metadata
    session_id: str
    timestamp: datetime
    iteration_count: int
    max_iterations: int
    
    # Error handling
    errors: List[str]
    requires_human_input: bool
    
    # DPL-specific context
    hdl_context: Dict[str, Any]  # Pipeline status, workflow info, etc.


class ConversationState(TypedDict):
    """
    Extended state for multi-turn conversations.
    
    Includes conversation-level context that persists across messages.
    """
    
    # Base agent state
    messages: Annotated[List[BaseMessage], add]
    
    # Conversation metadata
    conversation_id: str
    user_id: Optional[str]
    started_at: datetime
    last_updated: datetime
    turn_count: int
    
    # Conversation context
    topic: Optional[str]  # Current conversation topic
    entities_mentioned: List[str]  # Entities discussed
    issues_tracking: List[Dict[str, Any]]  # Ongoing issues
    
    # User preferences
    detail_level: str  # "brief", "standard", "detailed"
    include_examples: bool
    technical_depth: str  # "beginner", "intermediate", "expert"


class WorkflowState(TypedDict):
    """
    State for workflow orchestration tasks.
    
    Used when agent needs to orchestrate multiple DPL workflows.
    """
    
    # Base agent state
    messages: Annotated[List[BaseMessage], add]
    
    # Workflow context
    target_workflows: List[str]
    workflow_statuses: Dict[str, str]  # workflow_name -> status
    
    # Execution plan
    execution_sequence: List[str]  # Ordered workflow execution
    dependencies: Dict[str, List[str]]  # workflow -> dependencies
    
    # Results
    completed_workflows: List[str]
    failed_workflows: List[str]
    pending_workflows: List[str]


# ============================================================================
# STATE HELPERS
# ============================================================================

def create_initial_state(
    query: str,
    session_id: str,
    max_iterations: int = 10
) -> AgentState:
    """
    Create initial agent state.
    
    Args:
        query: User query
        session_id: Session identifier
        max_iterations: Maximum workflow iterations
        
    Returns:
        Initial AgentState
    """
    return AgentState(
        messages=[],
        query=query,
        entity_name=None,
        pipeline_type=None,
        layer=None,
        intent=None,
        confidence=None,
        retrieved_documents=[],
        retrieval_context=None,
        tools_to_call=[],
        tool_results=[],
        reasoning=[],
        current_step="start",
        draft_response=None,
        final_response=None,
        session_id=session_id,
        timestamp=datetime.utcnow(),
        iteration_count=0,
        max_iterations=max_iterations,
        errors=[],
        requires_human_input=False,
        hdl_context={}
    )


def should_continue(state: AgentState) -> bool:
    """
    Check if agent should continue processing.
    
    Args:
        state: Current agent state
        
    Returns:
        True if should continue, False otherwise
    """
    # Check iteration limit
    if state["iteration_count"] >= state["max_iterations"]:
        return False
    
    # Check if response is ready
    if state["final_response"]:
        return False
    
    # Check if waiting for human input
    if state["requires_human_input"]:
        return False
    
    # Check for critical errors
    if any("critical" in error.lower() for error in state["errors"]):
        return False
    
    return True


def extract_context_from_state(state: AgentState) -> Dict[str, Any]:
    """
    Extract relevant context from state for LLM prompts.
    
    Args:
        state: Current agent state
        
    Returns:
        Context dictionary
    """
    context = {
        "query": state["query"],
        "intent": state.get("intent"),
        "reasoning": state.get("reasoning", []),
        "retrieved_context": state.get("retrieval_context"),
        "hdl_context": state.get("hdl_context", {}),
    }
    
    # Add entity context if available
    if state.get("entity_name"):
        context["entity"] = state["entity_name"]
    
    # Add pipeline context if available
    if state.get("pipeline_type"):
        context["pipeline_type"] = state["pipeline_type"]
    
    # Add tool results if available
    if state.get("tool_results"):
        context["tool_results"] = state["tool_results"]
    
    return context


def add_reasoning_step(state: AgentState, step: str) -> AgentState:
    """
    Add a reasoning step to the state.
    
    Args:
        state: Current agent state
        step: Reasoning step to add
        
    Returns:
        Updated state
    """
    state["reasoning"].append(step)
    return state


def add_error(state: AgentState, error: str) -> AgentState:
    """
    Add an error to the state.
    
    Args:
        state: Current agent state
        error: Error message
        
    Returns:
        Updated state
    """
    state["errors"].append(error)
    return state


def increment_iteration(state: AgentState) -> AgentState:
    """
    Increment iteration count.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state
    """
    state["iteration_count"] += 1
    return state


# ============================================================================
# STATE VALIDATORS
# ============================================================================

def validate_state(state: AgentState) -> List[str]:
    """
    Validate agent state for consistency.
    
    Args:
        state: Agent state to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Required fields
    if not state.get("query"):
        errors.append("Query is required")
    
    if not state.get("session_id"):
        errors.append("Session ID is required")
    
    # Logical validations
    if state["iteration_count"] < 0:
        errors.append("Iteration count cannot be negative")
    
    if state["max_iterations"] <= 0:
        errors.append("Max iterations must be positive")
    
    if state["iteration_count"] > state["max_iterations"]:
        errors.append("Iteration count exceeds maximum")
    
    # Intent validation
    valid_intents = [
        "troubleshooting",
        "architecture",
        "optimization",
        "best_practices",
        "workflow_management",
        "data_quality",
        "general"
    ]
    
    if state.get("intent") and state["intent"] not in valid_intents:
        errors.append(f"Invalid intent: {state['intent']}")
    
    return errors


# ============================================================================
# STATE SERIALIZATION
# ============================================================================

def serialize_state(state: AgentState) -> Dict[str, Any]:
    """
    Serialize agent state for storage.
    
    Args:
        state: Agent state to serialize
        
    Returns:
        Serializable dictionary
    """
    serialized = dict(state)
    
    # Convert datetime to ISO format
    if isinstance(serialized.get("timestamp"), datetime):
        serialized["timestamp"] = serialized["timestamp"].isoformat()
    
    # Convert messages to serializable format
    if serialized.get("messages"):
        serialized["messages"] = [
            {
                "type": msg.type,
                "content": msg.content,
            }
            for msg in serialized["messages"]
        ]
    
    return serialized


def deserialize_state(data: Dict[str, Any]) -> AgentState:
    """
    Deserialize agent state from storage.
    
    Args:
        data: Serialized state data
        
    Returns:
        AgentState
    """
    # Convert ISO format to datetime
    if isinstance(data.get("timestamp"), str):
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
    
    # Reconstruct messages (simplified)
    # In production, would need proper BaseMessage reconstruction
    
    return AgentState(**data)

