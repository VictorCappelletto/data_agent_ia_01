"""
DPL Agent v3.0 - Knowledge Base Loader

Loads DPL documentation from markdown files into vector store.
Processes, chunks, and indexes knowledge for semantic search.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter
)
from langchain.schema import Document


@dataclass
class DocumentMetadata:
    """Metadata for loaded documents."""
    source: str
    category: str
    filename: str
    file_path: str
    file_size: int
    last_modified: float


class DPLKnowledgeLoader:
    """
    Loads DPL knowledge base from markdown files.
    
    Features:
    - Recursive directory scanning
    - Markdown header-based splitting
    - Automatic metadata extraction
    - Category detection
    - Filtering capabilities
    """
    
    def __init__(
        self,
        knowledge_base_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize knowledge loader.
        
        Args:
            knowledge_base_path: Path to knowledge base directory
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.knowledge_base_path = Path(knowledge_base_path)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize text splitters
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_all_documents(
        self,
        file_pattern: str = "*.md",
        exclude_patterns: Optional[List[str]] = None
    ) -> List[Document]:
        """
        Load all markdown documents from knowledge base.
        
        Args:
            file_pattern: Glob pattern for files to load
            exclude_patterns: Patterns to exclude (e.g., ["README.md"])
            
        Returns:
            List of LangChain Documents
        """
        if not self.knowledge_base_path.exists():
            logger.info(f"Knowledge base path not found: {self.knowledge_base_path}")
            return []
        
        exclude_patterns = exclude_patterns or []
        documents = []
        
        # Find all markdown files
        md_files = list(self.knowledge_base_path.rglob(file_pattern))
        
        logger.info(f"Found {len(md_files)} markdown files")
        
        for md_file in md_files:
            # Check exclusion patterns
            if any(pattern in str(md_file) for pattern in exclude_patterns):
                continue
            
            try:
                # Load document
                doc = self._load_single_document(md_file)
                if doc:
                    documents.append(doc)
            except Exception as e:
                logger.error(f"Error loading {md_file}: {e}")
        
        logger.info(f"Loaded {len(documents)} documents")
        return documents
    
    def _load_single_document(self, file_path: Path) -> Optional[Document]:
        """
        Load a single markdown document.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            LangChain Document or None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                return None
            
            # Extract metadata
            metadata = self._extract_metadata(file_path, content)
            
            # Create document
            doc = Document(
                page_content=content,
                metadata=metadata
            )
            
            return doc
            
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return None
    
    def _extract_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """
        Extract metadata from file and content.
        
        Args:
            file_path: Path to file
            content: File content
            
        Returns:
            Metadata dictionary
        """
        # Get relative path from knowledge base
        try:
            relative_path = file_path.relative_to(self.knowledge_base_path)
        except ValueError:
            relative_path = file_path
        
        # Determine category from directory structure
        category = "general"
        if len(relative_path.parents) > 1:
            category = relative_path.parents[-2].name
        
        # File stats
        stats = file_path.stat()
        
        metadata = {
            "source": str(relative_path),
            "category": category,
            "filename": file_path.name,
            "file_path": str(file_path),
            "file_size": stats.st_size,
            "last_modified": stats.st_mtime,
            "word_count": len(content.split()),
            "line_count": len(content.split('\n'))
        }
        
        # Extract title from first H1 header if exists
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                metadata["title"] = line[2:].strip()
                break
        
        return metadata
    
    def chunk_documents(
        self,
        documents: List[Document],
        use_markdown_splitter: bool = True
    ) -> List[Document]:
        """
        Chunk documents into smaller pieces.
        
        Args:
            documents: List of documents to chunk
            use_markdown_splitter: Use markdown-aware splitting
            
        Returns:
            List of chunked documents
        """
        all_chunks = []
        
        for doc in documents:
            try:
                if use_markdown_splitter:
                    # First split by markdown headers
                    header_splits = self.markdown_splitter.split_text(doc.page_content)
                    
                    # Then further chunk if needed
                    for split in header_splits:
                        chunks = self.text_splitter.split_text(split.page_content)
                        
                        for i, chunk in enumerate(chunks):
                            chunk_metadata = doc.metadata.copy()
                            chunk_metadata.update(split.metadata)
                            chunk_metadata["chunk_index"] = i
                            chunk_metadata["total_chunks"] = len(chunks)
                            
                            all_chunks.append(Document(
                                page_content=chunk,
                                metadata=chunk_metadata
                            ))
                else:
                    # Simple text splitting
                    chunks = self.text_splitter.split_text(doc.page_content)
                    
                    for i, chunk in enumerate(chunks):
                        chunk_metadata = doc.metadata.copy()
                        chunk_metadata["chunk_index"] = i
                        chunk_metadata["total_chunks"] = len(chunks)
                        
                        all_chunks.append(Document(
                            page_content=chunk,
                            metadata=chunk_metadata
                        ))
                        
            except Exception as e:
                filename = doc.metadata.get('filename', 'unknown')
                logger.error(f"Error chunking document {filename}: {e}")
        
        logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks
    
    def filter_by_category(
        self,
        documents: List[Document],
        categories: List[str]
    ) -> List[Document]:
        """
        Filter documents by category.
        
        Args:
            documents: List of documents
            categories: Categories to include
            
        Returns:
            Filtered list of documents
        """
        return [
            doc for doc in documents
            if doc.metadata.get("category") in categories
        ]
    
    def get_statistics(self, documents: List[Document]) -> Dict[str, Any]:
        """
        Get statistics about loaded documents.
        
        Args:
            documents: List of documents
            
        Returns:
            Statistics dictionary
        """
        if not documents:
            return {
                "total_documents": 0,
                "total_chunks": 0,
                "categories": [],
                "total_words": 0
            }
        
        categories = {}
        total_words = 0
        
        for doc in documents:
            category = doc.metadata.get("category", "unknown")
            categories[category] = categories.get(category, 0) + 1
            total_words += doc.metadata.get("word_count", 0)
        
        return {
            "total_documents": len(documents),
            "total_chunks": sum(
                doc.metadata.get("total_chunks", 1) for doc in documents
            ),
            "categories": dict(sorted(categories.items())),
            "total_words": total_words,
            "avg_words_per_doc": total_words / len(documents) if documents else 0
        }


class DPLKnowledgeIndexer:
    """
    Indexes DPL knowledge into vector store.
    
    Orchestrates loading, chunking, and indexing process.
    """
    
    def __init__(
        self,
        knowledge_loader: DPLKnowledgeLoader,
        vector_store
    ):
        """
        Initialize knowledge indexer.
        
        Args:
            knowledge_loader: DPLKnowledgeLoader instance
            vector_store: Vector store implementation
        """
        self.loader = knowledge_loader
        self.vector_store = vector_store
    
    async def index_knowledge_base(
        self,
        clear_existing: bool = False,
        categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Index complete knowledge base into vector store.
        
        Args:
            clear_existing: Clear existing collection before indexing
            categories: Only index specific categories
            
        Returns:
            Indexing statistics
        """
        logger.info("=" * 60)
        logger.info("DPL Knowledge Base Indexing")
        logger.info("=" * 60)
        
        # Clear existing if requested
        if clear_existing:
            logger.info("\nClearing existing collection...")
            await self.vector_store.clear_collection()
        
        # Load documents
        logger.info("\nLoading documents...")
        documents = self.loader.load_all_documents()
        
        if not documents:
            return {
                "status": "error",
                "message": "No documents found",
                "indexed_count": 0
            }
        
        # Filter by categories if specified
        if categories:
            logger.info(f"\nFiltering by categories: {categories}")
            documents = self.loader.filter_by_category(documents, categories)
        
        # Get statistics before chunking
        stats = self.loader.get_statistics(documents)
        total_docs = stats['total_documents']
        logger.info(f"\nLoaded {total_docs} documents:")
        for category, count in stats['categories'].items():
            logger.info(f"  - {category}: {count} documents")
        
        # Chunk documents
        logger.info("\nChunking documents...")
        chunks = self.loader.chunk_documents(documents)
        
        logger.info(f"Created {len(chunks)} chunks")
        
        # Index into vector store
        logger.info("\nIndexing into vector store...")
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        ids = await self.vector_store.add_documents(texts, metadatas)
        
        # Get final stats
        collection_stats = await self.vector_store.get_collection_stats()
        
        result = {
            "status": "success",
            "documents_loaded": stats['total_documents'],
            "chunks_created": len(chunks),
            "chunks_indexed": len(ids),
            "categories": stats['categories'],
            "collection_stats": collection_stats
        }
        
        logger.info("\n" + "=" * 60)
        logger.info("Indexing Complete!")
        logger.info("=" * 60)
        docs_loaded = result['documents_loaded']
        chunks_indexed = result['chunks_indexed']
        logger.info(f"Documents: {docs_loaded}")
        logger.info(f"Chunks: {chunks_indexed}")
        logger.info("=" * 60)
        
        return result


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_knowledge_loader(
    knowledge_base_path: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> DPLKnowledgeLoader:
    """
    Factory function to create DPLKnowledgeLoader.
    
    Args:
        knowledge_base_path: Path to knowledge base directory
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks
        
    Returns:
        Initialized DPLKnowledgeLoader
    """
    return DPLKnowledgeLoader(
        knowledge_base_path=knowledge_base_path,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )


def create_knowledge_indexer(
    knowledge_base_path: str,
    vector_store
) -> DPLKnowledgeIndexer:
    """
    Factory function to create DPLKnowledgeIndexer.
    
    Args:
        knowledge_base_path: Path to knowledge base directory
        vector_store: Vector store implementation
        
    Returns:
        Initialized DPLKnowledgeIndexer
    """
    loader = create_knowledge_loader(knowledge_base_path)
    return DPLKnowledgeIndexer(loader, vector_store)

