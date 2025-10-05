"""
Pytest configuration and shared fixtures for DPL Agent tests.
"""

import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_error_message():
    """Sample error message for testing."""
    return "TimeoutException: Job execution timeout after 5400 seconds"


@pytest.fixture
def sample_entity_name():
    """Sample entity name for testing."""
    return "visits"


@pytest.fixture
def sample_pipeline_name():
    """Sample pipeline name for testing."""
    return "hdl-batch-visits"


@pytest.fixture
def sample_workflow_name():
    """Sample workflow name for testing."""
    return "hdl-batch-ingestion-br"


@pytest.fixture
def mock_logger(mocker):
    """Mock logger for testing."""
    return mocker.patch('data_pipeline_agent_lib.utils.logging_config.DPLLogger')


@pytest.fixture
def sample_date_range():
    """Sample date range for testing."""
    return "2025-10-04"

