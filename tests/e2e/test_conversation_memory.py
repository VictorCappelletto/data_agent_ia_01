"""
E2E Tests: Multi-turn Conversation & Memory

Tests conversation memory, context tracking, and multi-turn interactions.
"""

import pytest
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph, create_initial_state
from data_pipeline_agent_lib.utils import create_conversation_config
from langchain_core.messages import HumanMessage


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.slow
class TestConversationMemory:
    """E2E tests for conversation memory."""
    
    async def test_two_turn_conversation(self, check_api_keys, conversation_thread_id):
        """Test 2-turn conversation with memory."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        # Turn 1
        query1 = "What is the bronze layer?"
        state1 = create_initial_state(query1)
        result1 = await graph.ainvoke(state1, config)
        
        assert "final_response" in result1
        assert "bronze" in result1["final_response"].lower()
        
        # Turn 2 - Follow-up question
        query2 = "What about silver layer?"
        # Use same config to maintain thread
        state2 = create_initial_state(query2)
        state2["messages"] = result1["messages"]  # Carry forward messages
        
        result2 = await graph.ainvoke(state2, config)
        
        assert "final_response" in result2
        assert "silver" in result2["final_response"].lower()
        
        # Should have accumulated messages
        assert len(result2["messages"]) > len(result1["messages"])
    
    async def test_context_tracking(self, check_api_keys, conversation_thread_id):
        """Test that agent tracks context across turns."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        # Turn 1: Ask about entity
        query1 = "Tell me about the visits entity"
        state1 = create_initial_state(query1)
        result1 = await graph.ainvoke(state1, config)
        
        # Turn 2: Ask follow-up using "it" (requires context)
        query2 = "How is it ingested?"
        state2 = create_initial_state(query2)
        state2["messages"] = result1["messages"]
        
        result2 = await graph.ainvoke(state2, config)
        
        assert "final_response" in result2
        # Should understand "it" refers to visits
        response_lower = result2["final_response"].lower()
        assert any(word in response_lower for word in [
            "visits", "ingest", "pipeline", "stream", "batch"
        ])
    
    async def test_multi_turn_workflow(self, check_api_keys, conversation_thread_id):
        """Test 3+ turn conversation workflow."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        queries = [
            "What is DPL?",
            "What are the main layers?",
            "How does bronze layer work?"
        ]
        
        previous_messages = []
        
        for i, query in enumerate(queries):
            state = create_initial_state(query)
            state["messages"] = previous_messages
            
            result = await graph.ainvoke(state, config)
            
            assert "final_response" in result
            assert len(result["final_response"]) > 20
            
            previous_messages = result["messages"]
            
            # Messages should accumulate
            assert len(previous_messages) >= (i + 1) * 2  # At least user + assistant per turn


@pytest.mark.e2e
@pytest.mark.asyncio
class TestCheckpointing:
    """E2E tests for checkpointing and state persistence."""
    
    async def test_checkpoint_creation(self, check_api_keys, conversation_thread_id):
        """Test that checkpoints are created during conversation."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "What is bronze layer?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        # Get state to verify checkpoint
        current_state = graph.get_state(config)
        
        assert current_state is not None
        assert current_state.values is not None
    
    async def test_state_retrieval(self, check_api_keys, conversation_thread_id):
        """Test retrieving state after execution."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        # Execute query
        query = "Explain SCD2"
        initial_state = create_initial_state(query)
        result = await graph.ainvoke(initial_state, config)
        
        # Retrieve state
        retrieved_state = graph.get_state(config)
        
        assert retrieved_state is not None
        assert retrieved_state.values["query"] == query
        assert len(retrieved_state.values["messages"]) > 0

