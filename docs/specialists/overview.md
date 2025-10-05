# Visão Geral dos Especialistas DPL

O DPL Agent inclui **7 ferramentas especializadas** projetadas para diferentes cenários operacionais do DPL.

---

## Por Que Especialistas?

Em vez de um agent monolítico tentando fazer tudo, temos **especialistas focados** que se destacam em tarefas específicas:

- **Melhor precisão** - Prompts e lógica especializados
- **Manutenção mais fácil** - Atualizar um especialista sem afetar outros
- **Responsabilidades claras** - Cada especialista tem um papel definido
- **Compostável** - Usar individualmente ou em conjunto

---

## Todos os 7 Especialistas

### 1. **Troubleshooter**

**Propósito**: Diagnosticar erros e investigar problemas

**Ferramentas** (2):
- `troubleshoot_hdl_error` - Diagnóstico de erro com correspondência de padrões
- `analyze_pipeline_health` - Verificação de saúde de pipeline

**Quando usar**:
- Pipeline falhou ou está expirando
- Comportamento inesperado em streaming/batch
- Precisa entender o que deu errado

**Exemplo**:
```python
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

result = await troubleshoot_hdl_error.ainvoke({
    "error_message": "Timeout de pipeline após 90 minutos",
    "entity_name": "visits",
    "pipeline_type": "streaming"
})
```

---

### 2. **Bug Resolver**

**Propósito**: Fornecer soluções para bugs e problemas conhecidos

**Ferramentas** (1):
- `resolve_hdl_bug` - Orientação para resolução de bugs

**Quando usar**:
- Padrões de bugs conhecidos (SCD2, conversão UUID, etc.)
- Precisa de instruções de correção passo a passo
- Procurando soluções testadas

**Exemplo**:
```python
from data_pipeline_agent_lib.specialists import resolve_hdl_bug

result = await resolve_hdl_bug.ainvoke({
    "bug_description": "Flags is_current do SCD2 estão incorretos",
    "entity_name": "visits"
})
```

---

### 3. **Performance Advisor**

**Propósito**: Otimizar performance de pipeline

**Ferramentas** (1):
- `optimize_hdl_pipeline` - Estratégias de otimização de performance

**Quando usar**:
- Pipeline executando lentamente
- Precisa melhorar throughput
- Otimização de recursos necessária

**Exemplo**:
```python
from data_pipeline_agent_lib.specialists import optimize_hdl_pipeline

result = await optimize_hdl_pipeline.ainvoke({
    "pipeline_name": "hdl-batch-tasks",
    "performance_issue": "Processamento levando muito tempo"
})
```

---

### 4. **Quality Assistant**

**Propósito**: Validar qualidade de dados

**Ferramentas** (1):
- `validate_hdl_data_quality` - Validação de qualidade de dados

**Quando usar**:
- Suspeita de problemas de qualidade de dados
- Precisa de verificações de completude/precisão
- Validando após reprocessamento

**Exemplo**:
```python
from data_pipeline_agent_lib.specialists import validate_hdl_data_quality

result = await validate_hdl_data_quality.ainvoke({
    "entity_name": "visits",
    "quality_dimension": "completeness"
})
```

---

### 5. DPL Commander

**Propósito**: Executar e monitorar workflows

**Ferramentas** (2):
- `execute_hdl_workflow` - Execução de workflow
- `get_workflow_status` - Monitoramento de workflow

**Quando usar**:
- Precisa executar um workflow
- Verificar status de execução de workflow
- Monitorar progresso de pipeline

**Exemplo**:
```python
from data_pipeline_agent_lib.specialists import execute_hdl_workflow, get_workflow_status

# Executar workflow
exec_result = await execute_hdl_workflow.ainvoke({
    "workflow_name": "dpl-stream-visits",
    "parameters": {}
})

# Verificar status
status_result = await get_workflow_status.ainvoke({
    "workflow_name": "dpl-stream-visits"
})
```

---

### 6. **Ecosystem Assistant**

**Propósito**: Explicar componentes DPL e fornecer orientação

**Ferramentas** (2):
- `explain_hdl_component` - Explicações de componentes
- `get_hdl_best_practices` - Orientação de melhores práticas

**Quando usar**:
- Aprendendo sobre arquitetura DPL
- Entendendo componentes específicos
- Precisa de orientação de melhores práticas

**Exemplo**:
```python
from data_pipeline_agent_lib.specialists import explain_hdl_component, get_hdl_best_practices

# Explicar componente
explanation = await explain_hdl_component.ainvoke({
    "component_name": "IngestionControl",
    "include_examples": True
})

# Obter melhores práticas
practices = await get_hdl_best_practices.ainvoke({
    "topic": "tratamento de erros"
})
```

---

### 7. **DPL Coordinator**

**Propósito**: Coordenar cenários de reprocessamento

**Ferramentas** (1):
- `coordinate_hdl_reprocessing` - Coordenação de reprocessamento

**Quando usar**:
- Reprocessamento urgente necessário
- Cenários de escalação do cliente
- Precisa coordenar com equipe KPI

**Exemplo**:
```python
from data_pipeline_agent_lib.specialists import coordinate_hdl_reprocessing

result = await coordinate_hdl_reprocessing.ainvoke({
    "entity_name": "tasks",
    "date_range": "2025-10-04",
    "notify_kpi_team": True
})
```

---

## Registro de Ferramentas

Todas as ferramentas são registradas e categorizadas:

```python
from data_pipeline_agent_lib.specialists import (
    ALL_DPL_TOOLS,  # Todas as 10 ferramentas
    TROUBLESHOOTING_TOOLS,  # 3 ferramentas
    OPTIMIZATION_TOOLS,  # 2 ferramentas
    OPERATIONAL_TOOLS,  # 3 ferramentas
    DOCUMENTATION_TOOLS,  # 2 ferramentas
    get_tools_for_intent  # Função auxiliar
)

# Obter ferramentas por intenção
troubleshooting = get_tools_for_intent("troubleshooting")
optimization = get_tools_for_intent("optimization")
```

---

## Arquitetura do Especialista

Cada especialista é implementado como uma **Ferramenta LangChain**:

```python
from langchain.tools import tool

@tool
async def troubleshoot_hdl_error(
    error_message: str,
    entity_name: str = None,
    pipeline_type: str = None
) -> str:
    """
    Diagnosticar erros de pipeline DPL com correspondência de padrões e análise de causa raiz.
    
    Args:
        error_message: A mensagem de erro ou sintoma
        entity_name: Entidade DPL opcional (visits, tasks, etc.)
        pipeline_type: Tipo de pipeline opcional (streaming, batch)
        
    Returns:
        Diagnóstico detalhado com etapas de investigação
    """
    # Implementação aqui
    return diagnosis
```

**Recursos Principais**:
- Suporte assíncrono
- Type hints
- Docstring para compreensão do LLM
- Entrada/saída estruturada

---

## Integração com LangGraph

Especialistas são integrados no workflow do agent:

```python
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph
from data_pipeline_agent_lib.agent.state import create_initial_state

# Criar agent (especialistas automaticamente incluídos)
agent = create_data_pipeline_agent_graph()

# Fazer pergunta
state = create_initial_state(
    query="Por que o pipeline de streaming visits está expirando?",
    session_id="session_001"
)

# Agent seleciona e usa especialistas inteligentemente
result = await agent.ainvoke(state)
```

**Workflow do Agent**:
1. **Analisar Intenção** → Determinar objetivo do usuário
2. **Selecionar Ferramentas** → Escolher especialistas relevantes
3. **Executar Ferramentas** → Executar especialistas
4. **Agregar Resultados** → Combinar saídas
5. **Gerar Resposta** → Criar resposta final

---

## Comparação de Capacidades dos Especialistas

| Especialista | Diagnóstico de Erro | Soluções | Monitoramento | Execução | Documentação |
|-----------|----------------|-----------|------------|-----------|---------------|
| Troubleshooter | ✓ | | | | |
| Bug Resolver | | ✓ | | | |
| Performance Advisor | ✓ | ✓ | | | |
| Quality Assistant | ✓ | ✓ | | | |
| DPL Commander | | | ✓ | ✓ | |
| Ecosystem Assistant | | | | | ✓ |
| DPL Coordinator | | ✓ | ✓ | | |

---

## Workflows Comuns

### Troubleshooting → Resolução

```python
# Passo 1: Diagnosticar
diagnosis = await troubleshoot_hdl_error.ainvoke({
    "error_message": "SCD2 quebrado",
    "entity_name": "visits"
})

# Passo 2: Obter solução
solution = await resolve_hdl_bug.ainvoke({
    "bug_description": "SCD2 is_current incorreto",
    "entity_name": "visits"
})
```

### Performance → Qualidade

```python
# Passo 1: Otimizar
optimization = await optimize_hdl_pipeline.ainvoke({
    "pipeline_name": "dpl-stream-visits",
    "performance_issue": "processamento lento"
})

# Passo 2: Validar
validation = await validate_hdl_data_quality.ainvoke({
    "entity_name": "visits",
    "quality_dimension": "all"
})
```

### Executar → Monitorar

```python
# Passo 1: Executar
exec_result = await execute_hdl_workflow.ainvoke({
    "workflow_name": "dpl-stream-visits"
})

# Passo 2: Monitorar
status = await get_workflow_status.ainvoke({
    "workflow_name": "dpl-stream-visits"
})
```

---

## Próximos Passos

### Explorar Mais

- **[Exemplos](../examples/basic.md)** - Exemplos práticos de uso
- **[Referência da API](../api/specialists.md)** - Documentação completa da API
- **[Arquitetura](../architecture/clean-architecture.md)** - Princípios de design
- **[Testes](../testing/test-results.md)** - Cobertura e resultados de testes

### Detalhes dos Especialistas Individuais

Todos os especialistas estão documentados acima com:
- Propósito e capacidades
- Ferramentas disponíveis
- Quando usar
- Exemplos de código

Para assinaturas detalhadas da API, veja a [Referência da API](../api/specialists.md).
