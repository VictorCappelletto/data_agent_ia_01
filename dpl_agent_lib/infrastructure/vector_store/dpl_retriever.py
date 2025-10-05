"""
DPL Agent v3.0 - DPL-Specific Retriever

Specialized retriever for DPL knowledge with context enhancement,
filtering, and relevance scoring.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from langchain.schema import Document


@dataclass
class RetrievalContext:
    """Context for knowledge retrieval."""
    query: str
    entity_name: Optional[str] = None
    pipeline_type: Optional[str] = None  # "streaming" or "batch"
    layer: Optional[str] = None  # "bronze" or "silver"
    category: Optional[str] = None  # "troubleshooting", "architecture", etc.
    include_related: bool = True
    top_k: int = 5


@dataclass
class RetrievalResult:
    """Result from knowledge retrieval."""
    documents: List[Document]
    query: str
    filters_applied: Dict[str, Any]
    total_results: int
    context_summary: str


class DPLRetriever:
    """
    DPL-specific knowledge retriever.
    
    Features:
    - Context-aware filtering
    - Entity-specific search
    - Pipeline type filtering
    - Relevance scoring
    - Context enhancement
    """
    
    def __init__(self, vector_store):
        """
        Initialize DPL retriever.
        
        Args:
            vector_store: VectorStorePort implementation
        """
        self.vector_store = vector_store
        
        # Category mappings for DPL knowledge
        self.category_keywords = {
            "troubleshooting": [
                "error", "failure", "timeout", "debug", "fix", "resolve",
                "problem", "issue", "diagnose"
            ],
            "architecture": [
                "structure", "design", "component", "layer", "pipeline",
                "workflow", "architecture", "overview"
            ],
            "best_practices": [
                "best practice", "recommendation", "guideline", "pattern",
                "optimization", "performance"
            ],
            "hdl_architecture": [
                "hdl", "bronze", "silver", "streaming", "batch", "scd2",
                "delta", "table", "entity"
            ]
        }
    
    async def retrieve(
        self,
        context: RetrievalContext
    ) -> RetrievalResult:
        """
        Retrieve relevant knowledge based on context.
        
        Args:
            context: Retrieval context with query and filters
            
        Returns:
            RetrievalResult with documents and metadata
        """
        # Build filters
        filters = self._build_filters(context)
        
        # Enhance query with context
        enhanced_query = self._enhance_query(context)
        
        # Perform search
        documents = await self.vector_store.search(
            query=enhanced_query,
            top_k=context.top_k,
            filters=filters if filters else None
        )
        
        # Convert to Document objects
        doc_objects = [
            Document(
                page_content=doc["content"],
                metadata=doc["metadata"]
            )
            for doc in documents
        ]
        
        # Generate context summary
        context_summary = self._generate_context_summary(
            doc_objects,
            context
        )
        
        return RetrievalResult(
            documents=doc_objects,
            query=context.query,
            filters_applied=filters,
            total_results=len(doc_objects),
            context_summary=context_summary
        )
    
    async def retrieve_with_scores(
        self,
        context: RetrievalContext
    ) -> Tuple[RetrievalResult, List[float]]:
        """
        Retrieve with similarity scores.
        
        Args:
            context: Retrieval context
            
        Returns:
            Tuple of (RetrievalResult, scores)
        """
        # Build filters
        filters = self._build_filters(context)
        
        # Enhance query
        enhanced_query = self._enhance_query(context)
        
        # Perform search with scores
        results = await self.vector_store.search_with_scores(
            query=enhanced_query,
            top_k=context.top_k,
            filters=filters if filters else None
        )
        
        # Separate documents and scores
        documents = [
            Document(
                page_content=result["content"],
                metadata=result["metadata"]
            )
            for result in results
        ]
        
        scores = [result["score"] for result in results]
        
        # Generate context summary
        context_summary = self._generate_context_summary(documents, context)
        
        retrieval_result = RetrievalResult(
            documents=documents,
            query=context.query,
            filters_applied=filters,
            total_results=len(documents),
            context_summary=context_summary
        )
        
        return retrieval_result, scores
    
    def _build_filters(self, context: RetrievalContext) -> Dict[str, Any]:
        """
        Build metadata filters from context.
        
        Args:
            context: Retrieval context
            
        Returns:
            Metadata filters dictionary
        """
        filters = {}
        
        if context.category:
            filters["category"] = context.category
        
        # Note: Additional filters can be added based on metadata structure
        # For now, category is the main filter
        
        return filters
    
    def _enhance_query(self, context: RetrievalContext) -> str:
        """
        Enhance query with context information.
        
        Args:
            context: Retrieval context
            
        Returns:
            Enhanced query string
        """
        query_parts = [context.query]
        
        # Add entity name if provided
        if context.entity_name:
            query_parts.append(f"entity: {context.entity_name}")
        
        # Add pipeline type if provided
        if context.pipeline_type:
            query_parts.append(f"pipeline type: {context.pipeline_type}")
        
        # Add layer if provided
        if context.layer:
            query_parts.append(f"layer: {context.layer}")
        
        return " ".join(query_parts)
    
    def _generate_context_summary(
        self,
        documents: List[Document],
        context: RetrievalContext
    ) -> str:
        """
        Generate summary of retrieval context.
        
        Args:
            documents: Retrieved documents
            metadata: Retrieval metadata
            
        Returns:
            Context summary string
        """
        if not documents:
            return "No relevant documentation found."
        
        # Count documents by category
        categories = {}
        for doc in documents:
            cat = doc.metadata.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        
        # Build summary
        summary_parts = [
            f"Found {len(documents)} relevant documents"
        ]
        
        if categories:
            cat_summary = ", ".join([f"{count} {cat}" for cat, count in categories.items()])
            summary_parts.append(f"Categories: {cat_summary}")
        
        if context.entity_name:
            summary_parts.append(f"Entity: {context.entity_name}")
        
        if context.pipeline_type:
            summary_parts.append(f"Pipeline type: {context.pipeline_type}")
        
        return ". ".join(summary_parts) + "."
    
    async def retrieve_for_troubleshooting(
        self,
        error_message: str,
        entity_name: Optional[str] = None,
        pipeline_type: Optional[str] = None
    ) -> RetrievalResult:
        """
        Specialized retrieval for troubleshooting.
        
        Args:
            error_message: Error message or description
            entity_name: Optional entity name
            pipeline_type: Optional pipeline type
            
        Returns:
            RetrievalResult focused on troubleshooting
        """
        context = RetrievalContext(
            query=error_message,
            entity_name=entity_name,
            pipeline_type=pipeline_type,
            category="troubleshooting",
            top_k=5
        )
        
        return await self.retrieve(context)
    
    async def retrieve_for_architecture(
        self,
        query: str,
        entity_name: Optional[str] = None
    ) -> RetrievalResult:
        """
        Specialized retrieval for architecture questions.
        
        Args:
            query: Architecture-related query
            entity_name: Optional entity name
            
        Returns:
            RetrievalResult focused on architecture
        """
        context = RetrievalContext(
            query=query,
            entity_name=entity_name,
            category="hdl_architecture",
            top_k=5
        )
        
        return await self.retrieve(context)
    
    async def retrieve_for_best_practices(
        self,
        query: str,
        pipeline_type: Optional[str] = None
    ) -> RetrievalResult:
        """
        Specialized retrieval for best practices.
        
        Args:
            query: Best practice query
            pipeline_type: Optional pipeline type
            
        Returns:
            RetrievalResult focused on best practices
        """
        context = RetrievalContext(
            query=query,
            pipeline_type=pipeline_type,
            category="best_practices",
            top_k=5
        )
        
        return await self.retrieve(context)
    
    def format_documents_for_llm(
        self,
        documents: List[Document],
        max_chars: int = 4000
    ) -> str:
        """
        Format retrieved documents for LLM context.
        
        Args:
            documents: List of documents
            max_chars: Maximum characters to return
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "No relevant documentation available."
        
        context_parts = []
        total_chars = 0
        
        for i, doc in enumerate(documents, 1):
            # Format document
            source = doc.metadata.get("source", "unknown")
            category = doc.metadata.get("category", "unknown")
            
            doc_text = f"\n--- Document {i} ({category}) ---\n"
            doc_text += f"Source: {source}\n\n"
            doc_text += doc.page_content
            doc_text += "\n"
            
            # Check if adding this document would exceed limit
            if total_chars + len(doc_text) > max_chars and context_parts:
                break
            
            context_parts.append(doc_text)
            total_chars += len(doc_text)
        
        return "\n".join(context_parts)


class DPLContextEnhancer:
    """
    Enhances retrieval results with additional context.
    
    Adds related entities, common patterns, and links between concepts.
    """
    
    def __init__(self, retriever: DPLRetriever):
        """
        Initialize context enhancer.
        
        Args:
            retriever: DPLRetriever instance
        """
        self.retriever = retriever
        
        # Entity relationships (can be expanded)
        self.entity_relationships = {
            "visits": ["tasks", "userclientcatalog"],
            "tasks": ["visits", "vendorgroups"],
            "userclientcatalog": ["visits", "identity"],
        }
    
    async def enhance_retrieval(
        self,
        result: RetrievalResult,
        include_related_entities: bool = True
    ) -> RetrievalResult:
        """
        Enhance retrieval result with additional context.
        
        Args:
            result: Original retrieval result
            include_related_entities: Include related entity documentation
            
        Returns:
            Enhanced retrieval result
        """
        enhanced_docs = result.documents.copy()
        
        if include_related_entities:
            # Extract entity mentions from results
            entities = self._extract_entities(result.documents)
            
            # Get related entity documentation
            for entity in entities:
                related = self.entity_relationships.get(entity, [])
                for related_entity in related[:2]:  # Limit to 2 related
                    related_context = RetrievalContext(
                        query=f"{related_entity} entity",
                        entity_name=related_entity,
                        top_k=2
                    )
                    related_result = await self.retriever.retrieve(related_context)
                    enhanced_docs.extend(related_result.documents)
        
        # Remove duplicates
        unique_docs = self._remove_duplicate_documents(enhanced_docs)
        
        return RetrievalResult(
            documents=unique_docs,
            query=result.query,
            filters_applied=result.filters_applied,
            total_results=len(unique_docs),
            context_summary=f"{result.context_summary} Enhanced with related context."
        )
    
    def _extract_entities(self, documents: List[Document]) -> List[str]:
        """Extract entity names from documents."""
        entities = []
        common_entities = ["visits", "tasks", "userclientcatalog", "vendorgroups"]
        
        for doc in documents:
            content_lower = doc.page_content.lower()
            for entity in common_entities:
                if entity in content_lower and entity not in entities:
                    entities.append(entity)
        
        return entities
    
    def _remove_duplicate_documents(
        self,
        documents: List[Document]
    ) -> List[Document]:
        """Remove duplicate documents based on content."""
        seen_content = set()
        unique_docs = []
        
        for doc in documents:
            content_hash = hash(doc.page_content[:200])  # Hash first 200 chars
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_docs.append(doc)
        
        return unique_docs


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_hdl_retriever(vector_store) -> DPLRetriever:
    """
    Factory function to create DPLRetriever.
    
    Args:
        vector_store: Vector store implementation
        
    Returns:
        Initialized DPLRetriever
    """
    return DPLRetriever(vector_store)


def create_context_enhancer(retriever: DPLRetriever) -> DPLContextEnhancer:
    """
    Factory function to create DPLContextEnhancer.
    
    Args:
        retriever: DPLRetriever instance
        
    Returns:
        Initialized DPLContextEnhancer
    """
    return DPLContextEnhancer(retriever)

