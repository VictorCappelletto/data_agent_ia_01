# 🌊 PostgressConector - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `utils` (DPL)
- **Categoria DPL**: **DPL_CORE**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 63
- **Tamanho**: 2164 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **batch** (13x - high)
- **table** (4x - medium)
- **silver** (2x - low)
- **Platform** (2x - low)
- **spark** (2x - low)
- **delta** (1x - low)

## 🔧 Métodos (2)

 1. **read_batch**
    - Assinatura: `def read_batch(host, db, user, password, entity, batch_size, schema=None)`

 2. **get_row_count**
    - Assinatura: `def get_row_count(host, db, user, password, entity, schema=None)`


## 🏗️ Classes (1)

- **PostgresConnector**
  - This class makes the connection with the postgres database  @staticmethod def read_batch(host, db, u...

## 🔗 Dependências DPL

- **Spark Features**: 
- **Delta Lake**: ✅
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ❌
- **Silver Layer**: ✅
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:52:14.768093*
