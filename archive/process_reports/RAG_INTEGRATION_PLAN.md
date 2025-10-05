# RAG Integration + Knowledge Base Completion - Implementation Plan

**Date:** 2025-10-05  
**Priority:** CRITICAL  
**Estimated Effort:** 8-10 hours  
**Status:** IN PROGRESS

---

## Executive Summary

**Problem Identified:**
1. **Specialists have ZERO RAG integration** - They provide generic responses when called standalone
2. **Knowledge base incomplete** - Only 4 workflows documented vs 26 real workflows (13 streaming + 13 batch)

**Impact:**
- Agent acts as **generalist** instead of **specialist**
- Cannot provide specific DPL pipeline knowledge
- Assumed non-existent pipelines as real (quiz failure)

**Solution:**
- Integrate RAG into all 7 specialists
- Complete knowledge base with actual workflow JSONs
- Ensure specialists ALWAYS use DPL-specific knowledge

---

## Current State Analysis

### Specialists Status (7 total, 8 tools):

| Specialist | RAG Integration | Knowledge Source | Status |
|------------|----------------|------------------|--------|
| Troubleshooter | None | Hardcoded patterns | Generic |
| Bug Resolver | None | Hardcoded solutions | Generic |
| Performance Advisor | None | Hardcoded optimizations | Generic |
| Quality Assistant | None | Hardcoded validations | Generic |
| DPL Commander | None | Hardcoded workflows | Generic |
| Ecosystem Assistant | None | Hardcoded explanations | Generic |
| DPL Coordinator | None | Hardcoded coordination | Generic |

**Total RAG References:** 1 (non-functional)  
**Problem:** All specialists use hardcoded knowledge, no semantic search

### Knowledge Base Status:

**Files:** 41 markdown files  
**Workflow Documentation:** 1 mention only  
**Missing:**
- 13 streaming workflow JSONs
- 13 batch workflow JSONs
- Detailed trigger configurations
- Entity-specific processing logic

---

## Implementation Strategy

### Phase 1: RAG Infrastructure (1-2 hours)

**Goal:** Create reusable RAG service for all specialists

**Orders:**
1. Create `DPLRetrieverService` class in `data_pipeline_agent_lib/application/services/`
2. Implement semantic search interface
3. Add context enhancement utilities
4. Create query templates for different specialist types

**Implementation:**
```python
# data_pipeline_agent_lib/application/services/hdl_retriever_service.py

from typing import List, Optional, Dict, Any
from ...infrastructure.vector_store import DPLRetriever

class DPLRetrieverService:
    """
    Centralized RAG service for DPL specialists.
    Provides semantic search and context enhancement.
    """
    
    def __init__(self, retriever: DPLRetriever):
        self.retriever = retriever
        
    def search_error_patterns(
        self,
        error_message: str,
        entity_name: Optional[str] = None,
        pipeline_type: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar error patterns in knowledge base."""
        query = f"Error: {error_message}"
        if entity_name:
            query += f" entity: {entity_name}"
        if pipeline_type:
            query += f" pipeline: {pipeline_type}"
            
        return self.retriever.search(query, top_k=top_k)
    
    def search_workflow_knowledge(
        self,
        workflow_name: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """Search for workflow-specific knowledge."""
        query = f"workflow: {workflow_name} configuration execution"
        return self.retriever.search(query, top_k=top_k)
    
    def search_optimization_strategies(
        self,
        pipeline_name: str,
        performance_issue: str,
        top_k: int = 4
    ) -> List[Dict[str, Any]]:
        """Search for performance optimization strategies."""
        query = f"optimize {pipeline_name} {performance_issue} performance"
        return self.retriever.search(query, top_k=top_k)
    
    def search_component_documentation(
        self,
        component_name: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """Search for component documentation."""
        query = f"component: {component_name} documentation architecture"
        return self.retriever.search(query, top_k=top_k)
    
    def enhance_context(
        self,
        search_results: List[Dict[str, Any]]
    ) -> str:
        """Convert search results into enhanced context string."""
        if not search_results:
            return "No specific DPL knowledge found."
        
        context_parts = ["=== RELEVANT DPL KNOWLEDGE ===\n"]
        
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"\n[Source {i}]")
            context_parts.append(result.get("content", "N/A"))
            context_parts.append("")
        
        return "\n".join(context_parts)
```

**Validation:**
- Unit tests for each search method
- Integration test with actual knowledge base
- Performance benchmark (< 200ms per search)

---

### Phase 2-8: Refactor All Specialists (4-5 hours)

**Pattern:** Inject RAG service into each specialist

**Example Refactoring (Troubleshooter):**

**Before (Generic):**
```python
@tool
def troubleshoot_hdl_error(
    error_message: str,
    entity_name: Optional[str] = None,
    pipeline_type: Optional[str] = None
) -> str:
    # Hardcoded error patterns
    result = DPLTroubleshooter.diagnose_error(
        error_message=error_message,
        entity_name=entity_name,
        pipeline_type=pipeline_type
    )
    return format_response(result)
```

**After (RAG-Enhanced):**
```python
# Initialize RAG service (singleton)
from ..application.services import DPLRetrieverService
from ..infrastructure.vector_store import get_hdl_retriever

_rag_service = DPLRetrieverService(get_hdl_retriever())

@tool
def troubleshoot_hdl_error(
    error_message: str,
    entity_name: Optional[str] = None,
    pipeline_type: Optional[str] = None
) -> str:
    """
    Diagnose DPL pipeline errors using RAG-enhanced knowledge.
    """
    # 1. Search for similar errors in knowledge base
    search_results = _rag_service.search_error_patterns(
        error_message=error_message,
        entity_name=entity_name,
        pipeline_type=pipeline_type,
        top_k=5
    )
    
    # 2. Enhance context with retrieved knowledge
    hdl_context = _rag_service.enhance_context(search_results)
    
    # 3. Diagnose with enhanced context
    result = DPLTroubleshooter.diagnose_error(
        error_message=error_message,
        entity_name=entity_name,
        pipeline_type=pipeline_type,
        hdl_context=hdl_context  # NEW: context from RAG
    )
    
    # 4. Include knowledge sources in response
    response = format_response(result)
    if search_results:
        response += "\n\n--- KNOWLEDGE SOURCES ---\n"
        for i, sr in enumerate(search_results[:3], 1):
            response += f"\n{i}. {sr.get('source', 'Unknown')}"
    
    return response
```

**Refactoring Checklist (per specialist):**
- [ ] Add RAG service initialization
- [ ] Implement semantic search call
- [ ] Enhance context integration
- [ ] Update response formatting
- [ ] Add knowledge source attribution
- [ ] Update unit tests
- [ ] Update docstrings

**Specialists to Refactor:**
1. Troubleshooter (2 tools)
2. Bug Resolver (1 tool)
3. Performance Advisor (1 tool)
4. Quality Assistant (1 tool)
5. DPL Commander (2 tools)
6. Ecosystem Assistant (2 tools) - Already has some knowledge, enhance
7. DPL Coordinator (1 tool)

---

### Phase 9-10: Complete Knowledge Base (2-3 hours)

**Goal:** Document all 26 workflows with actual JSONs

**Task 1: Create Workflow Documentation Template**
```markdown
# Workflow: {workflow_name}

## Type
- **Category:** Streaming / Batch
- **Entity:** {entity_name}

## Configuration
- **Trigger:** file_arrival / CRON
- **Schedule:** {cron_expression}
- **Cluster Policy:** {policy_id}

## Workflow JSON
\`\`\`json
{actual workflow JSON from Databricks}
\`\`\`

## Orders
1. **Task Name:** bronze_ingestion_streaming
   - **Notebook:** hdl_stm/layers/bronze/bronze_ingestion.py
   - **Purpose:** Event Hub → Bronze layer

2. **Task Name:** silver_ingestion_streaming
   - **Notebook:** hdl_stm/layers/silver/{entity}.py
   - **Purpose:** Bronze → Silver harmonized

## Troubleshooting
- **Common Issues:** [list]
- **Debug Tools:** [list]
- **Escalation:** [when to escalate]
```

**Task 2: Document 13 Streaming Workflows**

Create files in `data_pipeline_agent_lib/knowledge/workflows/streaming/`:
1. `dpl-stream-visits.md`
2. `dpl-stream-tasks.md`
3. `dpl-stream-userclientcatalog.md`
4. `dpl-stream-vendorgroups.md`
5. `dpl-stream-activitystaging.md`
6. `dpl-stream-offline_orders.md`
7. `dpl-stream-pre_orders.md`
8. `dpl-stream-ucc_eligibility.md`
9. `dpl-stream-visits_eligibility.md`
10. `dpl-stream-{4 more entities}.md`

**Task 3: Document 13 Batch Workflows**

Create files in `data_pipeline_agent_lib/knowledge/workflows/batch/`:
1. `dpl-ingestion-Orders.md`
2. `dpl-ingestion-OnTapUserSessions.md`
3. `dpl-ingestion-PartnerGroups.md`
4. `dpl-ingestion-UserProductCatalog.md`
5. `dpl-ingestion-EventStaging.md`
6. `sharedtables-ingestion.md` (multi-entity)
7. `dpl-ingestion-{7 more entities}.md`

**Task 4: Update Master Index**

Update `data_pipeline_agent_lib/knowledge/hdl_master_index.md`:
```markdown
## Workflows

### Streaming Workflows (13)
- [dpl-stream-visits](workflows/streaming/dpl-stream-visits.md)
- [dpl-stream-tasks](workflows/streaming/dpl-stream-tasks.md)
...

### Batch Workflows (13)
- [dpl-ingestion-Orders](workflows/batch/dpl-ingestion-Orders.md)
- [dpl-ingestion-OnTapUserSessions](workflows/batch/dpl-ingestion-OnTapUserSessions.md)
...
```

**Data Source:**
- Victor to provide actual workflow JSONs from Databricks
- Alternative: Extract from repository if available

---

### Phase 11: Testing (1 hour)

**Goal:** Verify RAG integration works correctly

**Test 1: Specific Knowledge Test**
```python
# Test that specialists return DPL-specific knowledge
result = troubleshoot_hdl_error("Timeout error in dpl-stream-visits after 1h30m")

# Should now reference:
# - Actual dpl-stream-visits workflow
# - Specific tasks (bronze_ingestion_streaming, silver_ingestion_streaming)
# - Real troubleshooting steps from knowledge base
# - NOT assume non-existent pipelines
```

**Test 2: Knowledge Source Attribution**
```python
# Verify knowledge sources are cited
assert "KNOWLEDGE SOURCES" in result
assert "dpl-stream-visits" in result or "knowledge base" in result
```

**Test 3: Standalone vs Full Agent**
```python
# Test that specialist in standalone mode uses RAG
standalone_result = troubleshoot_hdl_error("Pipeline error")
assert "No specific DPL knowledge" not in standalone_result

# Should retrieve and use knowledge even without full agent context
```

**Test 4: Quiz Repeat**
```python
# Repeat the quiz that failed before
query = "Timeout error in hdl-batch-tasks after 1h30m"
result = troubleshoot_hdl_error(query)

# Should now:
# - Recognize hdl-batch-tasks doesn't exist (via RAG search)
# - Suggest correct workflow name (dpl-ingestion-Orders)
# - Provide specific troubleshooting for Orders entity
```

**Unit Tests to Create:**
- `test_hdl_retriever_service.py` (12 tests)
- `test_rag_integration_troubleshooter.py` (8 tests)
- `test_rag_integration_all_specialists.py` (7 tests)

**E2E Tests to Update:**
- Update existing E2E tests to verify RAG usage
- Add new E2E test: "Agent Quiz with RAG"

---

### Phase 12: Final Package Build (30 min)

**Orders:**
1. Run all tests (unit + E2E)
2. Verify knowledge base completeness
3. Clean build artifacts
4. Rebuild .whl package
5. Verify package includes all new workflows
6. Update CHANGELOG.md
7. Update README.md
8. Update documentation

**Build Commands:**
```bash
# Clean
rm -rf build/ dist/ data_pipeline_agent_lib.egg-info/

# Test
pytest tests/unit/ -v
pytest tests/e2e/ -v --api-key=$ANTHROPIC_API_KEY

# Build
python setup.py bdist_wheel

# Verify
unzip -l dist/*.whl | grep "knowledge/workflows"
# Should show 26+ workflow files
```

**Expected Package:**
- **Version:** 3.1.0 (feature: RAG integration)
- **Size:** ~150KB (was 107KB, +40KB for workflows)
- **Files:** 39 Python modules + 67 knowledge files (41 + 26 workflows)
- **Tests:** 113 unit + 40 E2E (all passing)

---

## Implementation Order

### Quick Win Approach (Recommended):

**Step 1:** RAG Infrastructure (1-2h)
- Create `DPLRetrieverService`
- Test with existing knowledge base

**Step 2:** Refactor 1 Specialist (30min)
- Troubleshooter (most critical)
- Validate pattern works

**Step 3:** Refactor Remaining 6 Specialists (2-3h)
- Apply pattern to all
- Parallel work possible

**Step 4:** Document 3-5 Critical Workflows (1h)
- dpl-stream-visits
- dpl-stream-tasks
- dpl-ingestion-Orders
- dpl-ingestion-OnTapUserSessions
- sharedtables-ingestion

**Step 5:** Test & Validate (1h)
- Run quiz tests
- Verify improvements

**Step 6:** Complete Remaining Workflows (1-2h)
- Document remaining 21 workflows
- Victor provides JSONs

**Step 7:** Final Build & Documentation (30min)

**Total Estimated:** 6-8 hours (conservative)

---

## Success Criteria

### Must Have:
- [ ] All 7 specialists use RAG service
- [ ] At least 5 critical workflows documented
- [ ] Quiz test passes (no assumed pipelines)
- [ ] Standalone specialists return specific knowledge
- [ ] All unit tests passing

### Should Have:
- [ ] All 26 workflows documented
- [ ] Knowledge source attribution in responses
- [ ] Performance < 300ms per specialist call
- [ ] Documentation updated

### Nice to Have:
- [ ] Workflow JSON validation
- [ ] Automatic workflow sync from Databricks
- [ ] RAG performance metrics
- [ ] Knowledge base versioning

---

## Risks & Mitigation

### Risk 1: Missing Workflow JSONs
**Impact:** Cannot complete knowledge base  
**Mitigation:** Start with 5 critical workflows, get JSONs from Victor

### Risk 2: RAG Performance
**Impact:** Slow specialist responses  
**Mitigation:** Implement caching, optimize vector search

### Risk 3: Context Window Limits
**Impact:** Too much context for LLM  
**Mitigation:** Implement smart truncation, summary

### Risk 4: Breaking Existing Tests
**Impact:** Regression in functionality  
**Mitigation:** Comprehensive test suite, incremental changes

---

## Next Steps

**IMMEDIATE (Today):**
1. Create `DPLRetrieverService` class
2. Refactor Troubleshooter specialist
3. Test with existing knowledge base

**SHORT TERM (This Week):**
4. Refactor remaining 6 specialists
5. Document 5 critical workflows
6. Run comprehensive tests

**MEDIUM TERM (Next Week):**
7. Complete all 26 workflow docs
8. Production deployment
9. Monitor performance

---

**Status:** Ready to begin Phase 1  
**Next Action:** Create DPLRetrieverService infrastructure  
**Estimated Time to Complete:** 6-8 hours


