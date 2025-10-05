# Início Rápido

Comece a usar o DPL Agent v3.0 em 5 minutos.

---

## Pré-requisitos

- Python 3.9+
- Workspace Databricks ou ambiente Python local
- Opcional: Chave API Anthropic (para recursos completos do agent)

---

## Instalação

```python
# Databricks
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
dbutils.library.restartPython()

# Verificar
from data_pipeline_agent_lib.specialists import ALL_DPL_TOOLS
print(f"{len(ALL_DPL_TOOLS)} ferramentas especialistas disponíveis")
```

---

## Uso Básico

### Solucionar Erro de Pipeline

```python
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

result = troubleshoot_hdl_error(
    "Pipeline de streaming de sessões expirou após 90 minutos"
)

print(result)
```

**Saída**:
```
ANÁLISE DE TROUBLESHOOTING

Diagnóstico: Padrão de erro de timeout detectado
Severidade: ALTA
Confiança: 85%

Candidatos a Causa Raiz:
- Processamento de grande volume de dados
- Restrições de recursos do cluster

Etapas de Investigação:
1. Verificar duração da execução do pipeline
2. Revisar utilização de recursos do cluster
3. Verificar volume de dados processados
4. Inspecionar localização do checkpoint
```

### Otimizar Performance

```python
from data_pipeline_agent_lib.specialists import optimize_hdl_pipeline

recommendations = optimize_hdl_pipeline(
    "hdl-batch-tasks executando por 2 horas ao invés dos 30 minutos habituais"
)

print(recommendations)
```

### Validar Qualidade de Dados

```python
from data_pipeline_agent_lib.specialists import validate_hdl_data_quality

report = validate_hdl_data_quality(
    "Verificar completude e consistência para a entidade visits"
)

print(report)
```

### Coordenar Reprocessamento

```python
from data_pipeline_agent_lib.specialists import coordinate_hdl_reprocessing

plan = coordinate_hdl_reprocessing(
    "Entidade TASKS para 4 de outubro. Cliente aguardando. Notificar equipe KPI."
)

print(plan)
```

---

## Usando o Agent Completo

Requer configuração de chave API.

### Configurar Chaves API

```python
import os

# Databricks
os.environ["ANTHROPIC_API_KEY"] = dbutils.secrets.get(
    "hdl-agent-secrets", "anthropic-api-key"
)

# Local (usar arquivo .env)
from dotenv import load_dotenv
load_dotenv()
```

### Criar Agent

```python
from data_pipeline_agent_lib.agent import create_simple_hdl_graph
from data_pipeline_agent_lib.agent.state import create_initial_state

# Inicializar agent
agent = create_simple_hdl_graph()

# Fazer pergunta
state = create_initial_state(
    query="Como posso solucionar um timeout no pipeline de streaming de visits?",
    session_id="session_001"
)

# Obter resposta
result = agent.invoke(state)
print(result["final_response"])
```

### Conversa Multi-turno

```python
from data_pipeline_agent_lib.utils.checkpointer import create_conversation_config

config = create_conversation_config("thread_001")

# Primeira pergunta
state1 = create_initial_state("O que é SCD2?", "thread_001")
result1 = agent.invoke(state1, config=config)

# Pergunta de acompanhamento (lembra do contexto)
state2 = create_initial_state("Como é usado no DPL?", "thread_001")
result2 = agent.invoke(state2, config=config)
```

---

## Especialistas Disponíveis

### Troubleshooting
- `troubleshoot_hdl_error` - Diagnóstico de erros
- `analyze_pipeline_health` - Verificação de saúde
- `resolve_hdl_bug` - Resolução de bugs

### Otimização
- `optimize_hdl_pipeline` - Recomendações de performance
- `validate_hdl_data_quality` - Validação de qualidade

### Operações
- `execute_hdl_workflow` - Execução de workflow
- `get_workflow_status` - Monitoramento
- `coordinate_hdl_reprocessing` - Coordenação de reprocessamento

### Documentação
- `explain_hdl_component` - Explicação de componentes
- `get_hdl_best_practices` - Melhores práticas

---

## Exemplos do Mundo Real

### Falha Urgente de Pipeline

```python
from data_pipeline_agent_lib.specialists import (
    troubleshoot_hdl_error,
    coordinate_hdl_reprocessing
)

# Diagnosticar
diagnosis = troubleshoot_hdl_error(
    "URGENTE: Pipeline batch TASKS expirou. Dados não estão na camada silver."
)

# Obter plano de reprocessamento
plan = coordinate_hdl_reprocessing(
    "Entidade TASKS para 4 de outubro. Cliente aguardando. Notificar equipe KPI."
)
```

### Investigação de Performance

```python
from data_pipeline_agent_lib.specialists import optimize_hdl_pipeline

advice = optimize_hdl_pipeline(
    "hdl-batch-orders levando 2 horas ao invés dos 30 minutos habituais"
)
```

### Verificação de Qualidade de Dados

```python
from data_pipeline_agent_lib.specialists import validate_hdl_data_quality

report = validate_hdl_data_quality(
    "Verificar completude e consistência para a entidade visits"
)
```

---

## Próximos Passos

1. [Guia de Instalação](installation.md) - Configuração detalhada
2. [Visão Geral dos Especialistas](../specialists/overview.md) - Todos os 7 especialistas
3. [Arquitetura](../architecture/clean-architecture.md) - Princípios de design
4. [Exemplos](../examples/basic.md) - Mais exemplos de código

---

## Suporte

- **Líder Técnico**: Victor Cappelletto
- **Projeto**: Operations Strategy - DPL Operations

---

**Última Atualização**: 2025-10-04
