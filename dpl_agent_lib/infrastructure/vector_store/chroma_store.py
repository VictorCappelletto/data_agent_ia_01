"""
DPL Agent v3.0 - Chroma Vector Store Implementation

Implements VectorStorePort using ChromaDB for semantic search
across DPL knowledge base.
"""

import os
from typing import List, Optional, Dict, Any
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from ...domain.ports.hdl_repository_port import VectorStorePort


class ChromaVectorStore(VectorStorePort):
    """
    ChromaDB implementation of VectorStorePort.
    
    Provides semantic search capabilities over DPL knowledge base
    using OpenAI embeddings.
    """
    
    def __init__(
        self,
        persist_directory: Optional[str] = None,
        collection_name: str = "hdl_knowledge",
        embedding_model: str = "text-embedding-3-small"
    ):
        """
        Initialize Chroma vector store.
        
        Args:
            persist_directory: Directory to persist vector store
            collection_name: Name of the collection
            embedding_model: OpenAI embedding model to use
        """
        self.persist_directory = persist_directory or os.getenv(
            "CHROMA_DB_PATH",
            "./data/chroma_db"
        )
        self.collection_name = collection_name
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize Chroma
        self._vectorstore: Optional[Chroma] = None
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self) -> None:
        """Initialize or load existing vector store."""
        try:
            # Try to load existing vector store
            self._vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
        except Exception as e:
            # Create new vector store if it doesn't exist
            logger.info(f"Creating new vector store: {e}")
            Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
            self._vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
    
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            filters: Metadata filters (e.g., {"category": "troubleshooting"})
            
        Returns:
            List of documents with content and metadata
        """
        if not self._vectorstore:
            return []
        
        try:
            # Perform similarity search
            if filters:
                results = self._vectorstore.similarity_search(
                    query,
                    k=top_k,
                    filter=filters
                )
            else:
                results = self._vectorstore.similarity_search(query, k=top_k)
            
            # Convert to dictionary format
            documents = []
            for doc in results:
                documents.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "source": doc.metadata.get("source", "unknown")
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return []
    
    async def search_with_scores(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search with similarity scores.
        
        Args:
            query: Search query
            top_k: Number of results to return
            filters: Metadata filters
            
        Returns:
            List of documents with content, metadata, and scores
        """
        if not self._vectorstore:
            return []
        
        try:
            # Perform similarity search with scores
            if filters:
                results = self._vectorstore.similarity_search_with_score(
                    query,
                    k=top_k,
                    filter=filters
                )
            else:
                results = self._vectorstore.similarity_search_with_score(query, k=top_k)
            
            # Convert to dictionary format
            documents = []
            for doc, score in results:
                documents.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "source": doc.metadata.get("source", "unknown"),
                    "score": float(score)
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error during search with scores: {e}")
            return []
    
    async def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """
        Add documents to vector store.
        
        Args:
            documents: List of document texts
            metadatas: Optional list of metadata dicts
            
        Returns:
            List of document IDs
        """
        if not self._vectorstore:
            return []
        
        try:
            # Add documents to vector store
            ids = self._vectorstore.add_texts(
                texts=documents,
                metadatas=metadatas
            )
            
            return ids
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return []
    
    async def add_documents_chunked(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[str]:
        """
        Add documents with automatic chunking.
        
        Args:
            documents: List of document texts
            metadatas: Optional list of metadata dicts
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of chunk IDs
        """
        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Split documents into chunks
        all_chunks = []
        all_metadatas = []
        
        for i, doc_text in enumerate(documents):
            chunks = text_splitter.split_text(doc_text)
            all_chunks.extend(chunks)
            
            # Copy metadata for each chunk
            if metadatas and i < len(metadatas):
                base_metadata = metadatas[i].copy()
                for chunk_idx in range(len(chunks)):
                    chunk_metadata = base_metadata.copy()
                    chunk_metadata["chunk_index"] = chunk_idx
                    chunk_metadata["total_chunks"] = len(chunks)
                    all_metadatas.append(chunk_metadata)
            else:
                all_metadatas.extend([{"chunk_index": j} for j in range(len(chunks))])
        
        # Add chunked documents
        return await self.add_documents(all_chunks, all_metadatas)
    
    async def update_document(self, document_id: str, content: str) -> bool:
        """
        Update document content.
        
        Note: ChromaDB doesn't support direct updates,
        so we delete and re-add.
        
        Args:
            document_id: Document ID
            content: New content
            
        Returns:
            Success status
        """
        if not self._vectorstore:
            return False
        
        try:
            # Delete old document
            self._vectorstore.delete([document_id])
            
            # Add new document
            ids = await self.add_documents([content])
            
            return len(ids) > 0
            
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            return False
    
    async def delete_document(self, document_id: str) -> bool:
        """
        Delete document from vector store.
        
        Args:
            document_id: Document ID
            
        Returns:
            Success status
        """
        if not self._vectorstore:
            return False
        
        try:
            self._vectorstore.delete([document_id])
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get vector store collection statistics.
        
        Returns:
            Dictionary with collection stats
        """
        if not self._vectorstore:
            return {
                "error": "Vector store not initialized",
                "document_count": 0
            }
        
        try:
            # Get collection
            collection = self._vectorstore._collection
            
            return {
                "name": self.collection_name,
                "document_count": collection.count(),
                "persist_directory": self.persist_directory,
                "embedding_model": self.embeddings.model
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "document_count": 0
            }
    
    def as_retriever(
        self,
        search_type: str = "similarity",
        search_kwargs: Optional[Dict[str, Any]] = None
    ):
        """
        Get LangChain retriever interface.
        
        Args:
            search_type: "similarity", "mmr", or "similarity_score_threshold"
            search_kwargs: Additional search parameters
            
        Returns:
            LangChain Retriever
        """
        if not self._vectorstore:
            raise ValueError("Vector store not initialized")
        
        default_kwargs = {"k": 5}
        if search_kwargs:
            default_kwargs.update(search_kwargs)
        
        return self._vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs=default_kwargs
        )
    
    async def clear_collection(self) -> bool:
        """
        Clear all documents from collection.
        
        WARNING: This deletes all data!
        
        Returns:
            Success status
        """
        if not self._vectorstore:
            return False
        
        try:
            # Delete collection and recreate
            self._vectorstore._client.delete_collection(self.collection_name)
            self._initialize_vectorstore()
            return True
            
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
            return False


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_chroma_store(
    persist_directory: Optional[str] = None,
    collection_name: str = "hdl_knowledge"
) -> ChromaVectorStore:
    """
    Factory function to create ChromaVectorStore.
    
    Args:
        persist_directory: Directory to persist vector store
        collection_name: Name of the collection
        
    Returns:
        Initialized ChromaVectorStore
    """
    return ChromaVectorStore(
        persist_directory=persist_directory,
        collection_name=collection_name
    )

