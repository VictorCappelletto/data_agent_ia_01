#!/usr/bin/env python3
"""
DPL Agent v3.0 Library Setup
LangGraph-powered standalone DPL specialist
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="pipeline-agent-lib",
    version="3.1.0",
    description="Data Pipeline Agent - AI-powered pipeline operations with Clean Architecture, RAG, and LangGraph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Victor Cappelletto",
    author_email="victor.cappelletto@example.com",
    url="https://github.com/your-username/data-pipeline-agent",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    install_requires=[
        # Core LangChain/LangGraph
        "langchain>=0.2.0,<0.3.0",
        "langchain-anthropic>=0.1.0,<0.2.0",
        "langgraph>=0.2.0,<0.3.0",
        "langchain-community>=0.2.0,<0.3.0",
        
        # Vector Store & Embeddings
        "chromadb>=0.4.0,<0.5.0",
        "sentence-transformers>=2.0.0,<3.0.0",
        "openai>=1.0.0,<2.0.0",  # For embeddings
        
        # MCP Integration (requires Python 3.10+, optional)
        # "mcp>=1.0.0",
        
        # Databricks Integration
        "databricks-sdk>=0.8.0,<1.0.0",
        
        # Data Processing
        "pandas>=1.3.0,<2.0.0",
        "pyspark>=3.3.0,<4.0.0",
        
        # Utilities
        "python-dotenv>=1.0.0,<2.0.0",
        "pyyaml>=6.0.0,<7.0.0",
        "requests>=2.31.0,<3.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "python-dateutil>=2.8.0,<3.0.0",
        
        # CLI
        "rich>=13.0.0,<14.0.0",
        "typer>=0.9.0,<1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.0.0",
            "mkdocstrings[python]>=0.24.0",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: AI",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="data-pipeline databricks langchain langgraph ai agent rag clean-architecture etl",
    package_data={
        "pipeline_agent_lib": [
            "configs/*.yaml",
            "configs/*.json",
            "knowledge/*.md",
            "knowledge/**/*.md",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Source": "https://github.com/your-username/data-pipeline-agent",
        "Documentation": "https://github.com/your-username/data-pipeline-agent/docs",
        "Bug Reports": "https://github.com/your-username/data-pipeline-agent/issues",
    },
    entry_points={
        "console_scripts": [
            "hdl-agent=data_pipeline_agent_lib.cli:main",
        ],
    },
)

