# 🌊 IngestionBase - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `ingestion` (DPL)
- **Categoria DPL**: **DPL_CORE**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 374
- **Tamanho**: 12632 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **table** (73x - high)
- **silver** (31x - high)
- **harmonized** (22x - high)
- **bronze** (18x - high)
- **delta** (18x - high)
- **spark** (14x - high)
- **merge** (14x - high)
- **factory** (10x - high)
- **Platform** (5x - medium)
- **trigger** (5x - medium)

## 🔧 Métodos (4)

 1. **__init__**
    - Assinatura: `def __init__(self, configs: dict = {})`

 2. **completeness_workflow_trigger**
    - Assinatura: `def completeness_workflow_trigger(self)`

 3. **bronze_to_silver**
    - Assinatura: `def bronze_to_silver(self)`

 4. **silver_to_harmonized**
    - Assinatura: `def silver_to_harmonized(self)`


## 🥉 Operações Bronze Layer (28)

- **to_silver**
- **table**
- **table**
- **table**
- **table**
- **table**
- **table**
- **table**
- **table**
- **table**

## 🏗️ Classes (1)

- **IngestionBase**

## 📦 Imports e Dependências (8)

- `from pyspark.sql.types import BinaryType`
- `from datetime import datetime`
- `import uuid`
- `import pytz`
- `from pyspark.sql.functions import (`
- `from pyspark.sql.window import Window`
- `from pyspark.sql.types import ArrayType, StringType`
- `from pyspark.sql.functions import from_json`

## 🔗 Dependências DPL

- **Spark Features**: sql
- **Delta Lake**: ✅
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ✅
- **Silver Layer**: ✅
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:52:06.168605*
