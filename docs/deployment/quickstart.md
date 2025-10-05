# Guia de Início Rápido

Comece a usar o DPL Agent v3.0 em menos de 5 minutos!

---

## Instalação (1 minuto)

### Notebook Databricks
```python
# Instalar o pacote
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl

# Reiniciar kernel Python
dbutils.library.restartPython()
```

---

## Uso Básico (2 minutos)

### Opção 1: Usar Especialistas Diretamente (Não Requer Chave API)

Perfeito para uso offline ou quando você não tem chaves API configuradas.

```python
from data_pipeline_agent_lib.specialists import (
    troubleshoot_hdl_error,
    resolve_hdl_bug,
    optimize_hdl_pipeline
)

# Solucionar um erro
result = troubleshoot_hdl_error(
    "Erro de timeout após 1h30m no pipeline dpl-stream-visits"
)
print(result)

# Obter etapas de resolução de bug
result = resolve_hdl_bug(
    "Coluna is_current do SCD2 tem valores incorretos"
)
print(result)

# Obter conselhos de otimização de performance
result = optimize_hdl_pipeline(
    "Pipeline batch para entidade tasks está levando 2 horas"
)
print(result)
```

### Opção 2: Usar Agent Completo (Requer Chave API)

Para assistência interativa e consciente do contexto com RAG e LLM.

```python
import os
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph, create_initial_state
from data_pipeline_agent_lib.utils import create_conversation_config

# Definir chave API (usar secrets do Databricks em produção!)
os.environ["ANTHROPIC_API_KEY"] = "sua-chave-api"

# Criar agent
graph = create_data_pipeline_agent_graph()
config = create_conversation_config("minha_sessao")

# Fazer uma pergunta
query = "Meu pipeline de visits está expirando. Me ajude a solucionar."
state = create_initial_state(query)
result = graph.invoke(state, config)

print(result["final_response"])
```

---

## Configuração de Chave API (Produção)

### Usando Databricks Secrets (Recomendado)
```python
# Recuperar chave API do secret scope seguro
api_key = dbutils.secrets.get(
    scope="hdl-agent-secrets",
    key="anthropic-api-key"
)

import os
os.environ["ANTHROPIC_API_KEY"] = api_key
```

---

## Casos de Uso Comuns

### Caso 1: Diagnosticar Erro de Pipeline
```python
from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error

result = troubleshoot_hdl_error(
    "ConnectionRefusedError: Conexão MongoDB recusada"
)
# Retorna: Diagnóstico, severidade, ações imediatas, etapas de investigação
```

### Caso 2: Obter Conselhos de Performance
```python
from data_pipeline_agent_lib.specialists import optimize_hdl_pipeline

result = optimize_hdl_pipeline(
    "Pipeline hdl-batch-orders levando 3 horas ao invés de 30 minutos"
)
# Retorna: Recomendações de otimização, melhoria esperada
```

### Caso 3: Coordenar Reprocessamento Urgente
```python
from data_pipeline_agent_lib.specialists import coordinate_hdl_reprocessing

result = coordinate_hdl_reprocessing(
    "URGENTE: Preciso reprocessar entidade TASKS para 4 de outubro. "
    "Cliente aguardando. Notificar equipe KPI depois."
)
# Retorna: Plano passo a passo de reprocessamento, coordenação de equipe
```

### Caso 4: Validar Qualidade de Dados
```python
from data_pipeline_agent_lib.specialists import validate_hdl_data_quality

result = validate_hdl_data_quality(
    "Verificar completude e consistência para entidade visits na camada silver"
)
# Retorna: Checklist de qualidade, descobertas, recomendações
```

### Caso 5: Aprender Arquitetura DPL
```python
from data_pipeline_agent_lib.specialists import explain_hdl_component

result = explain_hdl_component("Processo de merge SCD2")
# Retorna: Explicação detalhada, conceitos relacionados
```

---

## Conversas Multi-turno

```python
# Turno 1: Perguntar sobre camada bronze
state1 = create_initial_state("O que é a camada bronze?")
result1 = graph.invoke(state1, config)
print(result1["final_response"])

# Turno 2: Pergunta de acompanhamento (agent lembra do contexto)
state2 = create_initial_state("E a camada silver?")
state2["messages"] = result1["messages"] # Carregar conversa
result2 = graph.invoke(state2, config)
print(result2["final_response"])
```

---

## Todos os Especialistas Disponíveis

| Especialista | Função | API Requerida? |
|------------|----------|---------------|
| **Troubleshooter** | `troubleshoot_hdl_error()` | Não |
| **Bug Resolver** | `resolve_hdl_bug()` | Não |
| **Performance Advisor** | `optimize_hdl_pipeline()` | Não |
| **Quality Assistant** | `validate_hdl_data_quality()` | Não |
| **DPL Commander** | `execute_hdl_workflow()` | Não |
| **Ecosystem Assistant** | `explain_hdl_component()` | Não |
| **DPL Coordinator** | `coordinate_hdl_reprocessing()` | Não |

**Nota:** Todos os especialistas funcionam sem chaves API! O agent completo (com LLM) requer `ANTHROPIC_API_KEY`.

---

## Verificar Instalação

```python
# Verificar se o pacote está instalado
try:
    import data_pipeline_agent_lib
    from data_pipeline_agent_lib.specialists import troubleshoot_hdl_error
    
    print("✓ DPL Agent instalado com sucesso!")
    
    # Teste rápido
    result = troubleshoot_hdl_error("Erro de teste")
    print("✓ Especialistas funcionando!")
    
except ImportError as e:
    print(f"✗ Problema na instalação: {e}")
```

---

## Precisa de Ajuda?

### Problemas Comuns

**Erro de Import:**
```python
# Reiniciar kernel Python
dbutils.library.restartPython()
```

**Erro de Chave API:**
```python
# Verificar se a chave API está configurada
import os
print("Chave API configurada:", "ANTHROPIC_API_KEY" in os.environ)
```

### Documentação
- Guia completo de deployment: `docs/deployment/production-deployment.md`
- Arquitetura: `docs/architecture/clean-architecture.md`
- Visão geral dos especialistas: `docs/specialists/overview.md`

---

## Você Está Pronto!

Comece a usar o DPL Agent para:
- Solucionar erros de pipeline
- Obter conselhos de otimização de performance
- Validar qualidade de dados
- Coordenar reprocessamento
- Aprender arquitetura DPL

**Próximos Passos:**
- Explorar ferramentas especialistas
- Experimentar o agent completo com suas consultas
- Ler a documentação de arquitetura
- Revisar exemplos do mundo real

---

**Início Rápido Completo!** 
**Versão:** 3.0.0 
**Status:** Pronto para Produção
