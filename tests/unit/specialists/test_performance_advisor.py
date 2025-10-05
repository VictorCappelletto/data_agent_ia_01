"""
Unit tests for data_pipeline_agent_lib.specialists.performance_advisor module.
"""

import pytest
from data_pipeline_agent_lib.specialists.performance_advisor import (
    PerformanceAdvisor,
    optimize_hdl_pipeline
)


class TestPerformanceAdvisorClass:
    """Test suite for PerformanceAdvisor class."""
    
    def test_optimization_strategies_exist(self):
        """Test that optimization strategies are defined."""
        assert hasattr(PerformanceAdvisor, 'OPTIMIZATION_STRATEGIES')
        assert isinstance(PerformanceAdvisor.OPTIMIZATION_STRATEGIES, dict)
        assert len(PerformanceAdvisor.OPTIMIZATION_STRATEGIES) > 0
    
    def test_strategy_slow_execution(self):
        """Test strategy for slow execution."""
        assert "slow_execution" in PerformanceAdvisor.OPTIMIZATION_STRATEGIES
        strategy = PerformanceAdvisor.OPTIMIZATION_STRATEGIES["slow_execution"]
        assert isinstance(strategy, list)
    
    def test_strategy_low_throughput(self):
        """Test strategy for low throughput."""
        assert "low_throughput" in PerformanceAdvisor.OPTIMIZATION_STRATEGIES
    
    def test_strategy_memory_issues(self):
        """Test strategy for memory issues."""
        # Strategy might be named differently
        strategies = PerformanceAdvisor.OPTIMIZATION_STRATEGIES
        assert any("memory" in key.lower() for key in strategies.keys())


class TestOptimizeDPLPipelineTool:
    """Test suite for optimize_hdl_pipeline tool function."""
    
    def test_tool_basic_call(self):
        """Test basic tool call."""
        # LangChain tools when called directly expect a dict matching their schema
        result = optimize_hdl_pipeline.invoke({
            "pipeline_name": "test-pipeline",
            "performance_issue": "slow execution"
        })
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_tool_no_emojis(self):
        """Test that output contains no emojis."""
        result = optimize_hdl_pipeline.invoke({
            "pipeline_name": "test-pipeline",
            "performance_issue": "general optimization"
        })
        
        emojis = ["⚡", "🚀", "💡", "📈"]
        for emoji in emojis:
            assert emoji not in result
    
    def test_tool_contains_recommendations(self):
        """Test that output contains recommendations."""
        result = optimize_hdl_pipeline.invoke({
            "pipeline_name": "test-pipeline",
            "performance_issue": "slow execution"
        })
        
        result_lower = result.lower()
        assert any(word in result_lower for word in [
            "recommendation", "optimize", "improve", "performance"
        ])


@pytest.mark.integration
class TestPerformanceAdvisorIntegration:
    """Integration tests for performance advisor."""
    
    def test_all_strategies_accessible(self):
        """Test that all optimization strategies can be accessed."""
        strategies = PerformanceAdvisor.OPTIMIZATION_STRATEGIES
        
        for strategy_name, strategy_list in strategies.items():
            assert isinstance(strategy_list, list)
            assert len(strategy_list) > 0
    
    def test_optimization_quality(self):
        """Test quality of optimization recommendations."""
        result = optimize_hdl_pipeline.invoke({
            "pipeline_name": "test-pipeline",
            "performance_issue": "pipeline is very slow"
        })
        
        assert len(result) > 100
        result_lower = result.lower()
        assert any(word in result_lower for word in [
            "partition", "cache", "optimize", "performance",
            "memory", "cpu", "resource"
        ])
    
    def test_multiple_issue_types(self):
        """Test handling multiple performance issue types."""
        issues = [
            "slow execution",
            "high latency",
            "resource intensive",
            "memory issues"
        ]
        
        for issue in issues:
            result = optimize_hdl_pipeline.invoke({
                "pipeline_name": "test-pipeline",
                "performance_issue": issue
            })
            assert isinstance(result, str)
            assert len(result) > 0
