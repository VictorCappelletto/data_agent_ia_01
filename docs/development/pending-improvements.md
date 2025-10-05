# Pending Improvements

**Last Updated:** 2025-10-04 
**Status:** Identified Issues Awaiting Implementation

---

## Critical: RAG Integration Required

### Issue

**Current Behavior:**
- Specialists operate in standalone mode without accessing the knowledge base
- Provide generic troubleshooting based on pattern matching
- Do not validate if pipelines/workflows actually exist
- Cannot leverage the 164+ DPL documentation files

**Expected Behavior:**
- Specialists should ALWAYS consult RAG (Retrieval-Augmented Generation) system
- Query knowledge base before responding
- Validate workflows against documented pipelines
- Provide specialized, context-aware responses

### Impact

**Severity:** HIGH 
**Affected Components:** All 7 specialists

**Example:**
```python
# Current behavior
troubleshoot_hdl_error("hdl-batch-tasks timeout")
# Returns: Generic timeout diagnosis (workflow not validated)

# Expected behavior (after fix)
troubleshoot_hdl_error("hdl-batch-tasks timeout")
# Should: 
# 1. Query knowledge base for "hdl-batch-tasks"
# 2. Identify workflow doesn't exist (suggest dpl-ingestion-Orders.json)
# 3. Provide specific diagnosis based on actual workflow
```

### Root Cause

Specialists are implemented as standalone LangChain tools that:
- Execute business logic directly without RAG consultation
- Were designed for offline operation (no API key required)
- Do not integrate with the vector store/retriever system

### Proposed Solution

**Option A: Refactor Specialists (Recommended)**
- Integrate DPLRetriever directly into each specialist
- Query knowledge base before diagnosis/recommendation
- Maintain offline capability with cached knowledge fallback

**Option B: Platform Full Agent Usage**
- Deprecate standalone specialist calls
- Require all usage through full LangGraph agent
- Agent handles RAG → Specialist flow

**Option C: Smart Specialist Wrapper**
- Create intermediate layer (SmartSpecialist)
- Automatically queries RAG before delegating to specialist
- Transparent to existing code

### Implementation Checklist

- [ ] Design RAG integration pattern for specialists
- [ ] Implement integration in Troubleshooter (pilot)
- [ ] Validate behavior with real workflows
- [ ] Extend to remaining 6 specialists
- [ ] Update unit tests to mock RAG queries
- [ ] Update E2E tests to validate RAG integration
- [ ] Update documentation

### Knowledge Base Gap

**Current Coverage:** 4 workflows documented
- dpl-stream-visits.json
- dpl-stream-tasks.json
- dpl-ingestion-Orders.json
- dpl-ingestion-OnTapUserSessions.json

**Actual System:** 26 workflows (as per engineering team)
- 13 streaming workflows
- 13 batch workflows
- 5 primary entities: Orders, Sessions, VendorGroup, UserProductCatalog, EventStaging

**Action Required:**
1. Document all 26 workflows in knowledge base
2. Include workflow configurations, triggers, dependencies
3. Update DPL_COMPLETE_KNOWLEDGE.md with complete list

### Estimated Effort

- **RAG Integration:** 8-12 hours
- Design: 2 hours
- Implementation: 4 hours
- Testing: 4 hours
- Documentation: 2 hours

- **Knowledge Base Completion:** 4-6 hours
- Gather workflow specs: 2 hours
- Document in markdown: 2 hours
- Validation: 2 hours

**Total:** 12-18 hours

### Priority

**Priority:** P0 (Critical) 
**Reason:** Agent is currently a generalist, not a specialist as intended

### Stakeholders

- **Engineering Lead:** Victor Cappelleto
- **Affected Users:** All DPL agent users
- **Dependencies:** DPL workflow documentation

---

## Additional Improvements

### 1. Workflow JSON Documentation

**Status:** Pending 
**Priority:** P1

Complete documentation of all Databricks workflows:
- Streaming workflows (13 total)
- Batch workflows (13 total)
- Trigger configurations
- Dependency chains
- Error patterns per workflow

### 2. E2E Test Execution

**Status:** Ready, Not Executed 
**Priority:** P1

40 E2E tests created but require API key:
- Set ANTHROPIC_API_KEY in environment
- Execute full E2E test suite
- Validate coverage increase (51% → ~75%)
- Document any failures

### 3. Python 3.10+ Upgrade

**Status:** Future Enhancement 
**Priority:** P2

Current limitation: Python 3.9 (MCP compatibility)
- Upgrade to Python 3.10+ for full MCP support
- Enable SqliteSaver for persistent checkpointing
- Enhanced tool integration capabilities

### 4. Production Monitoring

**Status:** Not Implemented 
**Priority:** P2

Add production observability:
- Token usage tracking
- Query latency monitoring
- Error rate dashboards
- Cost analytics
- User feedback collection

---

## How to Contribute

### Reporting Issues

1. Document current vs expected behavior
2. Provide reproduction steps
3. Include relevant code/configuration
4. Suggest potential solutions

### Implementing Fixes

1. Create feature branch
2. Implement changes with tests
3. Update documentation
4. Submit for review

---

**Document Version:** 1.0 
**Next Review:** After RAG integration implementation

