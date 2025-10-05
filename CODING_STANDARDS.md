# Professional Coding Standards - DPL Agent v3.0

**Established:** 2025-10-04  
**Status:** MANDATORY for all new code  
**Quality Target:** 9/10 (Senior Engineering Standard)

---

## Core Principles

### 1. Clean Code
- No code duplication
- Single Responsibility Principle
- DRY (Don't Repeat Yourself)
- SOLID principles applied
- Clean Architecture maintained

### 2. Professional Output
- NO emojis in code or responses
- NO decorative symbols
- Technical, professional language
- Clear, concise communication

### 3. Type Safety
- All function parameters typed
- Return types specified
- Use `Optional`, `List`, `Dict`, `Any` from typing
- Pydantic models where appropriate

---

## Mandatory Standards

### LOGGING (NOT print!)

**DO:**
```python
from ..utils import get_logger

logger = get_logger(__name__)

def process_data(data: str) -> bool:
    logger.info("Processing data", data_length=len(data))
    try:
        result = perform_operation(data)
        logger.debug("Operation successful", result=result)
        return True
    except Exception as e:
        logger.error("Operation failed", exc_info=True)
        return False
```

**DON'T:**
```python
def process_data(data):
    print(f"Processing {len(data)} characters")  # ❌ NO print()
    print("✅ Success!")  # ❌ NO emojis
    return True
```

---

### DOCSTRINGS (Always Required)

**DO:**
```python
def search_error_patterns(
    error_message: str,
    entity_name: Optional[str] = None,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search for similar error patterns in DPL knowledge base.
    
    Performs semantic search to find relevant error patterns and
    troubleshooting guidance from the knowledge base.
    
    Args:
        error_message: Error message or description to search for
        entity_name: Optional DPL entity name for context
        top_k: Number of top results to return (default: 5)
        
    Returns:
        List of dictionaries containing search results with:
        - content: Retrieved knowledge content
        - score: Relevance score
        - source: Source document reference
        
    Raises:
        ValueError: If error_message is empty
        RuntimeError: If vector store is not initialized
        
    Example:
        >>> results = search_error_patterns(
        ...     "Timeout in pipeline",
        ...     entity_name="visits",
        ...     top_k=3
        ... )
        >>> len(results)
        3
    """
    if not error_message:
        raise ValueError("error_message cannot be empty")
    
    # Implementation here
    pass
```

**DON'T:**
```python
def search_error_patterns(error_message, entity_name=None, top_k=5):
    # ❌ No type hints
    # ❌ No docstring
    pass
```

---

### ERROR HANDLING (Specific Exceptions)

**DO:**
```python
def load_knowledge_base(path: str) -> bool:
    """Load knowledge base from file path."""
    try:
        with open(path, 'r') as f:
            data = f.read()
        logger.info("Knowledge base loaded", file_path=path)
        return True
        
    except FileNotFoundError as e:
        logger.error("Knowledge base file not found", file_path=path)
        raise
        
    except PermissionError as e:
        logger.error("Permission denied reading knowledge base", file_path=path)
        raise
        
    except Exception as e:
        logger.error("Unexpected error loading knowledge base", exc_info=True)
        raise RuntimeError(f"Failed to load knowledge base: {e}")
```

**DON'T:**
```python
def load_knowledge_base(path):
    try:
        data = open(path).read()  # ❌ No context manager
        print("Loaded!")  # ❌ print() instead of logger
    except:  # ❌ Bare except
        print("Error!")  # ❌ No specific error info
        return None  # ❌ Silent failure
```

---

### RESPONSE FORMATTING (No Emojis)

**DO:**
```python
from ..utils import ResponseFormatter, CommonFormatters

def format_troubleshooting_result(result: dict) -> str:
    """Format troubleshooting result professionally."""
    response_parts = []
    response_parts.append("TROUBLESHOOTING ANALYSIS")
    response_parts.append("=" * 50)
    response_parts.append("")
    response_parts.append(f"Diagnosis: {result['diagnosis']}")
    response_parts.append(f"Severity: {result['severity']}")
    response_parts.append("")
    response_parts.append("Recommended Actions:")
    response_parts.append(CommonFormatters.format_list(
        result['actions'],
        numbered=True
    ))
    
    return "\n".join(response_parts)
```

**DON'T:**
```python
def format_troubleshooting_result(result):
    return f"""
🔍 **TROUBLESHOOTING ANALYSIS**  # ❌ Emoji
    
**Diagnosis**: {result['diagnosis']}  # ❌ Markdown in code
⚠️ **Severity**: {result['severity']}  # ❌ Emoji
"""
```

---

### CODE ORGANIZATION (Clean Structure)

**DO:**
```python
# hdl_retriever_service.py

"""
DPL Retriever Service - RAG Integration

Provides centralized semantic search and context enhancement
for all DPL specialists.
"""

from typing import List, Optional, Dict, Any
from ...infrastructure.vector_store import DPLRetriever
from ..utils import get_logger

logger = get_logger(__name__)


class DPLRetrieverService:
    """Centralized RAG service for DPL specialists."""
    
    def __init__(self, retriever: DPLRetriever):
        """
        Initialize retriever service.
        
        Args:
            retriever: DPL vector store retriever instance
        """
        self.retriever = retriever
        logger.info("DPL Retriever Service initialized")
    
    def search_error_patterns(
        self,
        error_message: str,
        entity_name: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for error patterns (see full docstring above)."""
        logger.debug(
            "Searching error patterns",
            error_length=len(error_message),
            entity=entity_name,
            top_k=top_k
        )
        
        query = self._build_error_query(error_message, entity_name)
        results = self.retriever.search(query, top_k=top_k)
        
        logger.info(
            "Error pattern search complete",
            results_found=len(results)
        )
        
        return results
    
    def _build_error_query(
        self,
        error_message: str,
        entity_name: Optional[str]
    ) -> str:
        """Build optimized search query for errors."""
        query_parts = [f"Error: {error_message}"]
        
        if entity_name:
            query_parts.append(f"entity: {entity_name}")
        
        return " ".join(query_parts)
```

**Structure Principles:**
- Clear class/function separation
- Private methods prefixed with `_`
- Logical grouping of related functionality
- No god classes (< 300 lines per class)

---

### TESTING (Professional Standards)

**DO:**
```python
# test_hdl_retriever_service.py

"""Unit tests for DPL Retriever Service."""

import pytest
from data_pipeline_agent_lib.application.services import DPLRetrieverService


class TestDPLRetrieverService:
    """Test suite for DPL Retriever Service."""
    
    def test_search_error_patterns_with_entity(
        self,
        mock_retriever
    ):
        """
        Test error pattern search with entity context.
        
        Verifies that entity name is included in search query
        and results are returned correctly.
        """
        # Arrange
        service = DPLRetrieverService(mock_retriever)
        error_msg = "Timeout in pipeline"
        entity = "visits"
        
        # Act
        results = service.search_error_patterns(
            error_message=error_msg,
            entity_name=entity,
            top_k=3
        )
        
        # Assert
        assert len(results) == 3
        mock_retriever.search.assert_called_once()
        call_query = mock_retriever.search.call_args[0][0]
        assert "visits" in call_query
        assert "Timeout" in call_query
    
    def test_search_error_patterns_empty_message_raises_error(
        self,
        mock_retriever
    ):
        """Test that empty error message raises ValueError."""
        service = DPLRetrieverService(mock_retriever)
        
        with pytest.raises(ValueError, match="cannot be empty"):
            service.search_error_patterns(error_message="")
```

**Test Principles:**
- Descriptive test names
- AAA pattern (Arrange, Act, Assert)
- One assertion concept per test
- Fixtures for reusable setup
- Edge cases covered

---

### IMPORTS (Clean Organization)

**DO:**
```python
# Standard library
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

# Third-party
from pydantic import BaseModel, Field
from langchain.tools import tool

# Local - absolute imports
from data_pipeline_agent_lib.utils import get_logger, ResponseFormatter
from data_pipeline_agent_lib.infrastructure.vector_store import DPLRetriever
from data_pipeline_agent_lib.domain.entities import DPLError

# Initialize module-level instances
logger = get_logger(__name__)
```

**Order:**
1. Standard library
2. Third-party packages
3. Local application imports
4. Module-level initialization

---

### LINE LENGTH & FORMATTING

**Standards:**
- Max 88 characters per line (Black default)
- 2 blank lines between top-level definitions
- 1 blank line between methods
- 4 spaces indentation (no tabs)

**DO:**
```python
def long_function_with_many_parameters(
    parameter_one: str,
    parameter_two: Optional[int] = None,
    parameter_three: bool = False,
    parameter_four: List[str] = None
) -> Dict[str, Any]:
    """
    Function with properly formatted long parameter list.
    """
    pass
```

---

### CONSTANTS & CONFIGURATION

**DO:**
```python
# Constants at module level
MAX_SEARCH_RESULTS = 10
DEFAULT_TIMEOUT_SECONDS = 30
RETRY_ATTEMPTS = 3

# Configuration classes
class ServiceConfig:
    """Configuration for retriever service."""
    
    MAX_RESULTS: int = 10
    TIMEOUT: int = 30
    RETRY_COUNT: int = 3
    CACHE_ENABLED: bool = True
```

**DON'T:**
```python
def search(query):
    results = retriever.search(query, 10)  # ❌ Magic number
    time.sleep(30)  # ❌ Magic number
```

---

## Code Review Checklist

Before committing code, verify:

- [ ] No `print()` statements (use logger)
- [ ] No emojis in code or outputs
- [ ] All functions have type hints
- [ ] All functions have docstrings
- [ ] Specific exception handling
- [ ] Logger used for all output
- [ ] No code duplication
- [ ] Tests added for new code
- [ ] Line length < 88 chars
- [ ] Imports organized
- [ ] No magic numbers
- [ ] Professional naming

---

## EnPlatformment

**Pre-commit Hooks:**
- `ruff` for linting
- `mypy` for type checking
- `black` for formatting
- `isort` for import sorting

**CI/CD:**
- All tests must pass
- Coverage > 50%
- No linting errors
- Type checking passes

**Code Review:**
- Senior engineer approval required
- Standards adherence mandatory
- No exceptions without justification

---

## Examples from Existing Code

**Good Example (Troubleshooter):**
```python
from ..utils import get_logger, ResponseFormatter

logger = get_logger(__name__)

@tool
def troubleshoot_hdl_error(
    error_message: str,
    entity_name: Optional[str] = None,
    pipeline_type: Optional[str] = None
) -> str:
    """
    Diagnose DPL pipeline errors and provide guidance.
    
    Args:
        error_message: Error message or description
        entity_name: Optional DPL entity name
        pipeline_type: Optional pipeline type
        
    Returns:
        Troubleshooting analysis and recommendations
    """
    logger.info(
        "Diagnosing DPL error",
        entity_name=entity_name,
        pipeline_type=pipeline_type
    )
    
    result = DPLTroubleshooter.diagnose_error(
        error_message=error_message,
        entity_name=entity_name,
        pipeline_type=pipeline_type
    )
    
    response = ResponseFormatter.format_troubleshooting(result)
    return response
```

---

**Status:** ACTIVE  
**Last Updated:** 2025-10-05  
**Maintainer:** Victor Cappelletto  
**Review Required:** For any deviations

