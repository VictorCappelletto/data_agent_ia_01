"""
Pytest configuration and fixtures for E2E tests.

Note: E2E tests require API keys for LLM and embeddings.
Set environment variables before running:
- ANTHROPIC_API_KEY (for Claude)
- OPENAI_API_KEY (optional, for embeddings)
"""

import pytest
import os
from typing import Generator
from datetime import datetime


@pytest.fixture(scope="session")
def check_api_keys():
    """
    Verify that required API keys are set.
    
    Skip tests if API keys are not available.
    """
    if not os.getenv("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not set - E2E tests require API keys")
    
    return True


@pytest.fixture
def conversation_thread_id() -> str:
    """Generate unique thread ID for conversation."""
    return f"test_thread_{datetime.utcnow().timestamp()}"


@pytest.fixture
def sample_hdl_queries() -> list:
    """Provide sample DPL queries for testing."""
    return [
        "What is the bronze layer in DPL?",
        "How do I troubleshoot a timeout error in streaming pipeline?",
        "Explain SCD2 merge process",
        "What are best practices for batch ingestion?",
        "How do I optimize a slow DPL pipeline?"
    ]


@pytest.fixture
def sample_error_scenarios() -> list:
    """Provide sample error scenarios."""
    return [
        {
            "description": "Streaming checkpoint timeout",
            "error": "Timeout after 1h30m in dpl-stream-visits",
            "entity": "visits"
        },
        {
            "description": "CosmosDB connection failure",
            "error": "Connection refused to MongoDB",
            "entity": "tasks"
        },
        {
            "description": "Memory issue in batch",
            "error": "OutOfMemoryError in hdl-batch-orders",
            "entity": "orders"
        }
    ]


@pytest.fixture
def mock_workflow_config() -> dict:
    """Provide mock workflow configuration."""
    return {
        "workflow_name": "hdl-test-workflow",
        "environment": "SIT",
        "entity": "visits",
        "date_range": "2025-10-04"
    }


@pytest.fixture(scope="session")
def test_data_dir(tmp_path_factory) -> str:
    """Create temporary directory for test data."""
    return str(tmp_path_factory.mktemp("hdl_e2e_data"))

