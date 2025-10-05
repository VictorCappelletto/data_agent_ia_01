#!/usr/bin/env python3
"""
DPL Agent v3.0 - RAG System Test Example
Test the RAG system with DPL knowledge base
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data_pipeline_agent_lib.infrastructure.vector_store import (
    create_chroma_store,
    create_knowledge_indexer,
    create_hdl_retriever,
    RetrievalContext,
)


async def test_indexing():
    """Test knowledge base indexing."""
    print("=" * 70)
    print("TEST 1: Knowledge Base Indexing")
    print("=" * 70)
    
    # Create vector store
    print("\n1. Creating vector store...")
    vector_store = create_chroma_store(
        persist_directory="./data/chroma_db_test",
        collection_name="hdl_test"
    )
    
    # Create indexer
    print("2. Creating knowledge indexer...")
    knowledge_path = project_root / "knowledge"
    indexer = create_knowledge_indexer(str(knowledge_path), vector_store)
    
    # Index knowledge base
    print("3. Indexing knowledge base...")
    result = await indexer.index_knowledge_base(clear_existing=True)
    
    # Print results
    print("\n" + "=" * 70)
    print("INDEXING RESULTS:")
    print("=" * 70)
    print(f"Status: {result['status']}")
    print(f"Documents loaded: {result['documents_loaded']}")
    print(f"Chunks indexed: {result['chunks_indexed']}")
    print(f"\nCategories:")
    for cat, count in result['categories'].items():
        print(f"  - {cat}: {count} documents")
    
    return vector_store


async def test_semantic_search(vector_store):
    """Test semantic search capabilities."""
    print("\n" + "=" * 70)
    print("TEST 2: Semantic Search")
    print("=" * 70)
    
    # Test queries
    queries = [
        "What is SCD2 merge process?",
        "How to debug DPL pipeline timeout?",
        "Explain visits streaming pipeline",
        "What are the DPL utilities available?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n--- Query {i} ---")
        print(f"Q: {query}")
        
        results = await vector_store.search(query, top_k=3)
        
        print(f"Found {len(results)} results:")
        for j, result in enumerate(results, 1):
            source = result['metadata'].get('source', 'unknown')
            category = result['metadata'].get('category', 'unknown')
            content_preview = result['content'][:150] + "..."
            
            print(f"\n  Result {j}:")
            print(f"  Source: {source}")
            print(f"  Category: {category}")
            print(f"  Preview: {content_preview}")


async def test_hdl_retriever(vector_store):
    """Test DPL-specific retriever."""
    print("\n" + "=" * 70)
    print("TEST 3: DPL Retriever")
    print("=" * 70)
    
    # Create retriever
    retriever = create_hdl_retriever(vector_store)
    
    # Test troubleshooting retrieval
    print("\n--- Troubleshooting Retrieval ---")
    result = await retriever.retrieve_for_troubleshooting(
        error_message="Pipeline timeout after 1 hour",
        entity_name="visits",
        pipeline_type="streaming"
    )
    
    print(f"Context: {result.context_summary}")
    print(f"Documents found: {result.total_results}")
    
    # Format for LLM
    formatted = retriever.format_documents_for_llm(result.documents, max_chars=500)
    print(f"\nFormatted for LLM (preview):")
    print(formatted[:500] + "...")
    
    # Test architecture retrieval
    print("\n--- Architecture Retrieval ---")
    result = await retriever.retrieve_for_architecture(
        query="What is the DPL architecture?",
        entity_name="tasks"
    )
    
    print(f"Context: {result.context_summary}")
    print(f"Documents found: {result.total_results}")


async def test_filtering(vector_store):
    """Test retrieval with filtering."""
    print("\n" + "=" * 70)
    print("TEST 4: Filtered Retrieval")
    print("=" * 70)
    
    # Create retriever
    retriever = create_hdl_retriever(vector_store)
    
    # Test with category filter
    print("\n--- Category Filter: hdl_architecture ---")
    context = RetrievalContext(
        query="streaming pipeline",
        category="hdl_architecture",
        top_k=3
    )
    
    result = await retriever.retrieve(context)
    
    print(f"Query: {result.query}")
    print(f"Filters applied: {result.filters_applied}")
    print(f"Documents found: {result.total_results}")
    
    for i, doc in enumerate(result.documents, 1):
        source = doc.metadata.get('source', 'unknown')
        category = doc.metadata.get('category', 'unknown')
        print(f"  {i}. {source} ({category})")


async def test_collection_stats(vector_store):
    """Test collection statistics."""
    print("\n" + "=" * 70)
    print("TEST 5: Collection Statistics")
    print("=" * 70)
    
    stats = await vector_store.get_collection_stats()
    
    print(f"Collection Name: {stats.get('name')}")
    print(f"Document Count: {stats.get('document_count')}")
    print(f"Persist Directory: {stats.get('persist_directory')}")
    print(f"Embedding Model: {stats.get('embedding_model')}")


async def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("DPL Agent v3.0 - RAG System Tests")
    print("=" * 70)
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not found in environment")
        print("Please configure your .env file")
        return
    
    try:
        # Run tests
        vector_store = await test_indexing()
        await test_semantic_search(vector_store)
        await test_hdl_retriever(vector_store)
        await test_filtering(vector_store)
        await test_collection_stats(vector_store)
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

