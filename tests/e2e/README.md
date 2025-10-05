# DPL Agent v3.0 - End-to-End Tests

## Overview

This directory contains **End-to-End (E2E) tests** for the DPL Agent v3.0, validating the complete agent workflow including LangGraph orchestration, RAG retrieval, tool calling with specialists, and conversation memory.

---

## 🔑 Requirements

### API Keys Required

E2E tests **require API keys** to run because they interact with real LLM services:

```bash
# Required
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Optional (if using OpenAI embeddings)
export OPENAI_API_KEY="your-openai-api-key"
```

### Environment Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Ensure all dependencies are installed
pip install -r requirements-dev.txt
```

---

## 📁 Test Files

| File | Purpose | Tests | Duration |
|------|---------|-------|----------|
| `test_simple_queries.py` | Basic Q&A without tools | ~15 | Fast (~10s) |
| `test_tool_calling.py` | Tool selection & execution | ~12 | Medium (~30s) |
| `test_conversation_memory.py` | Multi-turn conversations | ~8 | Medium (~25s) |
| `test_specialist_integration.py` | Specialist integration | ~10 | Slow (~45s) |
| `test_real_world_scenarios.py` | Real operational cases | ~9 | Slow (~60s) |

**Total:** ~54 E2E tests

---

## 🚀 Running E2E Tests

### Run All E2E Tests

```bash
pytest tests/e2e/ -v
```

### Run Specific Test File

```bash
# Simple queries only
pytest tests/e2e/test_simple_queries.py -v

# Tool calling tests
pytest tests/e2e/test_tool_calling.py -v

# Real-world scenarios
pytest tests/e2e/test_real_world_scenarios.py -v
```

### Run by Markers

```bash
# All E2E tests
pytest -m e2e -v

# Only slow tests
pytest -m slow -v

# Skip slow tests (faster execution)
pytest -m "e2e and not slow" -v
```

### Run with Output Capture

```bash
# See detailed output
pytest tests/e2e/ -v -s

# Quiet mode
pytest tests/e2e/ -q
```

---

## 🎯 What E2E Tests Validate

### 1. **LangGraph Workflow**
- ✅ StateGraph execution
- ✅ Node transitions
- ✅ Conditional routing
- ✅ Iteration management

### 2. **RAG System**
- ✅ Document retrieval from vector store
- ✅ Context relevance
- ✅ Semantic search quality
- ✅ Context integration in responses

### 3. **Tool Calling**
- ✅ Intelligent tool selection
- ✅ Tool execution with specialists
- ✅ Result aggregation
- ✅ Error handling during tool calls

### 4. **Conversation Memory**
- ✅ Multi-turn conversation tracking
- ✅ Context preservation across turns
- ✅ Message history management
- ✅ Checkpointing functionality

### 5. **Specialist Integration**
- ✅ All 7 specialists working in workflow
- ✅ Appropriate specialist selection
- ✅ Result integration in responses
- ✅ Multi-specialist coordination

### 6. **Real-World Scenarios**
- ✅ Urgent reprocessing (Victor's TASKS case)
- ✅ Streaming checkpoint timeouts
- ✅ CosmosDB connection failures
- ✅ Performance optimization requests
- ✅ Data quality investigations

---

## 📊 Test Markers

| Marker | Purpose | Usage |
|--------|---------|-------|
| `@pytest.mark.e2e` | All E2E tests | Distinguish from unit tests |
| `@pytest.mark.asyncio` | Async tests | Enable async test execution |
| `@pytest.mark.slow` | Long-running tests | Skip for quick validation |

---

## ⚙️ Configuration

### pytest.ini

```ini
[tool:pytest]
markers =
    e2e: End-to-end tests requiring API keys
    slow: Slow tests (>30 seconds)
    asyncio: Async test cases

asyncio_mode = strict
```

---

## 🐛 Troubleshooting

### Tests Skipped

**Reason:** API keys not set

```
SKIPPED [1] tests/e2e/conftest.py:18: ANTHROPIC_API_KEY not set
```

**Solution:** Set `ANTHROPIC_API_KEY` environment variable

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Tests Timeout

**Reason:** LLM calls can be slow

**Solution:** Increase pytest timeout

```bash
pytest tests/e2e/ --timeout=120
```

### Tests Fail Intermittently

**Reason:** LLM responses can vary

**Solution:** Use flexible assertions (check for keywords, not exact matches)

---

## 📈 Performance Expectations

### Execution Times (Approximate)

- **Simple queries:** 1-2 seconds per test
- **Tool calling:** 3-5 seconds per test
- **Multi-turn conversations:** 5-10 seconds per test
- **Complex scenarios:** 10-15 seconds per test

**Total suite runtime:** ~3-5 minutes (with API calls)

---

## 🎓 Best Practices

### 1. Use Flexible Assertions

```python
# ✅ GOOD: Check for keywords
assert "bronze" in response.lower()

# ❌ AVOID: Exact string matching
assert response == "The bronze layer is..."
```

### 2. Test Behavior, Not Implementation

```python
# ✅ GOOD: Test that tool was useful
assert len(result["final_response"]) > 100
assert "timeout" in result["final_response"].lower()

# ❌ AVOID: Test internal state details
assert result["tools_to_call"] == ["troubleshoot_hdl_error"]
```

### 3. Separate Fast and Slow Tests

```python
@pytest.mark.e2e
async def test_fast_query():
    """Fast test without tools."""
    pass

@pytest.mark.e2e
@pytest.mark.slow
async def test_complex_scenario():
    """Slow test with multiple specialists."""
    pass
```

### 4. Use Unique Thread IDs

```python
# ✅ GOOD: Unique thread per test
thread_id = f"test_{datetime.utcnow().timestamp()}"

# ❌ AVOID: Hardcoded thread IDs
thread_id = "test_thread"  # Can cause conflicts
```

---

## ✅ Success Criteria

E2E tests are considered successful when:

1. ✅ All tests pass (or are appropriately skipped)
2. ✅ No emojis in agent responses
3. ✅ Responses are substantive (>50 characters)
4. ✅ Tool calling works for appropriate queries
5. ✅ Conversation memory is maintained
6. ✅ Real-world scenarios are handled correctly

---

## 🔄 CI/CD Integration

### Azure DevOps Pipeline

```yaml
- script: |
    export ANTHROPIC_API_KEY=$(ANTHROPIC_API_KEY_SECRET)
    pytest tests/e2e/ -v --junitxml=test-results-e2e.xml
  displayName: 'Run E2E Tests'
```

### Skip E2E in Quick Validation

```bash
# Run only unit tests (fast)
pytest tests/unit/ -v

# Run unit + E2E (comprehensive)
pytest tests/ -v
```

---

## 📝 Adding New E2E Tests

### Template

```python
@pytest.mark.e2e
@pytest.mark.asyncio
async def test_my_scenario(check_api_keys, conversation_thread_id):
    """Test description."""
    graph = create_data_pipeline_agent_graph()
    config = create_conversation_config(conversation_thread_id)
    
    query = "Your test query"
    initial_state = create_initial_state(query)
    
    result = await graph.ainvoke(initial_state, config)
    
    assert "final_response" in result
    # Add your assertions
```

---

**Last Updated:** 2025-10-04  
**Status:** Ready for execution with API keys

