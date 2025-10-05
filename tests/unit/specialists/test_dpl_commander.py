"""
Unit tests for data_pipeline_agent_lib.specialists.hdl_commander module.
"""

import pytest
from data_pipeline_agent_lib.specialists.hdl_commander import (
    execute_hdl_workflow,
    get_workflow_status
)


class TestDPLCommanderModule:
    """Test suite for hdl_commander module."""
    
    def test_execute_workflow_exists(self):
        """Test that execute_hdl_workflow tool exists."""
        assert callable(execute_hdl_workflow)
    
    def test_get_status_exists(self):
        """Test that get_workflow_status tool exists."""
        assert callable(get_workflow_status)


class TestExecuteDPLWorkflowTool:
    """Test suite for execute_hdl_workflow tool function."""
    
    def test_tool_execute_streaming(self, sample_workflow_name):
        """Test executing streaming workflow."""
        result = execute_hdl_workflow(
            f"execute {sample_workflow_name}"
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_execute_batch(self, sample_workflow_name):
        """Test executing batch workflow."""
        result = execute_hdl_workflow(
            f"run batch workflow {sample_workflow_name}"
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_with_environment(self, sample_workflow_name):
        """Test workflow execution with environment."""
        result = execute_hdl_workflow(
            f"execute {sample_workflow_name} in production"
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_no_emojis(self, sample_workflow_name):
        """Test that output contains no emojis."""
        result = execute_hdl_workflow(sample_workflow_name)
        
        emojis = ["🚀", "✅", "⚙️", "🎮"]
        for emoji in emojis:
            assert emoji not in result
    
    def test_tool_contains_execution_info(self, sample_workflow_name):
        """Test that output contains execution information."""
        result = execute_hdl_workflow(sample_workflow_name)
        
        result_lower = result.lower()
        assert any(word in result_lower for word in [
            "workflow", "execute", "run", "status", "step"
        ])
    
    def test_tool_output_structure(self, sample_workflow_name):
        """Test that output has proper structure."""
        result = execute_hdl_workflow(sample_workflow_name)
        
        assert isinstance(result, str)
        assert len(result) > 0


class TestGetWorkflowStatusTool:
    """Test suite for get_workflow_status tool function."""
    
    def test_tool_get_status(self, sample_workflow_name):
        """Test getting workflow status."""
        result = get_workflow_status(sample_workflow_name)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert sample_workflow_name in result
    
    def test_tool_status_format(self, sample_workflow_name):
        """Test status output format."""
        result = get_workflow_status(sample_workflow_name)
        
        result_lower = result.lower()
        # Should contain status-related information
        assert any(word in result_lower for word in [
            "status", "running", "completed", "pending", "workflow"
        ])
    
    def test_tool_no_emojis(self, sample_workflow_name):
        """Test that status output contains no emojis."""
        result = get_workflow_status(sample_workflow_name)
        
        emojis = ["📊", "✅", "⏳", "🔄"]
        for emoji in emojis:
            assert emoji not in result
    
    def test_tool_contains_details(self, sample_workflow_name):
        """Test that status contains details."""
        result = get_workflow_status(sample_workflow_name)
        
        assert isinstance(result, str)
        assert len(result) > 20  # Should have meaningful content


@pytest.mark.integration
class TestDPLCommanderIntegration:
    """Integration tests for DPL commander."""
    
    def test_workflow_execution_flow(self):
        """Test complete workflow execution flow."""
        workflow = "hdl-batch-test"
        
        # Execute workflow
        exec_result = execute_hdl_workflow(f"execute {workflow}")
        assert isinstance(exec_result, str)
        assert len(exec_result) > 0
        
        # Get status
        status_result = get_workflow_status(workflow)
        assert isinstance(status_result, str)
        assert workflow in status_result
    
    def test_multiple_workflow_types(self):
        """Test handling multiple workflow types."""
        workflows = [
            "hdl-batch-visits",
            "dpl-stream-visits",
            "hdl-quality-check"
        ]
        
        for workflow in workflows:
            result = execute_hdl_workflow(workflow)
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_workflow_with_parameters(self):
        """Test workflow execution with parameters."""
        result = execute_hdl_workflow(
            "execute hdl-batch-visits with date=2025-10-04 and environment=uat"
        )
        
        assert isinstance(result, str)
        assert len(result) > 0

