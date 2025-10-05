# 🌊 DataframeUtils - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `utils` (DPL)
- **Categoria DPL**: **UTILITIES**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 186
- **Tamanho**: 7718 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **bronze** (3x - medium)
- **spark** (3x - medium)
- **dataframe** (2x - low)
- **table** (2x - low)
- **Platform** (1x - low)

## 🔧 Métodos (11)

 1. **convert_columns_to_string**
    - Assinatura: `def convert_columns_to_string(df)`

 2. **udf_to_uuid_cast**
    - Assinatura: `def udf_to_uuid_cast(binary_value)`

 3. **process_array_struct_row**
    - Assinatura: `def process_array_struct_row(row, column_name)`

 4. **process_array_struct_column_with_rdd**
    - Assinatura: `def process_array_struct_column_with_rdd(df, column_name)`

 5. **modify_schema**
    - Assinatura: `def modify_schema(schema, column_name)`

 6. **to_uuid_cast**
    - Assinatura: `def to_uuid_cast(df)`

 7. **estimated_rows_processed**
    - Assinatura: `def estimated_rows_processed(df)`

 8. **replace_binary_with_string**
    - Assinatura: `def replace_binary_with_string(data_type: DataType)`
    - Doc: Recursively traverses the schema and replaces BinaryType fields with StringType....

 9. **Platform_schema**
    - Assinatura: `def Platform_schema(bronze_table, col_schema)`
    - Doc: Receives a column schema and applies the appropriate transformations to the DataFrame column, including converting BinaryType fields to StringType wit...

10. **add_traceability_columns**
    - Assinatura: `def add_traceability_columns(df)`
    - Doc: Add traceability columns to the dataframe...

11. **cast_column_to_string**
    - Assinatura: `def cast_column_to_string(df_ldz)`


## 🥉 Operações Bronze Layer (2)

- **table**
- **table**

## 📦 Imports e Dependências (4)

- `import uuid`
- `from pyspark.sql import Row`
- `from pyspark.sql.functions import (`
- `from pyspark.sql.types import (`

## 🔗 Dependências DPL

- **Spark Features**: sql
- **Delta Lake**: ❌
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ✅
- **Silver Layer**: ❌
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:52:19.713958*
