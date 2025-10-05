# Exemplos de Uso do RAG

**Última Atualização**: 2025-10-05  
**Versão**: 3.1

Este guia mostra como o sistema RAG funciona na prática com exemplos reais de código e outputs.

---

## Exemplo 1: Troubleshooting com RAG

### Cenário
Usuário reporta erro de timeout em pipeline streaming.

### Código

```python
from dpl_agent_lib.specialists import troubleshoot_hdl_error

# Reportar erro
error = "Timeout após 1h30m no pipeline dpl-stream-visits"

# Especialista usa RAG automaticamente
result = troubleshoot_hdl_error(error)
print(result)
```

### Output Esperado

```
DIAGNÓSTICO: Pipeline dpl-stream-visits - Timeout

SEVERIDADE: High
CONFIANÇA: 85%

CAUSA RAIZ:
Baseado na documentação (fonte: troubleshooting/streaming-issues.md),
timeouts em pipelines streaming após 1h+ geralmente indicam:
- Processamento de batch acumulado (micro-batches muito grandes)
- Falta de recursos (CPU/memória no cluster)  
- Queries SQL complexas na transformação Silver

AÇÕES IMEDIATAS:
1. Verificar tamanho dos micro-batches no streaming
2. Revisar utilização de recursos do cluster
3. Inspecionar localização do checkpoint
4. Verificar conectividade com Event Hub

INVESTIGAÇÃO RECOMENDADA:
1. Verificar duração de execução do pipeline
2. Revisar utilização de recursos do cluster
3. Verificar volume de dados processados
4. Inspecionar localização do checkpoint

FERRAMENTAS RELEVANTES:
- GetLastUpdatedAt.py
- Databricks Workflows Tab

--- DPL KNOWLEDGE SOURCES ---

1. troubleshooting/streaming-issues.md (Relevância: 0.94)
2. workflows/dpl-stream-visits.json (Relevância: 0.89)
3. best-practices/streaming-optimization.md (Relevância: 0.82)
```

### O Que Aconteceu Internamente

```python
# 1. Especialista chama RAG service
rag_service = get_hdl_retriever_service()

# 2. Busca na base de conhecimento
search_results = rag_service.search_error_patterns(
    error_message="Timeout após 1h30m no pipeline dpl-stream-visits",
    entity_name="visits",
    pipeline_type="streaming",
    top_k=5
)
# Retorna: Top-5 documentos mais similares com scores

# 3. Formata contexto
context = rag_service.enhance_context(search_results)
# Resultado: Texto formatado com documentos recuperados

# 4. LLM gera diagnóstico baseado no contexto
diagnosis = llm.invoke(f"{context}\n\nDiagnostique: {error}")

# 5. Inclui citações das fontes
response = diagnosis + "\n\n--- DPL KNOWLEDGE SOURCES ---\n" + sources
```

---

## Exemplo 2: Verificando RAG Manualmente

### Cenário
Você quer ver o que o RAG recupera antes de gerar resposta.

### Código

```python
from dpl_agent_lib.application.services import get_hdl_retriever_service

# Obter serviço RAG
rag_service = get_hdl_retriever_service()

# Buscar manualmente na base de conhecimento
results = rag_service.search_error_patterns(
    error_message="timeout streaming",
    entity_name="visits",
    top_k=3
)

# Inspecionar resultados
for i, doc in enumerate(results, 1):
    print(f"\n[Documento {i}]")
    print(f"Score: {doc['score']:.3f}")
    print(f"Fonte: {doc['source']}")
    print(f"Conteúdo: {doc['content'][:300]}...")
    print("-" * 80)
```

### Output Esperado

```
[Documento 1]
Score: 0.942
Fonte: troubleshooting/streaming-issues.md
Conteúdo: ## Streaming Pipeline Timeouts

Timeouts em pipelines streaming geralmente ocorrem quando:
1. Micro-batches estão muito grandes
2. Processamento está mais lento que ingestão
3. Checkpoint está corrompido ou inacessível

**Diagnóstico:**
- Verificar tamanho dos batches
- Revisar Spark UI para identificar...
--------------------------------------------------------------------------------

[Documento 2]
Score: 0.891
Fonte: workflows/dpl-stream-visits.json
Conteúdo: {
  "name": "dpl-stream-visits",
  "pipeline_type": "streaming",
  "entity": "visits",
  "triggers": [
    {
      "type": "file_arrival",
      "source": "Event Hub"
    }
  ],
  "tasks": [
    {
      "name": "bronze_ingestion",
      "notebook": "Bronze/Visits"
    }
  ]
}...
--------------------------------------------------------------------------------

[Documento 3]
Score: 0.823
Fonte: best-practices/streaming-optimization.md
Conteúdo: # Otimização de Pipelines Streaming

## Performance Guidelines

Para pipelines streaming no DPL:
- Limitar micro-batch size a 10.000 registros
- Usar Auto Loader para ingestão eficiente
- Configurar checkpoints em Delta Tables
- Monitorar latência end-to-end...
--------------------------------------------------------------------------------
```

---

## Exemplo 3: Buscar Conhecimento Sobre Workflow

### Código

```python
from dpl_agent_lib.application.services import get_hdl_retriever_service

rag_service = get_hdl_retriever_service()

# Buscar informações sobre workflow específico
results = rag_service.search_workflow_knowledge(
    workflow_name="dpl-stream-visits",
    include_config=True,
    top_k=3
)

# Ver o que foi encontrado
for doc in results:
    print(f"Fonte: {doc['source']}")
    print(f"Score: {doc['score']:.2f}")
    print(f"Conteúdo: {doc['content'][:200]}...\n")
```

---

## Exemplo 4: Workflow Completo com Agent

### Código

```python
from dpl_agent_lib.agent import create_agent

# Criar agent completo (orquestra RAG + especialistas)
agent = create_agent()

# Fazer pergunta complexa
response = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Como otimizar o pipeline visits que está processando muito lento?"
    }]
})

# Exibir resposta
print(response["messages"][-1]["content"])
```

### O Que Acontece Internamente

```
1. LangGraph classifica intenção → Performance Advisor
2. Performance Advisor chama RAG:
   - search_optimization_strategies("visits", "processamento lento")
3. RAG recupera documentos sobre otimização de visits
4. Performance Advisor constrói prompt com contexto
5. LLM gera recomendações específicas do DPL
6. Agent retorna resposta com citações
```

### Output Esperado

```
ANÁLISE DE PERFORMANCE: dpl-stream-visits

Com base na documentação DPL, identifiquei as seguintes otimizações:

1. CONFIGURAÇÃO DE MICRO-BATCH
   - Limitar tamanho a 10.000 registros (fonte: best-practices/streaming-optimization.md)
   - Ajustar trigger interval para 5 minutos
   
2. PARTICIONAMENTO
   - Particionar por date_hour para melhor distribuição
   - Evitar data skew em datas específicas
   
3. AUTO LOADER
   - Usar cloudFiles para ingestão incremental
   - Configurar checkpointLocation em Delta Table
   
4. RECURSOS DO CLUSTER
   - Aumentar executors para 8 nodes
   - Configurar autoscaling

FONTES CONSULTADAS:
- best-practices/streaming-optimization.md
- workflows/dpl-stream-visits.json
- architecture/delta-lake-optimization.md
```

---

## Exemplo 5: Testar RAG com Query Customizada

### Código

```python
from dpl_agent_lib.application.services import get_hdl_retriever_service

rag_service = get_hdl_retriever_service()

# Buscar estratégias de otimização
results = rag_service.search_optimization_strategies(
    pipeline_name="dpl-stream-visits",
    performance_issue="Alta latência no processamento Silver",
    top_k=4
)

# Formatar contexto para LLM
context = rag_service.enhance_context(results, max_length=2000)

print(context)
```

### Output

```
=== RELEVANT DPL KNOWLEDGE ===

[Source 1] (Relevance: 0.91)
Document: best-practices/silver-optimization.md
Processamento Silver pode ter alta latência devido a:
- Joins complexos sem broadcast
- Falta de particionamento adequado
- Z-ordering não configurado

Recomendações:
1. Usar broadcast joins para tabelas pequenas (<10GB)
2. Particionar por campos de filtro comum
3. Executar OPTIMIZE + ZORDER após cargas grandes
...

[Source 2] (Relevance: 0.87)
Document: architecture/delta-lake-best-practices.md
...
```

---

## Exemplo 6: Verificar Integração RAG em Especialista

### Código de Teste

```python
def test_rag_integration():
    """Teste para verificar se RAG está realmente integrado."""
    from dpl_agent_lib.specialists import troubleshoot_hdl_error
    
    # Testar com workflow INEXISTENTE
    result = troubleshoot_hdl_error("erro no workflow-fake-xyz-123")
    
    # Se RAG integrado → deve mencionar que não encontrou docs
    # Se RAG NÃO integrado → vai dar diagnóstico genérico
    
    print("=== RESULTADO DO TESTE ===")
    print(result)
    print("\n=== ANÁLISE ===")
    
    if "não encontrado" in result.lower() or "knowledge sources" in result.lower():
        print("✅ RAG INTEGRADO: Especialista consultou base de conhecimento")
    else:
        print("❌ RAG NÃO INTEGRADO: Resposta genérica sem busca na base")

# Executar teste
test_rag_integration()
```

---

## Exemplo 7: Buscar Regras de Qualidade

### Código

```python
from dpl_agent_lib.application.services import get_hdl_retriever_service

rag_service = get_hdl_retriever_service()

# Buscar regras de qualidade para entidade específica
results = rag_service.search_quality_validation_rules(
    entity_name="visits",
    quality_dimension="completeness",
    top_k=4
)

# Ver regras recuperadas
for doc in results:
    print(f"\nScore: {doc['score']:.2f}")
    print(f"Fonte: {doc['source']}")
    print(doc['content'][:300])
    print("-" * 80)
```

---

## Exemplo 8: Buscar Documentação de Componente

### Código

```python
from dpl_agent_lib.application.services import get_hdl_retriever_service

rag_service = get_hdl_retriever_service()

# Buscar documentação sobre componente DPL
results = rag_service.search_component_documentation(
    component_name="BaseTable",
    top_k=3
)

# Formatar contexto
context = rag_service.enhance_context(results)
print(context)
```

---

## Debugging RAG

### Ver Log de Operações RAG

```python
import logging

# Ativar logs detalhados
logging.basicConfig(level=logging.DEBUG)

from dpl_agent_lib.specialists import troubleshoot_hdl_error

# Executar - verá logs de RAG no console
result = troubleshoot_hdl_error("timeout")
```

### Logs Esperados

```
DEBUG:dpl_agent_lib.application.services.dpl_retriever_service:Searching error patterns
  error_length=7
  entity=None
  pipeline_type=None
  top_k=5

INFO:dpl_agent_lib.application.services.dpl_retriever_service:Error pattern search complete
  results_found=5
  query_length=28

INFO:dpl_agent_lib.application.services.dpl_retriever_service:Context enhancement complete
  sources_included=5
  total_length=1847

INFO:dpl_agent_lib.specialists.troubleshooter:RAG search complete
  results_found=5
  context_length=1847
```

---

## Métricas RAG

### Verificar Performance

```python
import time
from dpl_agent_lib.application.services import get_hdl_retriever_service

rag_service = get_hdl_retriever_service()

# Medir tempo de busca
start = time.time()
results = rag_service.search_error_patterns("timeout", top_k=5)
elapsed = time.time() - start

print(f"Tempo de busca: {elapsed:.3f}s")
print(f"Documentos recuperados: {len(results)}")
print(f"Score médio: {sum(r['score'] for r in results) / len(results):.3f}")
```

### Output Típico

```
Tempo de busca: 0.142s
Documentos recuperados: 5
Score médio: 0.847
```

---

## Troubleshooting

### Problema: "RAG service initialization failed"

**Causa**: Base de conhecimento não foi carregada ou ChromaDB não acessível.

**Solução**:
```bash
# Carregar base de conhecimento
python scripts/load_knowledge_base.py

# Verificar se ChromaDB está acessível
ls -la chroma_db/
```

### Problema: Scores muito baixos (<0.5)

**Causa**: Query não está bem formulada ou conhecimento não existe na base.

**Solução**:
```python
# Tentar query mais específica
results = rag_service.search_error_patterns(
    error_message="timeout streaming visits event hub",  # Mais específico
    entity_name="visits",
    pipeline_type="streaming"
)
```

### Problema: Nenhum resultado retornado

**Causa**: Threshold de similaridade muito alto ou base vazia.

**Solução**:
```python
# Verificar se base de conhecimento tem documentos
from dpl_agent_lib.infrastructure.vector_store import get_hdl_retriever

retriever = get_hdl_retriever()
# Verificar collection não está vazia
```

---

## Próximos Passos

- 📖 [Explicação Técnica Completa do RAG](../architecture/rag-explained.md)
- 🏗️ [Arquitetura & Fluxo do Agent](../architecture/agent-flow.md)
- 🔧 [Visão Geral dos Especialistas](../specialists/overview.md)
- 🧪 [Resultados de Testes](../testing/test-results.md)

---

**Última Atualização**: 2025-10-05  
**Versão**: 3.1


