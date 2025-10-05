# Guia de Deploy em Produção

**Pacote:** `data_pipeline_agent_lib-3.0.0-py3-none-any.whl` 
**Alvo:** Clusters Databricks 
**Status:** Pronto para Produção

---

## Checklist Pré-Deploy

### Validação de Qualidade 
- [x] Todos os testes unitários passando (113/113)
- [x] Cobertura de código aceitável (51%)
- [x] Especialistas testados completamente (91%)
- [x] Sem emojis na saída
- [x] Clean Architecture validada
- [x] Pacote construído com sucesso

### Permissões Necessárias
- [ ] Acesso de escrita DBFS
- [ ] Permissões de instalação de biblioteca no cluster
- [ ] Acesso de leitura ao secret scope (para chaves API)
- [ ] Aprovação de admin do workspace (se necessário)

---

## Etapas de Deploy

### Etapa 1: Upload do Pacote para DBFS

#### Opção A: Usando CLI do Databricks
```bash
# Instalar CLI do Databricks (se ainda não instalado)
pip install databricks-cli

# Configurar autenticação
databricks configure --token

# Upload .whl para DBFS
databricks fs cp \
  dist/data_pipeline_agent_lib-3.0.0-py3-none-any.whl \
  dbfs:/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
```

#### Opção B: Usando Interface do Databricks
1. Navegue até **Data** → **DBFS** → **FileStore**
2. Crie a pasta: `libraries/` (se não existir)
3. Clique em **Upload**
4. Selecione: `data_pipeline_agent_lib-3.0.0-py3-none-any.whl`
5. Confirme o upload

#### Opção C: Usando API Python
```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Upload do arquivo
with open("dist/data_pipeline_agent_lib-3.0.0-py3-none-any.whl", "rb") as f:
    w.dbfs.upload(
        "/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl",
        f.read()
    )
```

---

### Etapa 2: Instalar no Cluster Databricks

#### Opção A: Instalar via Interface do Cluster
1. Navegue até **Compute** → Selecione seu cluster
2. Clique na aba **Libraries**
3. Clique em **Install new**
4. Selecione **Library Source:** "DBFS/ADLS"
5. Selecione **Library Type:** "Python Whl"
6. Digite o caminho: `dbfs:/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl`
7. Clique em **Install**
8. Aguarde o status: **Installed**

#### Opção B: Instalar via Notebook
```python
# Instalar a biblioteca
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl

# Reiniciar kernel Python para usar a biblioteca
dbutils.library.restartPython()
```

#### Opção C: Instalar via Script de Init do Cluster
Criar arquivo: `dbfs:/databricks/init-scripts/install-hdl-agent.sh`
```bash
#!/bin/bash
/databricks/python/bin/pip install \
  /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
```

Adicionar à configuração do cluster:
- **Cluster** → **Advanced Options** → **Init Scripts**
- Adicionar caminho: `dbfs:/databricks/init-scripts/install-hdl-agent.sh`

---

### Etapa 3: Configurar Chaves API (Seguro)

#### Criar Secret Scope (Configuração Única)
```bash
# Usando CLI do Databricks
databricks secrets create-scope --scope hdl-agent-secrets

# Adicionar Chave API Anthropic
databricks secrets put-secret \
  --scope hdl-agent-secrets \
  --key anthropic-api-key \
  --string-value "sk-ant-api03-sua-chave-aqui"
```

#### Acessar Secrets no Notebook
```python
# Recuperar chave API do secret scope
anthropic_api_key = dbutils.secrets.get(
    scope="hdl-agent-secrets",
    key="anthropic-api-key"
)

# Definir variável de ambiente
import os
os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
```

---

### Etapa 4: Validar Instalação

#### Teste 1: Importar Pacote
```python
# Testar import básico
try:
    import data_pipeline_agent_lib
    print("✓ Pacote importado com sucesso")
    print(f"Versão: {data_pipeline_agent_lib.__version__}")
except ImportError as e:
    print(f"✗ Import falhou: {e}")
```

#### Teste 2: Testar Especialistas (Não Requer API)
```python
from data_pipeline_agent_lib.specialists import (
    troubleshoot_hdl_error,
    resolve_hdl_bug,
    optimize_hdl_pipeline
)

# Testar troubleshooter
result = troubleshoot_hdl_error("Erro de timeout de teste no pipeline de streaming")
print("✓ Troubleshooter funcionando:")
print(result[:200])

# Testar bug resolver
result = resolve_hdl_bug("Problema de corrupção is_current do SCD2")
print("\n✓ Bug Resolver funcionando:")
print(result[:200])

# Testar performance advisor
result = optimize_hdl_pipeline("Pipeline batch lento levando 2 horas")
print("\n✓ Performance Advisor funcionando:")
print(result[:200])
```

#### Teste 3: Testar Agent Completo (Requer API)
```python
import os
from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph, create_initial_state
from data_pipeline_agent_lib.utils import create_conversation_config

# Definir chave API (dos secrets)
os.environ["ANTHROPIC_API_KEY"] = dbutils.secrets.get(
    scope="hdl-agent-secrets",
    key="anthropic-api-key"
)

# Criar agent
graph = create_data_pipeline_agent_graph()
config = create_conversation_config("sessao_teste")

# Consulta de teste
query = "O que é a camada bronze no DPL?"
state = create_initial_state(query)

# Executar
result = graph.invoke(state, config)
print("✓ Agent completo funcionando:")
print(result["final_response"])
```

---

## Melhores Práticas de Segurança

### Gerenciamento de Chave API
- **Nunca hardcode** chaves API em notebooks
- **Sempre use** secrets do Databricks
- **Restrinja acesso** aos secret scopes
- **Rotacione chaves** regularmente
- **Monitore uso** para anomalias

### Permissões de Secret Scope
```bash
# Conceder acesso de leitura a usuários específicos
databricks secrets put-acl \
  --scope hdl-agent-secrets \
  --principal usuario@empresa.com \
  --permission READ

# Listar permissões
databricks secrets list-acl --scope hdl-agent-secrets
```

---

## Monitoramento & Observabilidade

### Monitoramento de Logs
```python
from data_pipeline_agent_lib.utils import get_logger, setup_logging

# Configurar logging para produção
setup_logging(level="INFO", format_type="json")

# Usar logger no seu código
logger = get_logger(__name__)
logger.info("Consulta do agent iniciada", query=query, session_id=session_id)
```

### Rastreamento de Performance
```python
import time
from datetime import datetime

def rastrear_performance_agent(query: str):
    """Rastrear performance de consulta do agent."""
    start_time = datetime.utcnow()
    
    try:
        # Executar agent
        result = graph.invoke(state, config)
        
        # Registrar sucesso
        duration = (datetime.utcnow() - start_time).total_seconds()
        logger.info(
            "Consulta do agent concluída",
            query=query,
            duration_seconds=duration,
            response_length=len(result["final_response"]),
            status="sucesso"
        )
        
        return result
        
    except Exception as e:
        # Registrar falha
        duration = (datetime.utcnow() - start_time).total_seconds()
        logger.error(
            "Consulta do agent falhou",
            query=query,
            duration_seconds=duration,
            error=str(e),
            status="falha"
        )
        raise
```

### Rastreamento de Custos
```python
def estimar_custo_token(input_text: str, output_text: str):
    """Estimar custo da chamada LLM."""
    # Estimativa aproximada: ~4 caracteres por token
    input_tokens = len(input_text) / 4
    output_tokens = len(output_text) / 4
    
    # Preços Claude 3.5 Sonnet (exemplo)
    input_cost_per_1k = 0.003 # $3 por 1M tokens
    output_cost_per_1k = 0.015 # $15 por 1M tokens
    
    cost = (input_tokens / 1000 * input_cost_per_1k +
            output_tokens / 1000 * output_cost_per_1k)
    
    logger.info(
        "Custo LLM estimado",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost_usd=cost
    )
    
    return cost
```

---

## Solução de Problemas

### Problema 1: Erros de Import
**Sintoma:** `ModuleNotFoundError: No module named 'data_pipeline_agent_lib'`

**Soluções:**
```python
# 1. Verificar instalação
%pip list | grep hdl-agent

# 2. Reinstalar
%pip install --force-reinstall \
  /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl

# 3. Reiniciar Python
dbutils.library.restartPython()
```

### Problema 2: Chave API Não Encontrada
**Sintoma:** `KeyError: 'ANTHROPIC_API_KEY'`

**Soluções:**
```python
# 1. Verificar se secret scope existe
try:
    api_key = dbutils.secrets.get("hdl-agent-secrets", "anthropic-api-key")
    print("✓ Chave API recuperada")
except Exception as e:
    print(f"✗ Falha ao obter chave API: {e}")

# 2. Verificar permissões
# Contatar admin do workspace para conceder acesso READ

# 3. Verificar variável de ambiente
import os
print(f"ANTHROPIC_API_KEY configurada: {'ANTHROPIC_API_KEY' in os.environ}")
```

### Problema 3: Timeouts do Agent
**Sintoma:** `TimeoutError` durante execução do agent

**Soluções:**
```python
# 1. Aumentar timeout para chamadas LLM
from data_pipeline_agent_lib.infrastructure.llm import AnthropicLLMProvider

llm = AnthropicLLMProvider(
    model_name="claude-3-5-sonnet-20241022",
    temperature=0.7,
    max_tokens=4000,
    timeout=120 # Aumentar timeout para 120 segundos
)

# 2. Verificar conectividade de rede
import requests
try:
    response = requests.get("https://api.anthropic.com", timeout=10)
    print(f"✓ API Anthropic acessível: {response.status_code}")
except Exception as e:
    print(f"✗ Problema de rede: {e}")
```

### Problema 4: Erros do Vector Store
**Sintoma:** Falhas de inicialização do ChromaDB

**Soluções:**
```python
# 1. Verificar caminho do ChromaDB
import os
chroma_path = "/dbfs/FileStore/chroma_db"
os.makedirs(chroma_path, exist_ok=True)

# 2. Inicializar com caminho explícito
from data_pipeline_agent_lib.infrastructure.vector_store import ChromaVectorStore

vector_store = ChromaVectorStore(
    collection_name="hdl_knowledge",
    persist_directory=chroma_path
)
```

---

## Otimização de Performance

### Estratégias de Cache
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def obter_resposta_agent_cached(query: str):
    """Cachear respostas do agent para consultas comuns."""
    state = create_initial_state(query)
    result = graph.invoke(state, config)
    return result["final_response"]
```

### Processamento em Lote
```python
def processar_consultas_lote(queries: list[str], batch_size: int = 10):
    """Processar múltiplas consultas em lotes."""
    results = []
    
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i+batch_size]
        
        # Processar lote
        batch_results = [
            graph.invoke(create_initial_state(q), config)
            for q in batch
        ]
        
        results.extend(batch_results)
        
        # Registrar progresso
        logger.info(
            "Lote processado",
            batch_num=i//batch_size + 1,
            queries_processed=len(results)
        )
    
    return results
```

---

## Procedimento de Rollback

### Se Problemas Surgirem

#### Etapa 1: Desinstalar Versão Atual
```python
%pip uninstall -y hdl-agent-lib
dbutils.library.restartPython()
```

#### Etapa 2: Instalar Versão Anterior (se disponível)
```python
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-2.0.0-py3-none-any.whl
dbutils.library.restartPython()
```

#### Etapa 3: Verificar Rollback
```python
import data_pipeline_agent_lib
print(f"Rollback para versão: {data_pipeline_agent_lib.__version__}")
```

---

## Checklist Pós-Deploy

### Validação
- [ ] Pacote instalado em todos os clusters alvo
- [ ] Chaves API configuradas no secret scope
- [ ] Especialistas testados (sem API)
- [ ] Agent completo testado (com API)
- [ ] Logging configurado
- [ ] Dashboard de monitoramento atualizado

### Documentação
- [ ] Deploy documentado
- [ ] Equipe notificada da nova versão
- [ ] Guia do usuário atualizado
- [ ] Problemas conhecidos documentados

### Operações
- [ ] Equipe de suporte briefada
- [ ] Runbook atualizado
- [ ] Procedimentos de escalação revisados
- [ ] Plano de backup/rollback validado

---

## Suporte & Escalação

### Para Problemas Contate:
- **Líder Técnico:** Victor Cappelletto
- **Admin Databricks:** [Contato do admin]
- **Azure DevOps:** [Canal da equipe]

### Caminho de Escalação:
1. Verificar seção de solução de problemas acima
2. Revisar logs do agent no Databricks
3. Verificar Azure DevOps para problemas conhecidos
4. Contatar líder técnico
5. Criar ticket de incidente se necessário

---

## Critérios de Sucesso

Deploy é bem-sucedido quando:
- Pacote instalado sem erros
- Todos os 7 especialistas funcionais
- Agent completo responde a consultas
- Sem emoji na saída
- Logging funcionando corretamente
- Chaves API seguras
- Performance aceitável (<5s por consulta)

---

**Status do Deploy:** Pronto para Produção 
**Última Atualização:** 2025-10-04 
**Versão:** 3.0.0
