# 🌊 CustomLogger - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `utils` (DPL)
- **Categoria DPL**: **DPL_CORE**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 28
- **Tamanho**: 1058 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **table** (5x - medium)
- **etl** (1x - low)

## 🔧 Métodos (5)

 1. **__init__**
    - Assinatura: `def __init__(self, database, table, slack_integration=False)`

 2. **configure_logger**
    - Assinatura: `def configure_logger(self)`

 3. **info**
    - Assinatura: `def info(self, message)`

 4. **error**
    - Assinatura: `def error(self, message)`

 5. **send_message_to_slack**
    - Assinatura: `def send_message_to_slack(self, message)`


## 🏗️ Classes (1)

- **CustomLogger**

## 📦 Imports e Dependências (2)

- `import logging`
- `from datetime import datetime`

## 🔗 Dependências DPL

- **Spark Features**: 
- **Delta Lake**: ❌
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ❌
- **Silver Layer**: ❌
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:52:17.851256*
