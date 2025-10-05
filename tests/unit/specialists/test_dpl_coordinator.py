"""
Unit tests for data_pipeline_agent_lib.specialists.hdl_coordinator module.
"""

import pytest
from data_pipeline_agent_lib.specialists.hdl_coordinator import coordinate_hdl_reprocessing


class TestDPLCoordinatorModule:
    """Test suite for hdl_coordinator module."""
    
    def test_tool_exists(self):
        """Test that coordinate_hdl_reprocessing tool exists."""
        assert callable(coordinate_hdl_reprocessing)


class TestCoordinateDPLReprocessingTool:
    """Test suite for coordinate_hdl_reprocessing tool function."""
    
    def test_tool_basic_call(self):
        """Test basic reprocessing coordination."""
        result = coordinate_hdl_reprocessing.invoke({
            "entity_name": "visits",
            "date_range": "2025-10-04",
            "notify_kpi_team": True
        })
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "visits" in result.lower()
    
    def test_tool_without_notification(self):
        """Test reprocessing without KPI team notification."""
        result = coordinate_hdl_reprocessing.invoke({
            "entity_name": "tasks",
            "date_range": "2025-10-04",
            "notify_kpi_team": False
        })
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_no_emojis(self):
        """Test that output contains no emojis."""
        result = coordinate_hdl_reprocessing.invoke({
            "entity_name": "visits",
            "date_range": "2025-10-04"
        })
        
        emojis = ["🔄", "📢", "⚡", "✅"]
        for emoji in emojis:
            assert emoji not in result
    
    def test_tool_contains_coordination_plan(self):
        """Test that output contains coordination plan."""
        result = coordinate_hdl_reprocessing.invoke({
            "entity_name": "visits",
            "date_range": "2025-10-04"
        })
        
        result_lower = result.lower()
        assert any(word in result_lower for word in [
            "step", "reprocess", "coordinate", "team", "notify"
        ])
    
    def test_tool_output_structure(self):
        """Test that output has proper structure."""
        result = coordinate_hdl_reprocessing.invoke({
            "entity_name": "visits",
            "date_range": "2025-10-04"
        })
        
        assert isinstance(result, str)
        assert len(result) > 50
        assert "\n" in result


@pytest.mark.integration
class TestDPLCoordinatorIntegration:
    """Integration tests for DPL coordinator."""
    
    def test_complete_reprocessing_workflow(self):
        """Test complete reprocessing workflow."""
        result = coordinate_hdl_reprocessing.invoke({
            "entity_name": "visits",
            "date_range": "2025-10-04",
            "notify_kpi_team": True
        })
        
        assert isinstance(result, str)
        assert len(result) > 100
        
        result_lower = result.lower()
        assert "visits" in result_lower
        assert any(word in result_lower for word in [
            "reprocess", "step", "team"
        ])
    
    def test_real_world_scenario(self):
        """Test real-world reprocessing scenario (Victor's memory)."""
        result = coordinate_hdl_reprocessing.invoke({
            "entity_name": "TASKS",
            "date_range": "2025-10-03",
            "notify_kpi_team": True
        })
        
        assert isinstance(result, str)
        assert len(result) > 100
        
        result_lower = result.lower()
        assert "tasks" in result_lower or "task" in result_lower
    
    def test_multiple_scenarios(self):
        """Test different reprocessing scenarios."""
        scenarios = [
            {"entity_name": "visits", "date_range": "2025-10-04", "notify_kpi_team": True},
            {"entity_name": "tasks", "date_range": "2025-10-03", "notify_kpi_team": False},
            {"entity_name": "orders", "date_range": "2025-10-02", "notify_kpi_team": True}
        ]
        
        for scenario in scenarios:
            result = coordinate_hdl_reprocessing.invoke(scenario)
            assert isinstance(result, str)
            assert len(result) > 0
