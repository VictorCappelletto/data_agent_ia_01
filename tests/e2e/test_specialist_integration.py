"""
E2E Tests: Specialist Integration

Tests integration between LangGraph workflow and DPL specialists.
Validates that specialists are called appropriately and results are used.
"""

import pytest
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph, create_initial_state
from data_pipeline_agent_lib.utils import create_conversation_config


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.slow
class TestSpecialistIntegration:
    """E2E tests for specialist integration in workflow."""
    
    async def test_troubleshooter_integration(self, check_api_keys, conversation_thread_id):
        """Test integration with Troubleshooter specialist."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "My streaming pipeline has a timeout error after 1 hour. Help me diagnose."
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response = result["final_response"]
        
        # Should provide diagnostic information
        assert len(response) > 100
        response_lower = response.lower()
        assert any(word in response_lower for word in [
            "timeout", "streaming", "diagnose", "check", "investigate"
        ])
    
    async def test_bug_resolver_integration(self, check_api_keys, conversation_thread_id):
        """Test integration with Bug Resolver specialist."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "How do I resolve SCD2 is_current corruption?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        assert any(word in response_lower for word in [
            "scd2", "is_current", "fix", "resolve", "adjust"
        ])
    
    async def test_performance_advisor_integration(self, check_api_keys, conversation_thread_id):
        """Test integration with Performance Advisor specialist."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "My batch pipeline is taking 2 hours. How can I make it faster?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        assert any(word in response_lower for word in [
            "optimize", "performance", "faster", "batch", "recommendation"
        ])
    
    async def test_ecosystem_assistant_integration(self, check_api_keys, conversation_thread_id):
        """Test integration with Ecosystem Assistant specialist."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "Explain how TableFactory works in the DPL architecture"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        assert any(word in response_lower for word in [
            "table", "factory", "hdl", "architecture"
        ])
    
    async def test_coordinator_integration(self, check_api_keys, conversation_thread_id):
        """Test integration with DPL Coordinator specialist."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "I need to reprocess visits data for October 4th, it's urgent"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        assert any(word in response_lower for word in [
            "reprocess", "visits", "coordinate", "step"
        ])


@pytest.mark.e2e
@pytest.mark.asyncio
class TestMultiSpecialistWorkflow:
    """E2E tests requiring multiple specialists."""
    
    async def test_complex_scenario(self, check_api_keys, conversation_thread_id):
        """Test complex scenario requiring multiple specialists."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        # Complex query that might need troubleshooting + performance + coordination
        query = (
            "My visits batch pipeline is timing out and data quality is poor. "
            "I need to troubleshoot, optimize, and possibly reprocess."
        )
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response = result["final_response"]
        
        # Should provide comprehensive guidance
        assert len(response) > 150
        
        response_lower = response.lower()
        # Should address multiple concerns
        concern_count = sum(1 for word in [
            "timeout", "quality", "optimize", "troubleshoot", "reprocess"
        ] if word in response_lower)
        
        assert concern_count >= 2  # Should address at least 2 concerns


@pytest.mark.e2e
@pytest.mark.asyncio
class TestErrorHandling:
    """E2E tests for error handling in workflow."""
    
    async def test_invalid_query_handling(self, check_api_keys, conversation_thread_id):
        """Test handling of invalid or unclear queries."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "xyz abc 123"  # Nonsensical query
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        # Should still generate a response (not crash)
        assert "final_response" in result
        assert isinstance(result["final_response"], str)
    
    async def test_empty_query_handling(self, check_api_keys, conversation_thread_id):
        """Test handling of empty query."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = ""
        initial_state = create_initial_state(query)
        
        # Should handle gracefully
        try:
            result = await graph.ainvoke(initial_state, config)
            assert result is not None
        except Exception as e:
            # If it raises an exception, it should be handled gracefully
            assert "query" in str(e).lower() or "empty" in str(e).lower()

