"""
DPL Agent v3.0 - LangGraph Powered DPL Specialist

Standalone agent for DPL operations with:
- LangGraph StateGraph orchestration
- RAG-powered knowledge retrieval
- Claude 3.5 Sonnet integration
- 7 specialized DPL assistants
- Clean Architecture (SOLID principles)
"""

__version__ = "3.0.0"
__author__ = "Victor Cappelletto"

from data_pipeline_agent_lib.agent.graph import create_data_pipeline_agent_graph
from data_pipeline_agent_lib.domain.entities.hdl_entities import (
    DPLPipeline,
    DPLWorkflow,
    DPLTable,
    DPLError,
)
from data_pipeline_agent_lib.domain.services.hdl_domain_service import DPLDomainService

__all__ = [
    "create_data_pipeline_agent_graph",
    "DPLPipeline",
    "DPLWorkflow",
    "DPLTable",
    "DPLError",
    "DPLDomainService",
]

