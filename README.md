# Data Pipeline Agent

An intelligent AI agent specialized in troubleshooting, monitoring, and optimizing data pipeline operations.

## Overview

The Data Pipeline Agent (DPL Agent) is a production-ready AI system built with Clean Architecture principles, featuring:

- **7 Specialized Tools** for pipeline operations
- **RAG System** with semantic search over 66 knowledge base documents
- **LangGraph Orchestration** for stateful multi-agent workflows
- **Clean Architecture** with clear separation of concerns
- **136 Unit Tests** with 51% code coverage
- **Production Deployment** ready for Databricks clusters

## Features

### Core Capabilities

1. **Troubleshooting**: Diagnose pipeline errors and issues
2. **Bug Resolution**: Provide step-by-step fixes for common problems
3. **Performance Optimization**: Analyze and improve pipeline efficiency
4. **Quality Assurance**: Validate data quality and completeness
5. **Workflow Execution**: Monitor and control pipeline workflows
6. **Documentation**: Access component documentation and best practices
7. **Coordination**: Manage reprocessing and data recovery

### Technical Stack

- **LangChain/LangGraph**: Agent orchestration and tool integration
- **ChromaDB**: Vector store for semantic search
- **Claude (Anthropic)**: LLM for natural language understanding
- **Pydantic**: Data validation and serialization
- **pytest**: Comprehensive testing framework
- **MkDocs**: Professional documentation

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/data-pipeline-agent.git
cd data_pipeline_agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from pipeline_agent_lib.agent import create_agent

# Initialize the agent
agent = create_agent()

# Ask a question
response = agent.invoke({
    "messages": [{"role": "user", "content": "Why is the Orders pipeline failing?"}]
})

print(response["messages"][-1]["content"])
```

### Run Interactive Chat

```bash
python run_agent.py
```

## Architecture

### Clean Architecture Layers

```
pipeline_agent_lib/
├── domain/              # Business entities and rules
│   ├── entities/        # Core domain objects
│   ├── value_objects.py # Immutable value types
│   └── ports/           # Interface definitions
├── application/         # Use cases and orchestration
│   └── services/        # Application services (RAG, etc.)
├── infrastructure/      # External integrations
│   ├── llm/             # LLM providers (Claude, Databricks)
│   └── vector_store/    # Vector database integration
└── specialists/         # 7 specialized tools
```

### Data Flow

1. **User Query** → Agent receives natural language question
2. **Intent Analysis** → LangGraph determines which specialists to invoke
3. **RAG Retrieval** → Semantic search finds relevant documentation
4. **Tool Execution** → Specialists execute with enhanced context
5. **Response Generation** → Structured answer with sources

## Specialists

### 1. Troubleshooter
Diagnoses errors and provides root cause analysis.

```python
from pipeline_agent_lib.specialists import troubleshoot_pipeline_error

result = troubleshoot_pipeline_error(
    error_message="Connection timeout to database",
    pipeline_name="orders-ingestion"
)
```

### 2. Bug Resolver
Provides step-by-step solutions for known issues.

### 3. Performance Advisor
Analyzes pipeline performance and suggests optimizations.

### 4. Quality Assistant
Validates data quality and identifies anomalies.

### 5. Pipeline Commander
Monitors and controls workflow executions.

### 6. Ecosystem Assistant
Provides documentation and best practices.

### 7. Pipeline Coordinator
Manages reprocessing and data recovery operations.

## Configuration

### Environment Variables

```bash
# Required for local development
export ANTHROPIC_API_KEY="your-api-key-here"

# Optional: Custom configuration
export DPL_ENVIRONMENT="production"
export VECTOR_STORE_PATH="./chroma_db"
```

### Databricks Deployment

The agent integrates natively with Databricks Serving Endpoints for production use:

```python
from pipeline_agent_lib.infrastructure.llm import get_databricks_claude

# Uses Databricks native LLM serving
llm = get_databricks_claude(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    max_tokens=4096
)
```

See `databricks_examples/` for complete notebooks.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pipeline_agent_lib --cov-report=html

# Run only unit tests
pytest tests/unit/

# Run E2E tests
pytest tests/e2e/ -v
```

## Documentation

Full documentation is available at `docs/` and can be served locally:

```bash
mkdocs serve
# Open browser to http://127.0.0.1:8000
```

Or use the helper script:

```bash
./start_docs.sh
```

## Development

### Setup Development Environment

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run code quality checks
pre-commit run --all-files
```

### Project Structure

- `pipeline_agent_lib/` - Main Python package
- `docs/` - MkDocs documentation
- `tests/` - Unit, integration, and E2E tests
- `examples/` - Usage examples
- `databricks_examples/` - Databricks deployment notebooks
- `workflow_hdl/` - Sample workflow configurations

## Deployment

### Build Wheel Package

```bash
python setup.py bdist_wheel
```

The `.whl` file will be created in `dist/` and can be installed on Databricks clusters:

```python
# In Databricks notebook
%pip install /path/to/pipeline_agent_lib-3.1.0-py3-none-any.whl
```

### Production Checklist

- [ ] Set production environment variables
- [ ] Configure Databricks serving endpoints
- [ ] Load knowledge base into vector store
- [ ] Run full test suite
- [ ] Deploy wheel package to cluster
- [ ] Monitor initial agent responses

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards

- Use type hints for all functions
- Add docstrings following Google style
- Write unit tests for new features
- Run pre-commit hooks before committing
- Follow Clean Architecture principles
- Use professional logging (no print statements)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain) - LLM application framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Stateful agent orchestration
- [Anthropic Claude](https://www.anthropic.com/) - Large language model
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [MkDocs](https://www.mkdocs.org/) - Documentation generator

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the documentation at `/docs`
- Review examples in `/examples`

---

**Version**: 3.1.0  
**Status**: Production Ready  
**Last Updated**: 2025
