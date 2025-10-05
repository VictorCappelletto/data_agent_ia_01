# DPL Agent v3.1

Production-ready AI agent for troubleshooting, monitoring, and optimizing DPL (Data Pipeline Layer) pipelines in Databricks.

---

## Overview

DPL Agent is a specialized AI assistant built with LangChain and LangGraph that automates DPL pipeline operations through seven expert specialist tools with RAG-powered knowledge retrieval.

### Core Capabilities

- **Error Diagnosis**: Automated troubleshooting for pipeline failures
- **Bug Resolution**: Known solutions and resolution guidance
- **Performance Optimization**: Actionable recommendations for slow pipelines
- **Data Quality**: Comprehensive validation across quality dimensions
- **Workflow Management**: Execution coordination and monitoring
- **Knowledge Base**: DPL architecture and best practices
- **Reprocessing Coordination**: Data recovery workflows with team notification

---

## Architecture

### Clean Architecture Implementation
- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and orchestration (7 specialists)
- **Infrastructure Layer**: LLM, vector store, and external integrations

### RAG System
- **66 documentation files** as knowledge base (41 core + 25 workflows)
- **ChromaDB vector store** for semantic search
- **Context-aware retrieval** with entity and pipeline filtering
- **Integrated in all specialists** for enhanced responses

### LangGraph Orchestration
- **Stateful workflows** for multi-turn interactions
- **Intelligent routing** based on query intent
- **Tool calling** with specialist selection
- **Conversation memory** for context preservation

---

## Seven Specialist Tools

1. **Troubleshooter** - Error diagnosis and pipeline health analysis
2. **Bug Resolver** - Known bug solutions and resolution steps
3. **Performance Advisor** - Optimization strategies and recommendations
4. **Quality Assistant** - Data quality validation
5. **DPL Commander** - Workflow execution and monitoring
6. **Ecosystem Assistant** - Component documentation and best practices
7. **DPL Coordinator** - Reprocessing coordination and team notification

---

## Quick Start

### Installation
```python
# Databricks
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
dbutils.library.restartPython()
```

### Basic Usage
```python
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

# Diagnose pipeline error
result = troubleshoot_hdl_error(
    "Timeout error in dpl-stream-visits after 1h30m"
)
print(result)
```

**Full Guide**: [Quick Start](deployment/quickstart.md)

---

## Quality Metrics

- **136 unit tests** (100% passing)
- **40 E2E tests** (100% passing)
- **51% code coverage** (91% for specialists)
- **Professional output** (emoji-free, structured logging)
- **RAG integration** (all 7 specialists)

---

## Documentation

### Getting Started
- [Installation](getting-started/installation.md) - Setup for Databricks and local
- [Quick Start](getting-started/quickstart.md) - Get started in 5 minutes
- [Configuration](getting-started/configuration.md) - API keys and environment setup

### Deployment
- [Quick Deployment](deployment/quickstart.md) - Fast deployment guide
- [Production Deployment](deployment/production-deployment.md) - Complete workflow

### Reference
- [Architecture](architecture/clean-architecture.md) - Design principles
- [Specialists](specialists/overview.md) - Tool documentation
- [API Reference](api/specialists.md) - Detailed API docs
- [Examples](examples/basic.md) - Code examples
- [Test Results](testing/test-results.md) - Coverage and quality

---

## Package Information

- **Version**: 3.1.0
- **Size**: 162 KB
- **Format**: Python Wheel (.whl)
- **Python**: >=3.9
- **Knowledge**: 66 files (41 core + 25 workflows)
- **Dependencies**: LangChain, LangGraph, ChromaDB, Databricks SDK

---

## Support

- **Technical Lead**: Victor Cappelleto
- **Project**: Operations Strategy - DPL Operations
- **Documentation**: [MkDocs Site](https://your-docs-url)

---

**Last Updated**: 2025-10-05  
**Status**: Production Ready (v3.1.0 - RAG Complete)
