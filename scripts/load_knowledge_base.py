#!/usr/bin/env python3
"""
DPL Agent v3.0 - Knowledge Base Loader
Loads DPL documentation into Chroma vector store
"""

import logging
import os
import sys
from pathlib import Path
from typing import List

from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def load_markdown_files(knowledge_dir: Path) -> List[dict]:
    """
    Load all markdown files from knowledge directory.
    
    Args:
        knowledge_dir: Path to knowledge base directory
        
    Returns:
        List of documents with content and metadata
    """
    documents = []
    
    if not knowledge_dir.exists():
        logger.warning(f"Knowledge directory not found: {knowledge_dir}")
        return documents
    
    # Recursively find all markdown files
    md_files = list(knowledge_dir.rglob("*.md"))
    
    logger.info(f"Found {len(md_files)} markdown files")
    
    for md_file in md_files:
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Create document with metadata
            doc = {
                "content": content,
                "metadata": {
                    "source": str(md_file.relative_to(knowledge_dir)),
                    "category": md_file.parent.name,
                    "filename": md_file.name,
                }
            }
            
            documents.append(doc)
            logger.debug(f"Loaded: {md_file.name}")
            
        except Exception as e:
            logger.error(f"Error loading {md_file}: {e}")
    
    return documents


def create_vector_store(documents: List[dict]):
    """
    Create Chroma vector store and load documents.
    
    Args:
        documents: List of documents to load
    """
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError as e:
        logger.error(f"Error importing dependencies: {e}")
        logger.info("Please run: pip install -r requirements.txt")
        return
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY not found in environment")
        logger.info("Please configure your .env file")
        return
    
    logger.info("Creating embeddings...")
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Text splitter for chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    # Prepare documents for Chroma
    texts = []
    metadatas = []
    
    for doc in documents:
        # Split document into chunks
        chunks = text_splitter.split_text(doc["content"])
        
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append(doc["metadata"])
    
    logger.info(f"Created {len(texts)} chunks from {len(documents)} documents")
    
    # Create vector store
    chroma_db_path = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
    collection_name = os.getenv("CHROMA_COLLECTION_NAME", "hdl_knowledge")
    
    logger.info(f"Saving to vector store: {chroma_db_path}")
    
    try:
        vectorstore = Chroma.from_texts(
            texts=texts,
            metadatas=metadatas,
            embedding=embeddings,
            persist_directory=chroma_db_path,
            collection_name=collection_name,
        )
        
        logger.info("Vector store created successfully!")
        logger.info(f"Location: {chroma_db_path}")
        logger.info(f"Collection: {collection_name}")
        logger.info(f"Documents: {len(documents)}")
        logger.info(f"Chunks: {len(texts)}")
        
    except Exception as e:
        logger.error(f"Error creating vector store: {e}")


def main():
    """Main entry point."""
    logger.info("DPL Agent v3.0 - Knowledge Base Loader")
    logger.info("=" * 50)
    
    # Knowledge directory (now inside package)
    knowledge_dir = project_root / "data_pipeline_agent_lib" / "knowledge"
    
    if not knowledge_dir.exists():
        logger.error(f"Knowledge directory not found: {knowledge_dir}")
        logger.info("Please verify data_pipeline_agent_lib/knowledge/ exists")
        return
    
    # Load documents
    logger.info(f"Loading documents from: {knowledge_dir}")
    documents = load_markdown_files(knowledge_dir)
    
    if not documents:
        logger.warning("No documents found. Please add .md files to knowledge/ directory")
        return
    
    # Create vector store
    create_vector_store(documents)
    
    logger.info("Knowledge base loading complete!")


if __name__ == "__main__":
    main()

