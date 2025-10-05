# Changelog

All notable changes to DPL Agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.1.0] - 2025-10-05

### Added
- RAG integration in all 7 specialists for knowledge-enhanced responses
- Complete knowledge base with 25 workflow JSONs documented
- Databricks Claude integration via Serving Endpoints
- 66 total knowledge files (41 core + 25 workflows)
- DPLRetrieverService for semantic search and context enhancement

### Changed
- All specialists now use RAG by default with graceful fallback
- Knowledge base moved to data_pipeline_agent_lib/knowledge/ for proper packaging
- Improved logging with DPLLogger throughout codebase
- Response formatting standardized across all specialists

### Fixed
- Knowledge base inclusion in .whl package
- Tool invocation patterns for LangChain compatibility
- 176/176 tests passing (100%)

---

## [3.0.0] - 2025-10-04

### Added
- Clean Architecture Implementation with Domain, Application, Infrastructure layers
- LangGraph Orchestration with 7 processing nodes and conditional routing
- RAG System with ChromaDB vector store and 41 DPL documentation files
- 7 DPL Specialists: Troubleshooter, Bug Resolver, Performance Advisor, Quality Assistant, DPL Commander, Ecosystem Assistant, DPL Coordinator
- Professional Code Standards with centralized logging and response formatting
- Testing Infrastructure with 113 unit tests and 40 E2E tests (100% passing)
- MkDocs documentation site with Material theme
- Python wheel package for Databricks deployment

### Changed
- All print() statements replaced with structured logging
- Tool implementations standardized with ResponseFormatter
- Error handling improved with graceful degradation
- Code organization following Clean Architecture principles

### Fixed
- Import errors resolved
- LangChain tool invocation patterns corrected
- f-string syntax errors fixed
- Package data inclusion corrected

### Dependencies
- langchain>=0.2.0,<0.3.0
- langgraph>=0.2.0,<0.3.0
- langchain-anthropic>=0.1.0,<0.2.0
- langchain-openai>=0.1.0,<0.2.0
- chromadb>=0.4.0,<0.5.0
- databricks-sdk>=0.8.0,<1.0.0
- pydantic>=2.0.0,<3.0.0
- python-dotenv>=1.0.0
- pyyaml>=6.0.0
- requests>=2.31.0

---

## Version History

- v3.1.0 (2025-10-05) - RAG integration complete
- v3.0.0 (2025-10-04) - Initial release
- v2.0.0 (2025-09) - DPL-2 with Clean Architecture (reference)
- v1.0.0 (2025-08) - DPL-1 initial specialist (legacy)

---

## Versioning Guidelines

- Major version (X.0.0): Incompatible API changes
- Minor version (0.X.0): Backward-compatible new features
- Patch version (0.0.X): Backward-compatible bug fixes

## Release Process

1. Update version in setup.py
2. Document changes in this CHANGELOG
3. Run full test suite (pytest)
4. Build wheel package (python -m build --wheel)
5. Test in Databricks UAT environment
6. Tag release in git (git tag v3.1.0)
7. Deploy to production

---

## Support

For questions, issues, or contributions:
- Issues: https://github.com/your-username/data-pipeline-agent/issues
- Discussions: https://github.com/your-username/data-pipeline-agent/discussions
