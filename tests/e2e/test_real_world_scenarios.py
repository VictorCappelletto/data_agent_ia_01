"""
E2E Tests: Real-World Scenarios

Tests based on actual DPL operational scenarios from Victor's experience.
"""

import pytest
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph, create_initial_state
from data_pipeline_agent_lib.utils import create_conversation_config


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.slow
class TestRealWorldScenarios:
    """E2E tests simulating real operational scenarios."""
    
    async def test_urgent_reprocessing_scenario(self, check_api_keys, conversation_thread_id):
        """
        Test real-world scenario from Victor's memory:
        Timeout in job batch DPL (vendor BR, 1h30m) - urgent client waiting.
        """
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = (
            "URGENT: TASKS entity batch pipeline timed out after 1h30m. "
            "Data didn't reach silver layer. Client is waiting. "
            "What should I do? Need to coordinate with KPI team after."
        )
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response = result["final_response"]
        
        # Should provide urgent action plan
        assert len(response) > 150
        response_lower = response.lower()
        
        # Should address key points
        assert "tasks" in response_lower or "task" in response_lower
        assert any(word in response_lower for word in [
            "reprocess", "urgent", "silver", "kpi", "coordinate"
        ])
    
    async def test_streaming_checkpoint_issue(self, check_api_keys, conversation_thread_id):
        """Test streaming checkpoint timeout scenario."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = (
            "My dpl-stream-visits workflow is timing out at the checkpoint. "
            "What could be causing this and how do I fix it?"
        )
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        
        assert any(word in response_lower for word in [
            "checkpoint", "streaming", "timeout", "visits"
        ])
    
    async def test_document_storedb_connection_failure(self, check_api_keys, conversation_thread_id):
        """Test CosmosDB connection failure scenario."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = (
            "Batch pipeline failing with 'Connection refused to MongoDB'. "
            "This is the CosmosDB connection. How do I troubleshoot?"
        )
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        
        assert any(word in response_lower for word in [
            "connection", "document_storedb", "document_db", "troubleshoot", "batch"
        ])
    
    async def test_data_quality_investigation(self, check_api_keys, conversation_thread_id):
        """Test data quality investigation workflow."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = (
            "KPI team is reporting incorrect data in the gold layer. "
            "I need to validate data quality for orders entity in silver layer."
        )
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        
        assert any(word in response_lower for word in [
            "quality", "validate", "orders", "data", "check"
        ])
    
    async def test_performance_optimization_request(self, check_api_keys, conversation_thread_id):
        """Test performance optimization workflow."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = (
            "The hdl-batch-tasks pipeline is taking 2 hours to complete. "
            "Normally it takes 30 minutes. How can I optimize it?"
        )
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        
        assert any(word in response_lower for word in [
            "optimize", "performance", "batch", "tasks", "hours", "faster"
        ])


@pytest.mark.e2e
@pytest.mark.asyncio
class TestComplexWorkflows:
    """E2E tests for complex multi-step workflows."""
    
    async def test_diagnostic_to_resolution_workflow(self, check_api_keys, conversation_thread_id):
        """Test complete workflow from diagnosis to resolution."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        queries = [
            # Step 1: Report problem
            "Pipeline is failing with memory error",
            # Step 2: Ask for resolution
            "How do I fix this?",
            # Step 3: Ask about prevention
            "How can I prevent this in the future?"
        ]
        
        previous_messages = []
        
        for query in queries:
            state = create_initial_state(query)
            state["messages"] = previous_messages
            
            result = await graph.ainvoke(state, config)
            
            assert "final_response" in result
            assert len(result["final_response"]) > 30
            
            previous_messages = result["messages"]
        
        # Final response should have context from all queries
        final_response = result["final_response"]
        assert len(final_response) > 50
    
    async def test_architecture_deep_dive(self, check_api_keys, conversation_thread_id):
        """Test deep architectural questions."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = (
            "Explain the complete data flow from bronze to silver layer "
            "for streaming pipelines, including SCD2 merge"
        )
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response = result["final_response"]
        
        # Should provide comprehensive explanation
        assert len(response) > 200
        
        response_lower = response.lower()
        # Should cover key concepts
        key_concepts = sum(1 for word in [
            "bronze", "silver", "streaming", "scd2", "merge"
        ] if word in response_lower)
        
        assert key_concepts >= 3  # Should mention at least 3 key concepts


@pytest.mark.e2e
@pytest.mark.asyncio
class TestAgentReliability:
    """E2E tests for agent reliability and robustness."""
    
    async def test_consistent_responses(self, check_api_keys, conversation_thread_id):
        """Test that similar queries get consistent responses."""
        graph = create_data_pipeline_agent_graph()
        
        # Same question, different threads
        query = "What is the bronze layer?"
        
        results = []
        for i in range(2):
            config = create_conversation_config(f"{conversation_thread_id}_{i}")
            state = create_initial_state(query)
            result = await graph.ainvoke(state, config)
            results.append(result["final_response"])
        
        # Both should mention bronze
        for response in results:
            assert "bronze" in response.lower()
            assert len(response) > 30
    
    async def test_iteration_limit(self, check_api_keys, conversation_thread_id):
        """Test that agent respects iteration limits."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "Test query"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        # Should not exceed max iterations
        assert result["iteration_count"] <= 10
    
    async def test_response_quality(self, check_api_keys, conversation_thread_id):
        """Test overall response quality."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "How do I troubleshoot DPL pipeline issues?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        response = result["final_response"]
        
        # Quality checks
        assert len(response) > 100  # Substantive response
        assert response.strip() == response  # No leading/trailing whitespace
        
        # No emojis
        emojis = ["🎯", "✅", "🚀", "📊", "⚠️", "🔍", "💡"]
        for emoji in emojis:
            assert emoji not in response

