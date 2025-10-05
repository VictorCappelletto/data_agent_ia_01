#!/usr/bin/env python3
"""
DPL Agent v3.0 - RAG System Demo

Demonstrates Retrieval-Augmented Generation (RAG) system.
Shows knowledge base indexing and semantic search.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data_pipeline_agent_lib.infrastructure.vector_store import (
    create_chroma_store,
    create_hdl_retriever,
    create_knowledge_indexer,
)


def print_section(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"{title}")
    print("=" * 70)


def demo_1_knowledge_indexing():
    """Demo 1: Index knowledge base."""
    print_section("DEMO 1: Knowledge Base Indexing")
    
    knowledge_path = project_root / "knowledge"
    
    if not knowledge_path.exists():
        print(f"WARNING: Knowledge base not found at {knowledge_path}")
        print("Skipping indexing demo.")
        return None
    
    print(f"\nIndexing knowledge from: {knowledge_path}")
    
    # Create indexer
    indexer = create_knowledge_indexer(knowledge_path)
    
    # Index knowledge
    print("Processing markdown files...")
    stats = indexer.index_knowledge_base()
    
    print(f"\nIndexing complete:")
    print(f"  Files processed: {stats.get('files', 0)}")
    print(f"  Chunks created: {stats.get('chunks', 0)}")
    
    return indexer.vector_store


def demo_2_semantic_search(vector_store):
    """Demo 2: Semantic search."""
    print_section("DEMO 2: Semantic Search")
    
    if not vector_store:
        print("Vector store not available. Skipping demo.")
        return
    
    # Create retriever
    retriever = create_hdl_retriever(vector_store)
    
    # Search queries
    queries = [
        "What is SCD2?",
        "How do streaming pipelines work?",
        "Troubleshooting timeout errors",
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        docs = retriever.retrieve_documents(query, k=3)
        
        print(f"Found {len(docs)} relevant documents:")
        for i, doc in enumerate(docs, 1):
            preview = doc[:100] + "..." if len(doc) > 100 else doc
            print(f"  {i}. {preview}")


def demo_3_filtered_retrieval(vector_store):
    """Demo 3: Filtered retrieval by entity."""
    print_section("DEMO 3: Filtered Retrieval")
    
    if not vector_store:
        print("Vector store not available. Skipping demo.")
        return
    
    retriever = create_hdl_retriever(vector_store)
    
    # Filtered search
    query = "pipeline architecture"
    filters = {"entity": "visits"}
    
    print(f"\nQuery: {query}")
    print(f"Filters: {filters}")
    
    docs = retriever.retrieve_with_filters(query, filters=filters, k=3)
    
    print(f"\nFound {len(docs)} documents for visits entity:")
    for i, doc in enumerate(docs, 1):
        preview = doc[:100] + "..." if len(doc) > 100 else doc
        print(f"  {i}. {preview}")


def demo_4_collection_stats(vector_store):
    """Demo 4: Vector store statistics."""
    print_section("DEMO 4: Collection Statistics")
    
    if not vector_store:
        print("Vector store not available. Skipping demo.")
        return
    
    stats = vector_store.get_collection_stats()
    
    print("\nVector Store Statistics:")
    print(f"  Total documents: {stats.get('count', 0)}")
    print(f"  Embedding dimension: {stats.get('dimension', 0)}")
    print(f"  Collection name: {stats.get('name', 'N/A')}")


def main():
    """Run all RAG demos."""
    print("DPL AGENT V3.0 - RAG SYSTEM DEMO")
    print("Retrieval-Augmented Generation")
    
    try:
        # Run demos
        vector_store = demo_1_knowledge_indexing()
        demo_2_semantic_search(vector_store)
        demo_3_filtered_retrieval(vector_store)
        demo_4_collection_stats(vector_store)
        
        # Summary
        print_section("SUMMARY")
        print("RAG system demonstration complete!")
        print("\nWhat you learned:")
        print("- Knowledge base indexing from markdown files")
        print("- Semantic search with ChromaDB")
        print("- Filtered retrieval by entity/category")
        print("- Vector store statistics")
        print("\nNext steps:")
        print("- Try agent_conversation.py to see RAG in action")
        print("- Explore knowledge/ directory for source files")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure knowledge/ directory exists")
        print("2. Check ChromaDB installation")
        print("3. Verify sentence-transformers is installed")


if __name__ == "__main__":
    main()

