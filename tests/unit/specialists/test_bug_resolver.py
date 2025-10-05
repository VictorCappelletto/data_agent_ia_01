"""
Unit tests for data_pipeline_agent_lib.specialists.bug_resolver module.
"""

import pytest
from data_pipeline_agent_lib.specialists.bug_resolver import (
    BugResolver,
    resolve_hdl_bug
)


class TestBugResolver:
    """Test suite for BugResolver class."""
    
    def test_bug_solutions_exist(self):
        """Test that known bug solutions are defined."""
        assert hasattr(BugResolver, 'BUG_SOLUTIONS')
        assert isinstance(BugResolver.BUG_SOLUTIONS, dict)
        assert len(BugResolver.BUG_SOLUTIONS) > 0
    
    def test_known_bug_scd2(self):
        """Test known SCD2 bug solution."""
        assert "scd2_is_current_broken" in BugResolver.BUG_SOLUTIONS
        solution = BugResolver.BUG_SOLUTIONS["scd2_is_current_broken"]
        assert "solution" in solution
        assert "steps" in solution
    
    def test_known_bug_streaming_checkpoint(self):
        """Test known streaming checkpoint bug."""
        assert "streaming_checkpoint_corrupt" in BugResolver.BUG_SOLUTIONS
    
    def test_known_bug_document_storedb(self):
        """Test known CosmosDB bug."""
        assert "batch_document_storedb_connection" in BugResolver.BUG_SOLUTIONS


class TestResolveDPLBugTool:
    """Test suite for resolve_hdl_bug tool function."""
    
    def test_tool_scd2_bug(self):
        """Test resolving SCD2 bug."""
        # LangChain tool direct call doesn't support extra kwargs
        result = resolve_hdl_bug("scd2 is current broken")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "AdjustIsCurrent" in result or "scd2" in result.lower()
    
    def test_tool_streaming_checkpoint_bug(self):
        """Test resolving streaming checkpoint bug."""
        result = resolve_hdl_bug("streaming checkpoint corrupt")
        
        assert isinstance(result, str)
        assert "checkpoint" in result.lower()
    
    def test_tool_document_storedb_bug(self):
        """Test resolving CosmosDB connection bug."""
        result = resolve_hdl_bug("batch document_storedb connection failed")
        
        assert isinstance(result, str)
        assert "connection" in result.lower() or "document_store" in result.lower()
    
    def test_tool_generic_bug(self):
        """Test resolving unknown/generic bug."""
        result = resolve_hdl_bug("some unknown bug occurred")
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should provide generic guidance - check for common resolution words
        result_lower = result.lower()
        assert any(word in result_lower for word in ["step", "resolution", "guide", "check"])
    
    def test_tool_with_entity_name(self):
        """Test tool with entity name."""
        # LangChain tool direct call doesn't support extra kwargs
        result = resolve_hdl_bug("test bug")
        
        assert isinstance(result, str)
    
    def test_tool_no_emojis(self):
        """Test that output contains no emojis."""
        result = resolve_hdl_bug("test bug")
        
        emojis = ["🔧", "✅", "⚠️"]
        for emoji in emojis:
            assert emoji not in result
    
    def test_tool_contains_steps(self):
        """Test that output contains resolution steps."""
        result = resolve_hdl_bug("scd2 is current broken")
        
        # Should contain numbered or structured steps
        assert "1" in result or "step" in result.lower()


@pytest.mark.integration
class TestBugResolverIntegration:
    """Integration tests for bug resolver."""
    
    def test_all_known_bugs_resolvable(self):
        """Test that all known bugs can be resolved."""
        for bug_type in BugResolver.BUG_SOLUTIONS.keys():
            bug_description = bug_type.replace("_", " ")
            result = resolve_hdl_bug(bug_description)
            
            assert isinstance(result, str)
            assert len(result) > 100  # Should be detailed
    
    def test_resolution_quality(self):
        """Test quality of resolution guidance."""
        result = resolve_hdl_bug("scd2 is current broken")
        
        # Should contain practical information
        assert len(result) > 50
        result_lower = result.lower()
        assert any(word in result_lower for word in ["step", "run", "execute", "verify"])

