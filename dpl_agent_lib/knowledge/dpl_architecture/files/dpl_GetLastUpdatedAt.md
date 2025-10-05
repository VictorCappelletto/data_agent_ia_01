# 🌊 GetLastUpdatedAt - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `monitoring` (DPL)
- **Categoria DPL**: **DPL_CORE**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 136
- **Tamanho**: 4905 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **table** (18x - high)
- **hdl** (12x - high)
- **Platform** (6x - high)
- **spark** (4x - medium)
- **delta** (3x - medium)
- **bronze** (1x - low)
- **silver** (1x - low)
- **harmonized** (1x - low)

## 🔧 Métodos (2)

 1. **get_catalog**
    - Assinatura: `def get_catalog()`

 2. **get_last_updated_at_document_store**
    - Assinatura: `def get_last_updated_at_document_store(country, con_string, database, vendor_id)`


## 🥉 Operações Bronze Layer (2)

- **Platform**
- **vendor**

## 📦 Imports e Dependências (4)

- `from pyspark.sql.functions import udf, lit, col, when, regexp_replace, round as f_round, unix_timestamp, to_timestamp`
- `from pyspark.sql.types import IntegerType, StringType`
- `import json`
- `from pymongo import MongoClient`

## 🔗 Dependências DPL

- **Spark Features**: sql
- **Delta Lake**: ✅
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ✅
- **Silver Layer**: ✅
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:51:58.000185*
