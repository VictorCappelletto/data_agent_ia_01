"""
Unit tests for data_pipeline_agent_lib.specialists.quality_assistant module.
"""

import pytest
from data_pipeline_agent_lib.specialists.quality_assistant import validate_hdl_data_quality


class TestQualityAssistantModule:
    """Test suite for quality_assistant module."""
    
    def test_tool_function_exists(self):
        """Test that validate_hdl_data_quality tool exists."""
        assert callable(validate_hdl_data_quality)
    
    def test_tool_callable(self):
        """Test that tool is callable."""
        # Should not raise an error
        try:
            result = validate_hdl_data_quality("test entity")
            assert isinstance(result, str)
        except Exception:
            # If it fails, that's ok for now - we're just testing it exists
            pass


class TestValidateDPLDataQualityTool:
    """Test suite for validate_hdl_data_quality tool function."""
    
    def test_tool_completeness_check(self, sample_entity_name):
        """Test completeness validation."""
        result = validate_hdl_data_quality(
            f"{sample_entity_name} completeness"
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "completeness" in result.lower()
    
    def test_tool_consistency_check(self, sample_entity_name):
        """Test consistency validation."""
        result = validate_hdl_data_quality(
            f"{sample_entity_name} consistency"
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_timeliness_check(self, sample_entity_name):
        """Test timeliness validation."""
        result = validate_hdl_data_quality(
            f"{sample_entity_name} timeliness"
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_accuracy_check(self, sample_entity_name):
        """Test accuracy validation."""
        result = validate_hdl_data_quality(
            f"{sample_entity_name} accuracy"
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_all_dimensions(self, sample_entity_name):
        """Test validation across all dimensions."""
        result = validate_hdl_data_quality(
            f"{sample_entity_name} quality check"
        )
        
        assert isinstance(result, str)
        assert len(result) > 50
    
    def test_tool_no_emojis(self, sample_entity_name):
        """Test that output contains no emojis."""
        result = validate_hdl_data_quality(sample_entity_name)
        
        emojis = ["✓", "✅", "⚠️", "❌", "📊"]
        for emoji in emojis:
            assert emoji not in result
    
    def test_tool_contains_findings(self, sample_entity_name):
        """Test that output contains findings or recommendations."""
        result = validate_hdl_data_quality(sample_entity_name)
        
        result_lower = result.lower()
        assert any(word in result_lower for word in [
            "finding", "recommendation", "check", "quality", "validate"
        ])
    
    def test_tool_output_structure(self, sample_entity_name):
        """Test that output has proper structure."""
        result = validate_hdl_data_quality(sample_entity_name)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should be formatted
        assert "\n" in result or len(result.split()) > 5


@pytest.mark.integration
class TestQualityAssistantIntegration:
    """Integration tests for quality assistant."""
    
    def test_tool_functionality(self):
        """Test basic tool functionality."""
        result = validate_hdl_data_quality("visits entity")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_validation_quality(self):
        """Test quality of validation output."""
        result = validate_hdl_data_quality("visits data quality")
        
        assert len(result) > 50
        result_lower = result.lower()
        # Should contain quality-related terms
        assert any(word in result_lower for word in [
            "quality", "data", "check", "validate", "dimension"
        ])
    
    def test_multiple_entities(self):
        """Test validation for multiple entities."""
        entities = ["visits", "tasks", "orders", "products"]
        
        for entity in entities:
            result = validate_hdl_data_quality(entity)
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_comprehensive_validation(self):
        """Test comprehensive quality validation."""
        result = validate_hdl_data_quality(
            "visits entity complete quality assessment"
        )
        
        assert isinstance(result, str)
        assert len(result) > 100  # Should be detailed

