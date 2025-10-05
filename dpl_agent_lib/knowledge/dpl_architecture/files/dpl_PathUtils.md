# 🌊 PathUtils - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `utils` (DPL)
- **Categoria DPL**: **UTILITIES**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 71
- **Tamanho**: 2953 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **Platform** (4x - medium)
- **table** (4x - medium)
- **silver** (3x - medium)
- **checkpoint** (3x - medium)
- **bronze** (2x - low)
- **visits** (2x - low)
- **tasks** (2x - low)
- **ontap** (2x - low)
- **delta** (2x - low)
- **harmonized** (1x - low)

## 🔧 Métodos (5)

 1. **__init__**
    - Assinatura: `def __init__(self, entity: str, environment: str)`
    - Doc: Initialize the PathUtils instance with entity and environment....

 2. **_get_storage_account**
    - Assinatura: `def _get_storage_account(self, layer: str)`
    - Doc: Retrieve the storage account for a given layer....

 3. **get_location**
    - Assinatura: `def get_location(self, layer, path_type, source, database)`
    - Doc: Get the specified location (schema, checkpoint, or CDC source) for a given layer....

 4. **_get_url_container**
    - Assinatura: `def _get_url_container(self, layer: str)`
    - Doc: Generate the URL for the container based on the layer....

 5. **get_delta_location_path**
    - Assinatura: `def get_delta_location_path(self, layer: str)`
    - Doc: Get the Delta location path for a given layer....


## 🏗️ Classes (1)

- **PathUtils**
  - A utility class for managing paths in a data storage environment, tailored for different layers and ...

## 🔗 Dependências DPL

- **Spark Features**: 
- **Delta Lake**: ✅
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ✅
- **Silver Layer**: ✅
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:52:16.583567*
