"""
E2E Tests: Simple Queries (No Tool Calling)

Tests basic question-answering capabilities without tool execution.
Validates LangGraph workflow, RAG retrieval, and LLM response generation.
"""

import pytest
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph, create_initial_state
from data_pipeline_agent_lib.utils import create_conversation_config


@pytest.mark.e2e
@pytest.mark.asyncio
class TestSimpleQueries:
    """E2E tests for simple question-answering."""
    
    async def test_bronze_layer_explanation(self, check_api_keys, conversation_thread_id):
        """Test explaining bronze layer concept."""
        # Create agent
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        # Query about bronze layer
        query = "What is the bronze layer in DPL architecture?"
        initial_state = create_initial_state(query)
        
        # Execute workflow
        result = await graph.ainvoke(initial_state, config)
        
        # Validate response
        assert result is not None
        assert "final_response" in result
        assert len(result["final_response"]) > 50
        
        response_lower = result["final_response"].lower()
        assert "bronze" in response_lower
        assert any(word in response_lower for word in ["raw", "ingestion", "data"])
    
    async def test_scd2_explanation(self, check_api_keys, conversation_thread_id):
        """Test explaining SCD2 concept."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "Explain SCD2 in DPL context"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert result is not None
        assert "final_response" in result
        
        response_lower = result["final_response"].lower()
        assert "scd2" in response_lower or "slowly changing dimension" in response_lower
    
    async def test_streaming_vs_batch(self, check_api_keys, conversation_thread_id):
        """Test comparing streaming and batch pipelines."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "What's the difference between streaming and batch pipelines in DPL?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert result is not None
        response_lower = result["final_response"].lower()
        assert "streaming" in response_lower or "stream" in response_lower
        assert "batch" in response_lower
    
    async def test_workflow_architecture(self, check_api_keys, conversation_thread_id):
        """Test explaining workflow architecture."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "How do DPL workflows work?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert result is not None
        assert len(result["final_response"]) > 50
    
    async def test_no_emojis_in_response(self, check_api_keys, conversation_thread_id):
        """Test that responses contain no emojis."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "What is bronze layer?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        # Check for common emojis
        emojis = ["🎯", "✅", "🚀", "📊", "⚠️", "🔍", "💡"]
        response = result["final_response"]
        
        for emoji in emojis:
            assert emoji not in response, f"Found emoji {emoji} in response"


@pytest.mark.e2e
@pytest.mark.asyncio
class TestRAGRetrieval:
    """E2E tests validating RAG system functionality."""
    
    async def test_retrieval_quality(self, check_api_keys, conversation_thread_id):
        """Test that RAG retrieves relevant documents."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "How does IngestionControl work in DPL?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        # Check if documents were retrieved
        if "retrieved_documents" in result:
            assert len(result["retrieved_documents"]) > 0
        
        # Response should mention IngestionControl
        response_lower = result["final_response"].lower()
        assert "ingestion" in response_lower
    
    async def test_context_relevance(self, check_api_keys, conversation_thread_id):
        """Test that retrieved context is relevant to query."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "What is TableFactory used for?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        response_lower = result["final_response"].lower()
        assert "table" in response_lower or "factory" in response_lower


@pytest.mark.e2e
@pytest.mark.asyncio  
class TestAgentState:
    """E2E tests validating agent state management."""
    
    async def test_state_initialization(self, check_api_keys, conversation_thread_id):
        """Test that agent state initializes correctly."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "Test query"
        initial_state = create_initial_state(query)
        
        # Validate initial state structure
        assert "messages" in initial_state
        assert "query" in initial_state
        assert initial_state["query"] == query
        assert "iteration_count" in initial_state
        assert initial_state["iteration_count"] == 0
    
    async def test_state_persistence(self, check_api_keys, conversation_thread_id):
        """Test that state persists through workflow."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "What is bronze layer?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        # State should have been updated
        assert result["iteration_count"] >= 0
        assert len(result["messages"]) > 0

