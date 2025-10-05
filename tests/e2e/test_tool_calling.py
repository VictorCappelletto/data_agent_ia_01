"""
E2E Tests: Tool Calling Workflow

Tests the complete tool calling workflow including:
- Tool selection (decide_tools_node)
- Tool execution (execute_tools_with_specialists_node)
- Result integration into response
"""

import pytest
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph, create_initial_state
from data_pipeline_agent_lib.utils import create_conversation_config


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.slow
class TestToolCalling:
    """E2E tests for tool calling workflow."""
    
    async def test_troubleshooting_tool_call(self, check_api_keys, conversation_thread_id):
        """Test troubleshooting tool is called for error queries."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "I have a timeout error in my streaming pipeline, can you help diagnose?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        # Should have called troubleshooting tool
        assert "final_response" in result
        assert len(result["final_response"]) > 100
        
        response_lower = result["final_response"].lower()
        # Should contain troubleshooting-related terms
        assert any(word in response_lower for word in [
            "timeout", "diagnose", "troubleshoot", "error", "streaming"
        ])
    
    async def test_bug_resolution_tool_call(self, check_api_keys, conversation_thread_id):
        """Test bug resolution tool for known bugs."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "How do I fix SCD2 is_current issues?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        assert "scd2" in response_lower
    
    async def test_performance_optimization_tool(self, check_api_keys, conversation_thread_id):
        """Test performance optimization tool."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "My batch pipeline is very slow, how can I optimize it?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        assert any(word in response_lower for word in [
            "optimi", "performance", "slow", "batch"
        ])
    
    async def test_quality_validation_tool(self, check_api_keys, conversation_thread_id):
        """Test data quality validation tool."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "Can you validate data quality for the visits entity?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        assert any(word in response_lower for word in [
            "quality", "validate", "visits", "data"
        ])
    
    async def test_workflow_execution_tool(self, check_api_keys, conversation_thread_id):
        """Test workflow execution coordination."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "Execute hdl-batch-visits workflow in UAT environment"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        assert any(word in response_lower for word in [
            "workflow", "execute", "batch", "visits"
        ])


@pytest.mark.e2e
@pytest.mark.asyncio
class TestToolSelection:
    """E2E tests for intelligent tool selection."""
    
    async def test_appropriate_tool_selection(self, check_api_keys, conversation_thread_id):
        """Test that agent selects appropriate tools based on query."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        # Query that should trigger troubleshooting
        query = "Pipeline failing with connection error"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        # Should have selected and executed relevant tool
        assert "final_response" in result
        assert len(result["final_response"]) > 50
    
    async def test_no_tool_for_simple_question(self, check_api_keys, conversation_thread_id):
        """Test that simple questions don't trigger tools."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "What does DPL stand for?"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        # Should answer without tools
        assert "final_response" in result
        response_lower = result["final_response"].lower()
        assert "hdl" in response_lower or "high" in response_lower


@pytest.mark.e2e
@pytest.mark.asyncio
class TestToolResultIntegration:
    """E2E tests for tool result integration."""
    
    async def test_tool_results_in_response(self, check_api_keys, conversation_thread_id):
        """Test that tool results are integrated into final response."""
        graph = create_data_pipeline_agent_graph()
        config = create_conversation_config(conversation_thread_id)
        
        query = "Diagnose timeout error in visits pipeline"
        initial_state = create_initial_state(query)
        
        result = await graph.ainvoke(initial_state, config)
        
        # Tool results should influence response
        assert "final_response" in result
        assert len(result["final_response"]) > 100
        
        # Should contain actionable information
        response_lower = result["final_response"].lower()
        assert any(word in response_lower for word in [
            "timeout", "pipeline", "visits", "recommend", "check"
        ])

