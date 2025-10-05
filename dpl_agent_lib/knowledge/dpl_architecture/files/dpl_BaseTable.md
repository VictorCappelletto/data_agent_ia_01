# 🌊 BaseTable - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `tables` (DPL)
- **Categoria DPL**: **DPL_CORE**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 41
- **Tamanho**: 1422 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **bronze** (3x - medium)
- **silver** (3x - medium)
- **harmonized** (3x - medium)
- **spark** (2x - low)
- **table** (1x - low)

## 🔧 Métodos (5)

 1. **get_partition_by_layer**
    - Assinatura: `def get_partition_by_layer(self, layer)`

 2. **set_is_current**
    - Assinatura: `def set_is_current(self, df, partitionby_field="_id", orderby_field="updatedAt")`

 3. **bronze_transformations**
    - Assinatura: `def bronze_transformations(self)`

 4. **silver_transformations**
    - Assinatura: `def silver_transformations(self, df)`

 5. **harmonized_transformations**
    - Assinatura: `def harmonized_transformations(self, df)`


## 🥉 Operações Bronze Layer (4)

- **PARTITION_COLUMNS**
- **transformations**
- **PARTITION_COLUMNS**
- **transformations**

## 🏗️ Classes (1)

- **BaseTable**

## 📦 Imports e Dependências (3)

- `from pyspark.sql import functions as F`
- `from pyspark.sql import Window`
- `import base64`

## 🔗 Dependências DPL

- **Spark Features**: sql
- **Delta Lake**: ❌
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ✅
- **Silver Layer**: ✅
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:51:53.031501*
