# 🌊 RunUtils - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `utils` (DPL)
- **Categoria DPL**: **UTILITIES**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 213
- **Tamanho**: 8462 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **table** (19x - high)
- **Platform** (5x - medium)
- **spark** (4x - medium)
- **hdl** (2x - low)
- **bronze** (2x - low)
- **delta** (2x - low)
- **stream** (1x - low)

## 🔧 Métodos (6)

 1. **get_env_catalog**
    - Assinatura: `def get_env_catalog(self)`

 2. **generate_date_pairs**
    - Assinatura: `def generate_date_pairs(start_date)`

 3. **get_min_updated_at_document_store**
    - Assinatura: `def get_min_updated_at_document_store(collection_name, con_string, database, vendor_id)`

 4. **prepare_data**
    - Assinatura: `def prepare_data(self)`

 5. **run_notebook_in_parallel**
    - Assinatura: `def run_notebook_in_parallel(self, vendor_info)`

 6. **execute**
    - Assinatura: `def execute(self)`


## 🥉 Operações Bronze Layer (2)

- **Platform**
- **Platform**

## 🏗️ Classes (1)

- **CosmosDBIngestion**

## 📦 Imports e Dependências (5)

- `from pyspark.sql.functions import udf, lit, col, when, regexp_replace, explode`
- `from pyspark.sql.types import StructType, StructField, StringType, DateType, ArrayType`
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
*DPL Knowledge gerado automaticamente em 2025-09-24T21:52:17.163427*
