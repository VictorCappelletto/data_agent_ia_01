"""
DPL Retriever Service - RAG Integration

Provides centralized semantic search and context enhancement
for all DPL specialists. This service acts as the bridge between
specialists and the DPL knowledge base, enabling RAG-powered responses.
"""

from typing import List, Optional, Dict, Any
from ...infrastructure.vector_store import DPLRetriever
from ...utils import get_logger

logger = get_logger(__name__)


class DPLRetrieverService:
    """
    Centralized RAG service for DPL specialists.
    
    Provides semantic search capabilities and context enhancement
    to ensure specialists always provide DPL-specific knowledge
    rather than generic responses.
    """
    
    def __init__(self, retriever: DPLRetriever):
        """
        Initialize DPL retriever service.
        
        Args:
            retriever: DPL vector store retriever instance
            
        Raises:
            ValueError: If retriever is None
        """
        if retriever is None:
            raise ValueError("retriever cannot be None")
        
        self.retriever = retriever
        logger.info("DPL Retriever Service initialized")
    
    def search_error_patterns(
        self,
        error_message: str,
        entity_name: Optional[str] = None,
        pipeline_type: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar error patterns in DPL knowledge base.
        
        Performs semantic search to find relevant error patterns,
        troubleshooting guides, and resolution strategies from the
        DPL knowledge base.
        
        Args:
            error_message: Error message or description to search for
            entity_name: Optional DPL entity name for context (e.g., 'visits', 'tasks')
            pipeline_type: Optional pipeline type ('streaming' or 'batch')
            top_k: Number of top results to return (default: 5)
            
        Returns:
            List of dictionaries containing search results with:
            - content: Retrieved knowledge content
            - score: Relevance score (0-1)
            - source: Source document reference
            - metadata: Additional metadata
            
        Raises:
            ValueError: If error_message is empty
            RuntimeError: If search operation fails
            
        Example:
            >>> results = service.search_error_patterns(
            ...     error_message="Timeout in pipeline after 1h30m",
            ...     entity_name="visits",
            ...     pipeline_type="streaming",
            ...     top_k=3
            ... )
            >>> len(results)
            3
        """
        if not error_message or not error_message.strip():
            raise ValueError("error_message cannot be empty")
        
        logger.debug(
            "Searching error patterns",
            error_length=len(error_message),
            entity=entity_name,
            pipeline_type=pipeline_type,
            top_k=top_k
        )
        
        query = self._build_error_query(error_message, entity_name, pipeline_type)
        
        try:
            results = self.retriever.search(query, top_k=top_k)
            
            logger.info(
                "Error pattern search complete",
                results_found=len(results),
                query_length=len(query)
            )
            
            return results
            
        except Exception as e:
            logger.error(
                "Error pattern search failed",
                error_message=error_message[:100],
                exc_info=True
            )
            raise RuntimeError(f"Failed to search error patterns: {e}")
    
    def search_workflow_knowledge(
        self,
        workflow_name: str,
        include_config: bool = True,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search for workflow-specific knowledge and configuration.
        
        Retrieves documentation, configuration, and best practices
        for specific DPL workflows.
        
        Args:
            workflow_name: Name of the workflow (e.g., 'dpl-stream-visits')
            include_config: Whether to search for config details (default: True)
            top_k: Number of top results to return (default: 3)
            
        Returns:
            List of dictionaries containing workflow knowledge
            
        Raises:
            ValueError: If workflow_name is empty
            RuntimeError: If search operation fails
            
        Example:
            >>> results = service.search_workflow_knowledge(
            ...     workflow_name="dpl-stream-visits",
            ...     include_config=True
            ... )
        """
        if not workflow_name or not workflow_name.strip():
            raise ValueError("workflow_name cannot be empty")
        
        logger.debug(
            "Searching workflow knowledge",
            workflow=workflow_name,
            include_config=include_config,
            top_k=top_k
        )
        
        query = self._build_workflow_query(workflow_name, include_config)
        
        try:
            results = self.retriever.search(query, top_k=top_k)
            
            logger.info(
                "Workflow knowledge search complete",
                workflow=workflow_name,
                results_found=len(results)
            )
            
            return results
            
        except Exception as e:
            logger.error(
                "Workflow knowledge search failed",
                workflow=workflow_name,
                exc_info=True
            )
            raise RuntimeError(f"Failed to search workflow knowledge: {e}")
    
    def search_optimization_strategies(
        self,
        pipeline_name: str,
        performance_issue: str,
        top_k: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Search for performance optimization strategies.
        
        Finds relevant optimization techniques, best practices, and
        configuration tuning strategies for DPL pipelines.
        
        Args:
            pipeline_name: Name of the pipeline to optimize
            performance_issue: Description of the performance issue
            top_k: Number of top results to return (default: 4)
            
        Returns:
            List of dictionaries containing optimization strategies
            
        Raises:
            ValueError: If pipeline_name or performance_issue is empty
            RuntimeError: If search operation fails
            
        Example:
            >>> results = service.search_optimization_strategies(
            ...     pipeline_name="dpl-stream-visits",
            ...     performance_issue="High latency in silver processing"
            ... )
        """
        if not pipeline_name or not pipeline_name.strip():
            raise ValueError("pipeline_name cannot be empty")
        if not performance_issue or not performance_issue.strip():
            raise ValueError("performance_issue cannot be empty")
        
        logger.debug(
            "Searching optimization strategies",
            pipeline=pipeline_name,
            issue_length=len(performance_issue),
            top_k=top_k
        )
        
        query = self._build_optimization_query(pipeline_name, performance_issue)
        
        try:
            results = self.retriever.search(query, top_k=top_k)
            
            logger.info(
                "Optimization strategy search complete",
                pipeline=pipeline_name,
                results_found=len(results)
            )
            
            return results
            
        except Exception as e:
            logger.error(
                "Optimization strategy search failed",
                pipeline=pipeline_name,
                exc_info=True
            )
            raise RuntimeError(f"Failed to search optimization strategies: {e}")
    
    def search_component_documentation(
        self,
        component_name: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search for DPL component documentation and architecture details.
        
        Retrieves documentation about DPL components, classes, utilities,
        and architectural patterns.
        
        Args:
            component_name: Name of the component (e.g., 'BaseTable', 'IngestionControl')
            top_k: Number of top results to return (default: 3)
            
        Returns:
            List of dictionaries containing component documentation
            
        Raises:
            ValueError: If component_name is empty
            RuntimeError: If search operation fails
            
        Example:
            >>> results = service.search_component_documentation(
            ...     component_name="BaseTable"
            ... )
        """
        if not component_name or not component_name.strip():
            raise ValueError("component_name cannot be empty")
        
        logger.debug(
            "Searching component documentation",
            component=component_name,
            top_k=top_k
        )
        
        query = self._build_component_query(component_name)
        
        try:
            results = self.retriever.search(query, top_k=top_k)
            
            logger.info(
                "Component documentation search complete",
                component=component_name,
                results_found=len(results)
            )
            
            return results
            
        except Exception as e:
            logger.error(
                "Component documentation search failed",
                component=component_name,
                exc_info=True
            )
            raise RuntimeError(f"Failed to search component documentation: {e}")
    
    def search_quality_validation_rules(
        self,
        entity_name: str,
        quality_dimension: str = "all",
        top_k: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Search for data quality validation rules and checks.
        
        Finds quality validation rules, completeness checks, and
        data quality best practices for DPL entities.
        
        Args:
            entity_name: Name of the DPL entity (e.g., 'visits', 'tasks')
            quality_dimension: Quality dimension ('completeness', 'accuracy', 'all')
            top_k: Number of top results to return (default: 4)
            
        Returns:
            List of dictionaries containing quality validation rules
            
        Raises:
            ValueError: If entity_name is empty
            RuntimeError: If search operation fails
            
        Example:
            >>> results = service.search_quality_validation_rules(
            ...     entity_name="visits",
            ...     quality_dimension="completeness"
            ... )
        """
        if not entity_name or not entity_name.strip():
            raise ValueError("entity_name cannot be empty")
        
        logger.debug(
            "Searching quality validation rules",
            entity=entity_name,
            dimension=quality_dimension,
            top_k=top_k
        )
        
        query = self._build_quality_query(entity_name, quality_dimension)
        
        try:
            results = self.retriever.search(query, top_k=top_k)
            
            logger.info(
                "Quality validation rules search complete",
                entity=entity_name,
                results_found=len(results)
            )
            
            return results
            
        except Exception as e:
            logger.error(
                "Quality validation rules search failed",
                entity=entity_name,
                exc_info=True
            )
            raise RuntimeError(f"Failed to search quality validation rules: {e}")
    
    def enhance_context(
        self,
        search_results: List[Dict[str, Any]],
        max_length: int = 2000
    ) -> str:
        """
        Convert search results into enhanced context string for LLM.
        
        Formats search results into a clean, structured context that can be
        included in prompts to provide DPL-specific knowledge to the LLM.
        
        Args:
            search_results: List of search results from knowledge base
            max_length: Maximum length of context string (default: 2000)
            
        Returns:
            Formatted context string ready for LLM consumption
            
        Example:
            >>> context = service.enhance_context(search_results)
            >>> "RELEVANT DPL KNOWLEDGE" in context
            True
        """
        if not search_results:
            logger.debug("No search results to enhance")
            return "No specific DPL knowledge found for this query."
        
        logger.debug(
            "Enhancing context from search results",
            results_count=len(search_results),
            max_length=max_length
        )
        
        context_parts = ["=== RELEVANT DPL KNOWLEDGE ===\n"]
        current_length = len(context_parts[0])
        
        for i, result in enumerate(search_results, 1):
            source_info = result.get("source", "Unknown")
            content = result.get("content", "N/A")
            score = result.get("score", 0.0)
            
            # Format source entry
            entry = f"\n[Source {i}] (Relevance: {score:.2f})\n"
            entry += f"Document: {source_info}\n"
            entry += f"{content}\n"
            
            # Check length limit
            if current_length + len(entry) > max_length:
                logger.debug(
                    "Context length limit reached",
                    sources_included=i-1,
                    max_length=max_length
                )
                break
            
            context_parts.append(entry)
            current_length += len(entry)
        
        enhanced_context = "\n".join(context_parts)
        
        logger.info(
            "Context enhancement complete",
            sources_included=len(context_parts)-1,
            total_length=len(enhanced_context)
        )
        
        return enhanced_context
    
    # Private helper methods for building optimized queries
    
    def _build_error_query(
        self,
        error_message: str,
        entity_name: Optional[str],
        pipeline_type: Optional[str]
    ) -> str:
        """Build optimized search query for error patterns."""
        query_parts = [f"Error troubleshooting: {error_message}"]
        
        if entity_name:
            query_parts.append(f"entity: {entity_name}")
        
        if pipeline_type:
            query_parts.append(f"pipeline type: {pipeline_type}")
        
        return " ".join(query_parts)
    
    def _build_workflow_query(
        self,
        workflow_name: str,
        include_config: bool
    ) -> str:
        """Build optimized search query for workflow knowledge."""
        query_parts = [f"workflow: {workflow_name}"]
        
        if include_config:
            query_parts.extend([
                "configuration",
                "tasks",
                "triggers",
                "execution"
            ])
        else:
            query_parts.extend([
                "documentation",
                "overview",
                "purpose"
            ])
        
        return " ".join(query_parts)
    
    def _build_optimization_query(
        self,
        pipeline_name: str,
        performance_issue: str
    ) -> str:
        """Build optimized search query for optimization strategies."""
        return f"optimize performance {pipeline_name} {performance_issue} best practices tuning"
    
    def _build_component_query(self, component_name: str) -> str:
        """Build optimized search query for component documentation."""
        return f"component: {component_name} documentation architecture purpose usage"
    
    def _build_quality_query(
        self,
        entity_name: str,
        quality_dimension: str
    ) -> str:
        """Build optimized search query for quality validation rules."""
        query_parts = [
            f"data quality validation {entity_name}",
            quality_dimension if quality_dimension != "all" else "completeness accuracy consistency"
        ]
        
        return " ".join(query_parts)


# Singleton instance management
_retriever_service_instance: Optional[DPLRetrieverService] = None


def get_hdl_retriever_service(
    retriever: Optional[DPLRetriever] = None
) -> DPLRetrieverService:
    """
    Get or create singleton instance of DPL Retriever Service.
    
    Args:
        retriever: Optional DPL retriever instance. If not provided,
                  will use existing singleton or create with default retriever.
                  
    Returns:
        DPL Retriever Service singleton instance
        
    Raises:
        RuntimeError: If no retriever provided and singleton doesn't exist
        
    Example:
        >>> service = get_hdl_retriever_service()
        >>> results = service.search_error_patterns("Timeout error")
    """
    global _retriever_service_instance
    
    if _retriever_service_instance is None:
        if retriever is None:
            # Import here to avoid circular dependency
            from ...infrastructure.vector_store import get_hdl_retriever
            retriever = get_hdl_retriever()
        
        _retriever_service_instance = DPLRetrieverService(retriever)
        logger.info("Created DPL Retriever Service singleton")
    
    return _retriever_service_instance

