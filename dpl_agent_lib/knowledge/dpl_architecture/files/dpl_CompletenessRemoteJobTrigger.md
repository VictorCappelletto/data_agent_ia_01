# 🌊 CompletenessRemoteJobTrigger - DPL Knowledge Base

## 🏷️ Metadata
- **Pasta**: `utils` (DPL)
- **Categoria DPL**: **DPL_CORE**
- **Tipo**: NOTEBOOK
- **Linguagem**: PYTHON
- **Linhas**: 453
- **Tamanho**: 15287 caracteres

## 🔤 Palavras-Chave DPL (Semantic Index)
- **table** (57x - high)
- **trigger** (42x - high)
- **stream** (2x - low)
- **etl** (2x - low)
- **ucc** (1x - low)

## 🔧 Métodos (26)

 1. **__init__**
    - Assinatura: `def __init__(self, dbutils)`
    - Doc: Initialize the DatabricksRuntimeInfo instance.  :param dbutils: The Databricks utilities object used to retrieve execution context and parameters....

 2. **get_param_or_return_null**
    - Assinatura: `def get_param_or_return_null(func)`
    - Doc: Decorator to catch exceptions and return None if an exception occurs.  This decorator is used to wrap methods that retrieve execution context paramete...

 3. **wrapper**
    - Assinatura: `def wrapper(*args, **kwargs)`

 4. **__set_execution_context**
    - Assinatura: `def __set_execution_context(self, dbutils)`

 5. **__set_execution_parameters**
    - Assinatura: `def __set_execution_parameters(self, dbutils)`

 6. **workspace_id**
    - Assinatura: `def workspace_id(self)`

 7. **workspace_url**
    - Assinatura: `def workspace_url(self)`

 8. **job_group**
    - Assinatura: `def job_group(self)`

 9. **cluster_id**
    - Assinatura: `def cluster_id(self)`

10. **notebook_path**
    - Assinatura: `def notebook_path(self)`

11. **root_run_id**
    - Assinatura: `def root_run_id(self)`

12. **current_run_id**
    - Assinatura: `def current_run_id(self)`

13. **job_id**
    - Assinatura: `def job_id(self)`

14. **create_internal_logger**
    - Assinatura: `def create_internal_logger(self)`
    - Doc: Create and configure the internal logger....

15. **databricks_instance**
    - Assinatura: `def databricks_instance(self, url: str)`
    - Doc: Validate and format the Databricks instance URL.  Args: url (str): The URL of the Databricks instance.  Returns: str: The formatted and validated URL....

16. **trigger_job**
    - Assinatura: `def trigger_job(self, job_id: str, job_params: dict = None)`
    - Doc: Trigger a job to run immediately in the Databricks workspace.  Args: job_id (str): The ID of the job to be triggered. job_params (dict, optional): Par...

17. **_validate_and_set_environment**
    - Assinatura: `def _validate_and_set_environment(self, environment: str)`
    - Doc: Validate and set the environment.  Args: environment (str): The environment to validate and set.  Returns: str: The validated environment....

18. **_job_id_by_env**
    - Assinatura: `def _job_id_by_env(self)`
    - Doc: Get job IDs for each environment.  Returns: dict: Mapping of environment names to job IDs...

19. **_create_internal_logger**
    - Assinatura: `def _create_internal_logger(self)`
    - Doc: Create and configure the internal logger....

20. **_databricks_instance_by_env**
    - Assinatura: `def _databricks_instance_by_env(self)`
    - Doc: Get Databricks instance URLs for each environment.  Returns: dict: Mapping of environment names to Databricks instance URLs...

21. **_set_databricks_workspace**
    - Assinatura: `def _set_databricks_workspace(self)`
    - Doc: Initialize the Databricks workspace connection.  Raises: Exception: If workspace connection fails...

22. **_check_if_table_should_trigger_regex**
    - Assinatura: `def _check_if_table_should_trigger_regex(self, table_name: str)`
    - Doc: Check if the given table should trigger a completeness workflow.  Args: table_name (str): Name of the table to check  Returns: bool: True if the table...

23. **_check_if_table_should_trigger_list**
    - Assinatura: `def _check_if_table_should_trigger_list(self, table_name: str)`
    - Doc: Check if the given table should trigger a completeness workflow.  Args: table_name (str): Name of the table to check  Returns: bool: True if the table...

24. **_trigger**
    - Assinatura: `def _trigger()`
    - Doc: Trigger the completeness workflow for the specified table....

25. **_decorator**
    - Assinatura: `def _decorator(f)`

26. **wrapper**
    - Assinatura: `def wrapper(*args, **kwargs)`
    - Doc: Wrapper that executes the decorated function and triggers completeness workflow....


## 🏗️ Classes (3)

- **DatabricksRuntimeInfo**
  - A class to encapsulate the runtime information of a Databricks notebook.  This class retrieves vario...
- **DatabricksWorkspace**
  - This class has the objective of make easier to interact with databricks account API....
- **CompletenessRemoteJobTrigger**
  - A class to trigger remote completeness workflow jobs in Databricks.  This class handles the authenti...

## 📦 Imports e Dependências (4)

- `from functools import wraps`
- `import logging`
- `import re`
- `import requests`

## 🔗 Dependências DPL

- **Spark Features**: 
- **Delta Lake**: ❌
- **Streaming**: ❌
- **Event Hub**: ❌
- **Bronze Layer**: ❌
- **Silver Layer**: ❌
- **DPL Utils**: ❌

---
*DPL Knowledge gerado automaticamente em 2025-09-24T21:52:15.945645*
