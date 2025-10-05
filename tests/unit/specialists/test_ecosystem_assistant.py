"""
Unit tests for data_pipeline_agent_lib.specialists.ecosystem_assistant module.
"""

import pytest
from data_pipeline_agent_lib.specialists.ecosystem_assistant import (
    explain_hdl_component,
    get_hdl_best_practices
)


class TestEcosystemAssistantModule:
    """Test suite for ecosystem_assistant module."""
    
    def test_explain_component_exists(self):
        """Test that explain_hdl_component tool exists."""
        assert callable(explain_hdl_component)
    
    def test_get_practices_exists(self):
        """Test that get_hdl_best_practices tool exists."""
        assert callable(get_hdl_best_practices)


class TestExplainDPLComponentTool:
    """Test suite for explain_hdl_component tool function."""
    
    def test_tool_explain_streaming(self):
        """Test explaining streaming component."""
        result = explain_hdl_component("streaming pipeline")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "stream" in result.lower()
    
    def test_tool_explain_batch(self):
        """Test explaining batch component."""
        result = explain_hdl_component("batch ingestion")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_explain_bronze(self):
        """Test explaining bronze layer."""
        result = explain_hdl_component("bronze layer")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "bronze" in result.lower()
    
    def test_tool_explain_silver(self):
        """Test explaining silver layer."""
        result = explain_hdl_component("silver layer")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_explain_scd2(self):
        """Test explaining SCD2."""
        result = explain_hdl_component("SCD2")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_no_emojis(self):
        """Test that output contains no emojis."""
        result = explain_hdl_component("bronze layer")
        
        emojis = ["📚", "💡", "🔍", "📖"]
        for emoji in emojis:
            assert emoji not in result
    
    def test_tool_contains_explanation(self):
        """Test that output contains explanation."""
        result = explain_hdl_component("streaming pipeline")
        
        assert isinstance(result, str)
        assert len(result) > 50  # Should be explanatory
    
    def test_tool_unknown_component(self):
        """Test explaining unknown component."""
        result = explain_hdl_component("unknown_component_xyz")
        
        assert isinstance(result, str)
        assert len(result) > 0


class TestGetDPLBestPracticesTool:
    """Test suite for get_hdl_best_practices tool function."""
    
    def test_tool_get_streaming_practices(self):
        """Test getting streaming best practices."""
        result = get_hdl_best_practices("streaming")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "stream" in result.lower() or "practice" in result.lower()
    
    def test_tool_get_batch_practices(self):
        """Test getting batch best practices."""
        result = get_hdl_best_practices("batch")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_get_quality_practices(self):
        """Test getting quality best practices."""
        result = get_hdl_best_practices("data quality")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_get_performance_practices(self):
        """Test getting performance best practices."""
        result = get_hdl_best_practices("performance")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_no_emojis(self):
        """Test that output contains no emojis."""
        result = get_hdl_best_practices("streaming")
        
        emojis = ["✓", "✅", "📋", "💡"]
        for emoji in emojis:
            assert emoji not in result
    
    def test_tool_contains_practices(self):
        """Test that output contains practices."""
        result = get_hdl_best_practices("streaming")
        
        result_lower = result.lower()
        assert any(word in result_lower for word in [
            "practice", "should", "recommend", "best", "guideline"
        ])
    
    def test_tool_generic_request(self):
        """Test generic best practices request."""
        result = get_hdl_best_practices("general")
        
        assert isinstance(result, str)
        assert len(result) > 0


@pytest.mark.integration
class TestEcosystemAssistantIntegration:
    """Integration tests for ecosystem assistant."""
    
    def test_component_explanation_quality(self):
        """Test quality of component explanations."""
        components = ["streaming", "batch", "bronze", "silver", "SCD2"]
        
        for component in components:
            result = explain_hdl_component(component)
            assert isinstance(result, str)
            assert len(result) > 30  # Should be explanatory
    
    def test_best_practices_quality(self):
        """Test quality of best practices."""
        topics = ["streaming", "batch", "performance", "quality"]
        
        for topic in topics:
            result = get_hdl_best_practices(topic)
            assert isinstance(result, str)
            assert len(result) > 30
    
    def test_comprehensive_documentation(self):
        """Test comprehensive documentation access."""
        # Explain component
        explanation = explain_hdl_component("streaming pipeline")
        assert len(explanation) > 50
        
        # Get best practices
        practices = get_hdl_best_practices("streaming")
        assert len(practices) > 50
        
        # Both should be informative
        assert explanation != practices  # Different content

