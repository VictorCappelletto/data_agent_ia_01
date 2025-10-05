# Instalação

Instruções de configuração para o DPL Agent v3.0 em ambientes Databricks e locais.

---

## Requisitos

- **Python**: 3.9 ou superior
- **Plataforma**: Databricks (principal) ou desenvolvimento local
- **Memória**: Mínimo de 2GB RAM
- **Armazenamento**: ~100MB para o pacote e dependências

---

## Instalação no Databricks

### Passo 1: Upload do Pacote para DBFS

**Opção A: Interface do Databricks**
1. Navegue até **Data** → **DBFS** → **FileStore** → **libraries**
2. Clique em **Upload** e selecione `data_pipeline_agent_lib-3.0.0-py3-none-any.whl`
3. Aguarde a confirmação do upload

**Opção B: CLI do Databricks**
```bash
databricks fs cp \
  dist/data_pipeline_agent_lib-3.0.0-py3-none-any.whl \
  dbfs:/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
```

### Passo 2: Instalação no Cluster

**Opção A: Interface do Cluster**
1. Navegue até **Compute** → Selecione o cluster
2. Clique na aba **Libraries** → **Install new**
3. Selecione **DBFS/ADLS** → **Python Whl**
4. Caminho: `dbfs:/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl`
5. Clique em **Install** e aguarde o checkmark verde

**Opção B: Notebook**
```python
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
dbutils.library.restartPython()
```

### Passo 3: Verificar Instalação

```python
import data_pipeline_agent_lib
from data_pipeline_agent_lib.specialists import ALL_DPL_TOOLS

print(f"DPL Agent v{data_pipeline_agent_lib.__version__}")
print(f"{len(ALL_DPL_TOOLS)} ferramentas especialistas disponíveis")
```

---

## Configuração de Chave API

### Databricks (Recomendado)

**Criar Secret Scope**:
```bash
databricks secrets create-scope --scope hdl-agent-secrets
```

**Adicionar Chave API**:
```bash
databricks secrets put-secret \
  --scope hdl-agent-secrets \
  --key anthropic-api-key \
  --string-value "sk-ant-api03-sua-chave-aqui"
```

**Usar no Notebook**:
```python
import os

api_key = dbutils.secrets.get(
    scope="hdl-agent-secrets",
    key="anthropic-api-key"
)
os.environ["ANTHROPIC_API_KEY"] = api_key
```

### Desenvolvimento Local

**Criar arquivo `.env`**:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-sua-chave-aqui
OPENAI_API_KEY=sk-sua-chave-openai-opcional
LOG_LEVEL=INFO
```

**Carregar no Python**:
```python
from dotenv import load_dotenv
import os

load_dotenv()
print(f"Chave API configurada: {'ANTHROPIC_API_KEY' in os.environ}")
```

---

## Instalação Local

### Instalar a partir do Wheel

```bash
pip install dist/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
python -c "import data_pipeline_agent_lib; print(data_pipeline_agent_lib.__version__)"
```

### Configuração para Desenvolvimento

```bash
# Clonar repositório
git clone [url-do-repositorio]
cd data_pipeline_agent

# Criar ambiente virtual
python3.9 -m venv venv
source venv/bin/activate

# Instalar em modo editável
pip install -e .
pip install -r requirements-dev.txt
```

---

## Verificação

```python
# Testar imports
from data_pipeline_agent_lib.specialists import (
    troubleshoot_hdl_error,
    resolve_hdl_bug,
    optimize_hdl_pipeline
)

# Testar especialista (não requer API)
result = troubleshoot_hdl_error("Mensagem de erro de teste")
print("Instalação bem-sucedida!")
print(f"Saída de exemplo: {result[:100]}...")
```

---

## Solução de Problemas

### ModuleNotFoundError
```python
# Reiniciar kernel
dbutils.library.restartPython()

# Verificar instalação
%pip list | grep hdl-agent

# Reinstalar se necessário
%pip install --force-reinstall /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl
```

### Conflitos de Dependências
```python
# Instalar com flag no-deps
%pip install --no-deps /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl

# Instalar dependências críticas manualmente
%pip install langchain langgraph pydantic

# Reiniciar
dbutils.library.restartPython()
```

### Caminho DBFS Não Encontrado
```bash
# Verificar se o arquivo existe
databricks fs ls dbfs:/FileStore/libraries/

# Re-upload se necessário
databricks fs cp dist/data_pipeline_agent_lib-3.0.0-py3-none-any.whl dbfs:/FileStore/libraries/
```

### Problemas com Chave API
```python
# Verificar se o secret existe
key = dbutils.secrets.get("hdl-agent-secrets", "anthropic-api-key")
print(f"Secret recuperado (tamanho: {len(key)})")

# Verificar variável de ambiente
import os
print(f"Variável de ambiente configurada: {'ANTHROPIC_API_KEY' in os.environ}")
```

---

## Upgrade da v2.0

```python
# Desinstalar versão antiga
%pip uninstall -y hdl-agent-lib

# Instalar nova versão
%pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl

# Reiniciar e verificar
dbutils.library.restartPython()
```

**Mudanças que Quebram Compatibilidade**:
- Nova estrutura Clean Architecture
- Mudanças nas assinaturas de API dos especialistas
- Orquestração LangGraph substitui chains simples

---

## Próximos Passos

1. [Guia de Início Rápido](../deployment/quickstart.md)
2. [Referência de Configuração](configuration.md)
3. [Visão Geral dos Especialistas](../specialists/overview.md)
4. [Exemplos de Código](../examples/basic.md)

---

**Última Atualização**: 2025-10-04
