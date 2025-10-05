# 🌊 run_history - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `hdl` (DPL)
- **Categoria DPL**: **DPL_CORE**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 214
- **Tamanho**: 7426 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **table** (18x - high)
- **Platform** (5x - medium)
- **spark** (5x - medium)
- **tasks** (3x - medium)
- **hdl** (2x - low)
- **bronze** (2x - low)
- **delta** (2x - low)
- **stream** (1x - low)
- **dataframe** (1x - low)

## 🔧 Métodos (4)

 1. **get_env_catalog**
    - Assinatura: `def get_env_catalog()`

 2. **generate_date_pairs**
    - Assinatura: `def generate_date_pairs(start_date)`

 3. **get_min_updated_at_document_store**
    - Assinatura: `def get_min_updated_at_document_store(collection_name, con_string, database, vendor_id)`

 4. **run_notebook_in_parallel**
    - Assinatura: `def run_notebook_in_parallel(vendor_info)`


## 🥉 Operações Bronze Layer (2)

- **Platform**
- **Platform**

## 📦 Imports e Dependências (6)

- `from pyspark.sql.functions import udf, lit, col, when, regexp_replace, round as f_round, unix_timestamp, to_timestamp, explode`
- `from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType, LongType, DoubleType, ArrayType, DateType`
- `import json`
- `from pymongo import MongoClient`
- `import datetime`
- `import concurrent.futures`

## 🔗 Dependências DPL

- **Spark Features**: sql
- **Delta Lake**: ✅
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ✅
- **Silver Layer**: ❌
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:52:00.108308*
