# Pending Improvements

**Last Updated:** 2025-10-05  
**Status:** Tracking Future Enhancements

---

## ✅ COMPLETED: RAG Integration

### Status: IMPLEMENTED (v3.1)

**Implementation Confirmed:**
- ✅ All 7 specialists now use `DPLRetrieverService` for RAG
- ✅ Knowledge base queries happen automatically in each specialist
- ✅ Responses include citations from documentation sources
- ✅ Fallback to hardcoded patterns if RAG unavailable

**Example (Current Behavior):**
```python
from dpl_agent_lib.specialists import troubleshoot_hdl_error

# Specialist automatically uses RAG
result = troubleshoot_hdl_error("timeout no dpl-stream-visits")

# Internally:
# 1. Calls rag_service.search_error_patterns()
# 2. Retrieves Top-5 relevant docs from knowledge base
# 3. Enhances context with retrieved knowledge
# 4. LLM generates response based on documentation
# 5. Includes source citations in response
```

**Code Evidence:**
- `troubleshooter.py`: Lines 358-383 - RAG search before diagnosis
- `performance_advisor.py`: Lines 29-39 - RAG service initialization
- `quality_assistant.py`: Lines 29-39 - RAG integration
- `ecosystem_assistant.py`: Lines 20-30 - RAG service
- All specialists: Import and use `get_hdl_retriever_service()`

---

## Future Enhancements

### Priority 1: Advanced RAG Features

**Hybrid Search**
- Combine semantic search (embeddings) with keyword search (BM25)
- Better recall for technical terms and error codes
- Estimated effort: 4-6 hours

**Query Decomposition**
- Break complex questions into sub-queries
- Search knowledge base multiple times with different angles
- Estimated effort: 6-8 hours

### Priority 2: RAG Performance

**Metadata Filtering**
- Filter by document type before vector search
- Filter by entity, pipeline type, or date
- Reduces search space, improves speed
- Estimated effort: 3-4 hours

**Re-ranking with Cross-Encoder**
- Initial retrieval: Fast but less accurate
- Re-rank Top-20 with precise cross-encoder model
- Better Top-5 final results
- Estimated effort: 4-6 hours

### Priority 3: RAG Quality

**Evaluation Metrics**
- Track faithfulness (answer matches context)
- Track answer relevance (answer matches question)
- Track context precision (retrieved docs are relevant)
- Estimated effort: 8-10 hours

**Feedback Loop**
- Collect user feedback on responses
- Use feedback to improve retrieval
- Fine-tune ranking based on usage patterns
- Estimated effort: 12-16 hours

---

## Other Improvements (Non-RAG)

### Knowledge Base Expansion

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

