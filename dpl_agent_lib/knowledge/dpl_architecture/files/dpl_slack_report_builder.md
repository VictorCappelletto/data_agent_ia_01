# 🌊 slack_report_builder - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `utils` (DPL)
- **Categoria DPL**: **DPL_CORE**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 78
- **Tamanho**: 2759 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **table** (12x - high)
- **Platform** (2x - low)
- **spark** (2x - low)
- **hdl** (1x - low)
- **etl** (1x - low)
- **dataframe** (1x - low)

## 🔧 Métodos (6)

 1. **__init__**
    - Assinatura: `def __init__(self, table_name, df)`

 2. **__default_message**
    - Assinatura: `def __default_message(self)`

 3. **__alert_last_updated**
    - Assinatura: `def __alert_last_updated(self)`

 4. **__send_message**
    - Assinatura: `def __send_message(self, message)`

 5. **__build_soap**
    - Assinatura: `def __build_soap(self, message)`

 6. **send_message_to_slack**
    - Assinatura: `def send_message_to_slack(self, alert_type=None)`


## 🏗️ Classes (1)

- **SlackReportBuilder**
  - Class model used to make reports and send it to slack channel...

## 📦 Imports e Dependências (3)

- `import requests`
- `import json`
- `import pandas as pd`

## 🔗 Dependências DPL

- **Spark Features**: 
- **Delta Lake**: ❌
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ❌
- **Silver Layer**: ❌
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:52:21.047012*
