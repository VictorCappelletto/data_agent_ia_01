# 🌊 IngestionControl - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `utils` (DPL)
- **Categoria DPL**: **DPL_CORE**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 95
- **Tamanho**: 3702 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **table** (11x - high)
- **stream** (6x - high)
- **spark** (5x - medium)
- **Platform** (2x - low)
- **hdl** (1x - low)
- **bronze** (1x - low)
- **dataframe** (1x - low)
- **delta** (1x - low)

## 🔧 Métodos (4)

 1. **__init__**
    - Assinatura: `def __init__(self, ingestion_id, database, table_base_name, region, source, execution_time_utc, use_datastream, logger, spark_session)`

 2. **__cast_to_bool**
    - Assinatura: `def __cast_to_bool(self, variable)`

 3. **__get_path**
    - Assinatura: `def __get_path(self)`

 4. **save_data**
    - Assinatura: `def save_data(self, layer, country, estimated_rows_processed, time_elapsed_in_seconds, last_updated_at_table=None, error=False, error_message=None)`


## 🥉 Operações Bronze Layer (1)

- **Platform**

## 🏗️ Classes (1)

- **IngestionControl**

## 📦 Imports e Dependências (1)

- `from pyspark.sql.types import (`

## 🔗 Dependências DPL

- **Spark Features**: sql
- **Delta Lake**: ✅
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ✅
- **Silver Layer**: ❌
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:52:15.337584*
