# 🌊 extract_users_hdl - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `process` (DPL)
- **Categoria DPL**: **DPL_CORE**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 273
- **Tamanho**: 9398 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **Platform** (15x - high)
- **table** (8x - high)
- **spark** (7x - high)
- **dataframe** (4x - medium)
- **silver** (2x - low)
- **harmonized** (2x - low)
- **hdl** (1x - low)
- **delta** (1x - low)
- **merge** (1x - low)

## 🔧 Métodos (8)

 1. **_get_region**
    - Assinatura: `def _get_region()`

 2. **_get_env**
    - Assinatura: `def _get_env()`

 3. **generate_random_numbers**
    - Assinatura: `def generate_random_numbers(length)`

 4. **generate_random_letters_and_numbers**
    - Assinatura: `def generate_random_letters_and_numbers(length)`

 5. **gedenrate_requestTraceId**
    - Assinatura: `def gedenrate_requestTraceId()`

 6. **write_sanitized_table**
    - Assinatura: `def write_sanitized_table(df)`

 7. **get_token**
    - Assinatura: `def get_token()`

 8. **run_request**
    - Assinatura: `def run_request(countries, distinct_bdr_id, requestTraceId)`


## 📦 Imports e Dependências (8)

- `from pyspark.sql.functions import *`
- `from pyspark.sql import functions as F`
- `from urllib.parse import urlencode`
- `from pyspark.sql.types import StringType, StructType, StructField`
- `import requests`
- `from datetime import datetime`
- `import random`
- `import string`

## 🔗 Dependências DPL

- **Spark Features**: sql
- **Delta Lake**: ✅
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ❌
- **Silver Layer**: ✅
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:52:04.310364*
