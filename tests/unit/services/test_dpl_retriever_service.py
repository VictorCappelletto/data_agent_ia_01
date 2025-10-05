"""
Unit tests for DPL Retriever Service.

Tests the RAG integration service that provides semantic search
and context enhancement for DPL specialists.
"""

import pytest
from unittest.mock import Mock, MagicMock
from data_pipeline_agent_lib.application.services import (
    DPLRetrieverService,
    get_hdl_retriever_service,
)


class TestDPLRetrieverServiceInitialization:
    """Test suite for DPL Retriever Service initialization."""
    
    def test_init_with_valid_retriever(self):
        """Test initialization with valid retriever instance."""
        mock_retriever = Mock()
        service = DPLRetrieverService(mock_retriever)
        
        assert service.retriever is mock_retriever
    
    def test_init_with_none_retriever_raises_error(self):
        """Test that None retriever raises ValueError."""
        with pytest.raises(ValueError, match="retriever cannot be None"):
            DPLRetrieverService(None)


class TestSearchErrorPatterns:
    """Test suite for error pattern search."""
    
    @pytest.fixture
    def mock_retriever(self):
        """Create mock retriever with search results."""
        retriever = Mock()
        retriever.search.return_value = [
            {
                "content": "Timeout error in streaming pipeline",
                "score": 0.95,
                "source": "hdl_troubleshooting.md"
            },
            {
                "content": "Common causes of pipeline timeouts",
                "score": 0.87,
                "source": "hdl_common_issues.md"
            }
        ]
        return retriever
    
    @pytest.fixture
    def service(self, mock_retriever):
        """Create service instance with mock retriever."""
        return DPLRetrieverService(mock_retriever)
    
    def test_search_error_patterns_with_entity(
        self,
        service,
        mock_retriever
    ):
        """Test error pattern search with entity context."""
        error_msg = "Timeout in pipeline"
        entity = "visits"
        
        results = service.search_error_patterns(
            error_message=error_msg,
            entity_name=entity,
            top_k=3
        )
        
        assert len(results) == 2
        mock_retriever.search.assert_called_once()
        
        call_query = mock_retriever.search.call_args[0][0]
        assert "visits" in call_query
        assert "Timeout" in call_query
    
    def test_search_error_patterns_with_pipeline_type(
        self,
        service,
        mock_retriever
    ):
        """Test error pattern search with pipeline type context."""
        results = service.search_error_patterns(
            error_message="Connection timeout",
            pipeline_type="streaming",
            top_k=2
        )
        
        assert len(results) == 2
        call_query = mock_retriever.search.call_args[0][0]
        assert "streaming" in call_query
    
    def test_search_error_patterns_empty_message_raises_error(
        self,
        service
    ):
        """Test that empty error message raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.search_error_patterns(error_message="")
    
    def test_search_error_patterns_whitespace_only_raises_error(
        self,
        service
    ):
        """Test that whitespace-only message raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.search_error_patterns(error_message="   ")
    
    def test_search_error_patterns_retriever_exception(
        self,
        service,
        mock_retriever
    ):
        """Test that retriever exceptions are wrapped."""
        mock_retriever.search.side_effect = Exception("Search failed")
        
        with pytest.raises(RuntimeError, match="Failed to search error patterns"):
            service.search_error_patterns("Some error")


class TestSearchWorkflowKnowledge:
    """Test suite for workflow knowledge search."""
    
    @pytest.fixture
    def mock_retriever(self):
        """Create mock retriever with workflow results."""
        retriever = Mock()
        retriever.search.return_value = [
            {
                "content": "dpl-stream-visits workflow configuration",
                "score": 0.93,
                "source": "workflow_visits.md"
            }
        ]
        return retriever
    
    @pytest.fixture
    def service(self, mock_retriever):
        """Create service instance with mock retriever."""
        return DPLRetrieverService(mock_retriever)
    
    def test_search_workflow_knowledge_with_config(
        self,
        service,
        mock_retriever
    ):
        """Test workflow search including configuration."""
        results = service.search_workflow_knowledge(
            workflow_name="dpl-stream-visits",
            include_config=True
        )
        
        assert len(results) == 1
        call_query = mock_retriever.search.call_args[0][0]
        assert "dpl-stream-visits" in call_query
        assert "configuration" in call_query
    
    def test_search_workflow_knowledge_without_config(
        self,
        service,
        mock_retriever
    ):
        """Test workflow search without configuration details."""
        results = service.search_workflow_knowledge(
            workflow_name="dpl-stream-visits",
            include_config=False
        )
        
        call_query = mock_retriever.search.call_args[0][0]
        assert "documentation" in call_query
        assert "configuration" not in call_query
    
    def test_search_workflow_knowledge_empty_name_raises_error(
        self,
        service
    ):
        """Test that empty workflow name raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.search_workflow_knowledge(workflow_name="")


class TestSearchOptimizationStrategies:
    """Test suite for optimization strategy search."""
    
    @pytest.fixture
    def mock_retriever(self):
        """Create mock retriever with optimization results."""
        retriever = Mock()
        retriever.search.return_value = [
            {
                "content": "Optimize streaming checkpoint configuration",
                "score": 0.89,
                "source": "optimization_guide.md"
            }
        ]
        return retriever
    
    @pytest.fixture
    def service(self, mock_retriever):
        """Create service instance with mock retriever."""
        return DPLRetrieverService(mock_retriever)
    
    def test_search_optimization_strategies_success(
        self,
        service,
        mock_retriever
    ):
        """Test optimization strategy search."""
        results = service.search_optimization_strategies(
            pipeline_name="dpl-stream-visits",
            performance_issue="High latency"
        )
        
        assert len(results) == 1
        call_query = mock_retriever.search.call_args[0][0]
        assert "dpl-stream-visits" in call_query
        assert "High latency" in call_query
    
    def test_search_optimization_empty_pipeline_raises_error(
        self,
        service
    ):
        """Test that empty pipeline name raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.search_optimization_strategies(
                pipeline_name="",
                performance_issue="Slow"
            )
    
    def test_search_optimization_empty_issue_raises_error(
        self,
        service
    ):
        """Test that empty performance issue raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.search_optimization_strategies(
                pipeline_name="test-pipeline",
                performance_issue=""
            )


class TestSearchComponentDocumentation:
    """Test suite for component documentation search."""
    
    @pytest.fixture
    def mock_retriever(self):
        """Create mock retriever with component results."""
        retriever = Mock()
        retriever.search.return_value = [
            {
                "content": "BaseTable is the abstract parent class",
                "score": 0.91,
                "source": "hdl_BaseTable.md"
            }
        ]
        return retriever
    
    @pytest.fixture
    def service(self, mock_retriever):
        """Create service instance with mock retriever."""
        return DPLRetrieverService(mock_retriever)
    
    def test_search_component_documentation_success(
        self,
        service,
        mock_retriever
    ):
        """Test component documentation search."""
        results = service.search_component_documentation(
            component_name="BaseTable"
        )
        
        assert len(results) == 1
        call_query = mock_retriever.search.call_args[0][0]
        assert "BaseTable" in call_query
    
    def test_search_component_empty_name_raises_error(
        self,
        service
    ):
        """Test that empty component name raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.search_component_documentation(component_name="")


class TestSearchQualityValidationRules:
    """Test suite for quality validation rules search."""
    
    @pytest.fixture
    def mock_retriever(self):
        """Create mock retriever with quality rules results."""
        retriever = Mock()
        retriever.search.return_value = [
            {
                "content": "Completeness validation for visits entity",
                "score": 0.88,
                "source": "quality_validations.md"
            }
        ]
        return retriever
    
    @pytest.fixture
    def service(self, mock_retriever):
        """Create service instance with mock retriever."""
        return DPLRetrieverService(mock_retriever)
    
    def test_search_quality_rules_with_dimension(
        self,
        service,
        mock_retriever
    ):
        """Test quality rules search with specific dimension."""
        results = service.search_quality_validation_rules(
            entity_name="visits",
            quality_dimension="completeness"
        )
        
        assert len(results) == 1
        call_query = mock_retriever.search.call_args[0][0]
        assert "visits" in call_query
        assert "completeness" in call_query
    
    def test_search_quality_rules_all_dimensions(
        self,
        service,
        mock_retriever
    ):
        """Test quality rules search for all dimensions."""
        results = service.search_quality_validation_rules(
            entity_name="tasks",
            quality_dimension="all"
        )
        
        call_query = mock_retriever.search.call_args[0][0]
        assert "completeness" in call_query
        assert "accuracy" in call_query
    
    def test_search_quality_empty_entity_raises_error(
        self,
        service
    ):
        """Test that empty entity name raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.search_quality_validation_rules(entity_name="")


class TestEnhanceContext:
    """Test suite for context enhancement."""
    
    @pytest.fixture
    def service(self):
        """Create service instance with mock retriever."""
        mock_retriever = Mock()
        return DPLRetrieverService(mock_retriever)
    
    def test_enhance_context_with_results(self, service):
        """Test context enhancement with search results."""
        search_results = [
            {
                "content": "First knowledge item",
                "score": 0.95,
                "source": "doc1.md"
            },
            {
                "content": "Second knowledge item",
                "score": 0.87,
                "source": "doc2.md"
            }
        ]
        
        context = service.enhance_context(search_results)
        
        assert "RELEVANT DPL KNOWLEDGE" in context
        assert "First knowledge item" in context
        assert "Second knowledge item" in context
        assert "doc1.md" in context
        assert "0.95" in context
    
    def test_enhance_context_empty_results(self, service):
        """Test context enhancement with no results."""
        context = service.enhance_context([])
        
        assert "No specific DPL knowledge found" in context
    
    def test_enhance_context_respects_max_length(self, service):
        """Test that context enhancement respects max length."""
        long_content = "A" * 1000
        search_results = [
            {"content": long_content, "score": 0.9, "source": "doc1.md"},
            {"content": long_content, "score": 0.8, "source": "doc2.md"},
            {"content": long_content, "score": 0.7, "source": "doc3.md"}
        ]
        
        context = service.enhance_context(search_results, max_length=1500)
        
        assert len(context) <= 1500
        assert "doc1.md" in context


class TestGetDPLRetrieverService:
    """Test suite for singleton getter function."""
    
    def test_get_service_with_retriever(self):
        """Test getting service with provided retriever."""
        mock_retriever = Mock()
        service = get_hdl_retriever_service(mock_retriever)
        
        assert isinstance(service, DPLRetrieverService)
        assert service.retriever is mock_retriever
    
    def test_get_service_returns_singleton(self):
        """Test that multiple calls return same instance."""
        mock_retriever = Mock()
        service1 = get_hdl_retriever_service(mock_retriever)
        service2 = get_hdl_retriever_service()
        
        assert service1 is service2

