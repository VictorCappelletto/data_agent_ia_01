# Requisitos do Projeto & Contexto

Esta página documenta os requisitos originais e o contexto necessário para adaptar este agent para seu ambiente específico.

---

## Visão Geral

Este Data Pipeline Agent foi originalmente desenvolvido para uma **plataforma de dados empresarial real** servindo um sistema de operações B2B em larga escala. O código foi anonimizado para release público, mas a arquitetura e padrões subjacentes são testados em produção.

---

## O Que Foi Anonimizado

Para tornar este projeto publicamente compartilhável, os seguintes elementos foram substituídos por equivalentes genéricos:

### Nomes de Empresa & Produto

| Original (Sistema Real) | Anonimizado (Código Público) | Descrição |
|------------------------|--------------------------|-------------|
| AB InBev | TechCorp Inc | Nome da empresa |
| BEES Platform | DataHub | Nome da plataforma do produto |
| Frontline Strategy | Operations Platform | Área do projeto |
| Force Data Platform | Platform Data Platform | Nome do sistema |

### Nomes de Sistemas Técnicos

| Original | Anonimizado | Propósito |
|----------|------------|---------|
| HDL (High-Level Data) | DPL (Data Pipeline Layer) | Nome da camada de dados principal |
| GHQ_B2B_Delta | enterprise_data_platform | Nome do catálogo de produção |

### Entidades de Dados

| Entidade Original | Anonimizada | Contexto de Negócio |
|----------------|------------|------------------|
| Tasks | Orders | Tarefas de representantes de vendas |
| Visits | Sessions | Registros de visitas a clientes |
| VendorGroups | PartnerGroups | Agrupamentos de fornecedores |
| UserClientCatalog | UserProductCatalog | Catálogo de produtos usuário-cliente |
| ActivityStaging | EventStaging | Área de staging de atividades |
| OnTapUserVisits | UserSessions | Rastreamento de visitas de usuários on-premise |
| OfflineOrders | LocalTransactions | Sincronização de pedidos offline |
| OrdersCartSuggestion | CartRecommendations | Sugestões de carrinho com IA |

### Infraestrutura

| Original | Anonimizado | Notas |
|----------|------------|-------|
| Azure DevOps | GitHub | Hospedagem de repositório |
| Domínios de email internos | example.com | Informações de contato |
| Regiões Azure específicas | Nuvem genérica | Deployments regionais |

---

## O Que Você Precisa Adaptar

Para fazer este agent funcionar em **seu ambiente**, você precisará configurar:

### 1. Ambiente Databricks

**Necessário**:
- Workspace Databricks (AWS, Azure ou GCP)
- Unity Catalog habilitado
- Endpoint Databricks Model Serving para Claude ou LLM similar

**Configuração**:
```python
# No seu notebook ou ambiente Databricks
DATABRICKS_HOST = "https://seu-workspace.cloud.databricks.com"
DATABRICKS_TOKEN = dbutils.secrets.get(scope="seu-scope", key="token")
MODEL_SERVING_ENDPOINT = "seu-endpoint-claude"  # ou GPT-4, Llama, etc.
```

### 2. Arquitetura de Camadas de Dados

O agent espera uma **arquitetura medallion** com estas camadas:

```
Camada Bronze (Dados Brutos)
└── Tabelas streaming de fontes de eventos
└── Tabelas batch de APIs/bancos de dados

Camada Silver (Harmonizada)
└── Dados limpos e validados
└── Regras de negócio aplicadas

Camada Gold (Pronto para Analytics)
└── Métricas agregadas
└── KPIs de negócio
└── Camada de compartilhamento para consumo
```

**Seu Equivalente**:
- Mapear suas camadas de dados para a estrutura esperada
- Atualizar nomes de catálogos nos docs `hdl_agent_lib/knowledge/`
- Modificar nomes de entidades nas ferramentas especialistas

### 3. Entidades de Dados

A base de conhecimento do agent referencia estes tipos de entidade. **Mapeie para suas entidades**:

**Entidades Streaming** (Processamento de eventos em tempo real):
- Eventos de atividade do usuário
- Eventos de transação
- Dados de sensores/IoT
- Logs de aplicação

**Entidades Batch** (Processamento agendado):
- Dados mestre (produtos, clientes, fornecedores)
- Transações históricas
- Dados de referência
- Dados de APIs externas

**Exemplo de Mapeamento**:
```yaml
# Suas entidades → Entidades do agent
seus_pedidos_vendas: Orders
suas_visitas_clientes: Sessions
seus_grupos_fornecedores: PartnerGroups
seu_catalogo_produtos: UserProductCatalog
```

### 4. Padrões de Workflow

O agent entende **Databricks Workflows** com:

**Workflows Streaming**:
- Event Hub / fonte Kafka
- Ingestão Auto Loader
- Pipelines Bronze → Silver
- Gatilhos de chegada de arquivo

**Workflows Batch**:
- Execução CRON agendada
- Fontes MongoDB/CosmosDB
- Pipelines Bronze → Silver → Gold
- Gerenciamento de dependências

**Seu Equivalente**:
- Documentar seus JSONs de workflow em `workflow_hdl/`
- Atualizar nomes e gatilhos de workflow
- Ajustar dependências de tarefas

### 5. Gerenciamento de Secrets

O agent espera secrets em **Databricks Secret Scopes**:

```python
# Padrão default
scope_name = "seu-secret-scope"
api_key = dbutils.secrets.get(scope=scope_name, key="api-key")
db_password = dbutils.secrets.get(scope=scope_name, key="db-password")
```

**Sua Configuração**:
```bash
# Criar secret scope
databricks secrets create-scope --scope seu-secret-scope

# Adicionar secrets
databricks secrets put --scope seu-secret-scope --key api-key
databricks secrets put --scope seu-secret-scope --key db-password
```

### 6. Base de Conhecimento RAG

O agent usa **ChromaDB** para RAG. Você precisa:

1. **Atualizar Base de Conhecimento**:
   - Editar arquivos em `hdl_agent_lib/knowledge/`
   - Substituir workflows genéricos pelos seus workflows reais
   - Documentar suas entidades de dados e pipelines

2. **Carregar Conhecimento**:
   ```bash
   python scripts/load_knowledge_base.py
   ```

3. **Embeddings**:
   - Padrão: embeddings OpenAI (requer chave API)
   - Alternativa: embeddings Databricks, modelos locais, etc.

**Configuração**:
```python
# Opção 1: embeddings OpenAI (padrão)
OPENAI_API_KEY = "sua-chave"

# Opção 2: embeddings Databricks
from databricks_genai import embeddings
embeddings_model = embeddings.get_model("seu-modelo-embedding")

# Opção 3: embeddings locais (sentence-transformers)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
```

---

## Contexto do Mundo Real

### Caso de Uso Original

O agent foi construído para uma **plataforma global de distribuição de bebidas B2B** servindo:
- 50.000+ representantes de vendas
- 1M+ clientes
- 13 pipelines streaming (tempo real)
- 13 pipelines batch (agendados)
- Processando 500GB+ de dados diários

### Problemas Que Resolve

1. **Troubleshooting de Pipeline**: Diagnosticar falhas streaming/batch
2. **Otimização de Performance**: Identificar gargalos, sugerir melhorias
3. **Garantia de Qualidade**: Validar completude de dados, detectar anomalias
4. **Navegação de Ecossistema**: Entender dependências, workflows
5. **Suporte Operacional**: Corrigir bugs, coordenar reprocessamento

### Padrões de Produção

**O Que Funciona**:
- RAG para conhecimento específico de workflow
- Ferramentas especialistas para tarefas focadas
- LangGraph para orquestração complexa
- Clean Architecture para manutenibilidade

**O Que Adaptar**:
- Nomes de entidades e lógica de negócio
- Estruturas de workflow e dependências
- Padrões de erro e alertas
- Pontos de integração e APIs

---

## Exemplo Mínimo Funcional

Para fazer o agent funcionar com **mudanças mínimas**:

### Passo 1: Configuração do Ambiente

```bash
# Clonar e configurar
git clone https://github.com/seu-usuario/data-pipeline-agent
cd data-pipeline-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Passo 2: Configurar Credenciais

```bash
# Criar arquivo .env
cat > .env << EOF
DATABRICKS_HOST=https://seu-workspace.cloud.databricks.com
DATABRICKS_TOKEN=seu-token
MODEL_SERVING_ENDPOINT=seu-endpoint-claude
OPENAI_API_KEY=sua-chave-openai  # Opcional, para embeddings RAG
EOF
```

### Passo 3: Atualizar Base de Conhecimento

```bash
# Editar seus workflows
vim hdl_agent_lib/knowledge/workflows/streaming/seu-pipeline.md
vim hdl_agent_lib/knowledge/workflows/batch/seu-job-batch.md

# Carregar no vector store
python scripts/load_knowledge_base.py
```

### Passo 4: Testar Localmente

```python
# test_local.py
from dpl_agent_lib.specialists import diagnose_pipeline_error

result = diagnose_pipeline_error(
    error_message="Sua mensagem de erro real",
    pipeline_name="nome-do-seu-pipeline",
    context="Contexto adicional sobre a falha"
)

print(result)
```

### Passo 5: Deploy no Databricks

```python
# Upload do pacote wheel
databricks fs cp dist/dpl_agent_lib-3.1.0-py3-none-any.whl dbfs:/FileStore/wheels/

# Instalar no cluster
%pip install /dbfs/FileStore/wheels/dpl_agent_lib-3.1.0-py3-none-any.whl

# Usar no notebook
from dpl_agent_lib.specialists import *
result = diagnose_pipeline_error(...)
```

---

## Guia de Integração Customizada

### Para Seu Ambiente Específico

1. **Clonar o Repositório**
   ```bash
   git clone https://github.com/seu-usuario/data-pipeline-agent
   cd data-pipeline-agent
   ```

2. **Find & Replace Global**
   ```bash
   # Substituir nomes genéricos pelos seus nomes reais
   find . -type f -name "*.py" -exec sed -i 's/DataHub/SuaPlataforma/g' {} +
   find . -type f -name "*.md" -exec sed -i 's/DPL/SuaCamadaDados/g' {} +
   ```

3. **Atualizar Mapeamentos de Entidades**
   ```python
   # Em dpl_agent_lib/domain/entities/
   # Renomear ou estender classes de entidades para corresponder ao seu modelo de dados
   ```

4. **Documentar Seus Workflows**
   ```bash
   # Copiar seus JSONs de workflow
   cp /caminho/para/seus/workflows/*.json workflow_hdl/
   
   # Gerar documentação
   python scripts/generate_workflow_docs.py
   ```

5. **Customizar Especialistas**
   ```python
   # Em dpl_agent_lib/specialists/
   # Ajustar padrões de erro, regras de validação e lógica de negócio
   ```

6. **Reconstruir Pacote**
   ```bash
   python setup.py bdist_wheel
   ```

---

## FAQ

### P: Preciso da mesma estrutura de dados exata?

**R**: Não. O agent é flexível. Apenas atualize os nomes de entidades e base de conhecimento para corresponder à sua estrutura.

### P: Posso usar um LLM diferente?

**R**: Sim. O agent suporta qualquer LLM acessível via Databricks Model Serving ou integrações LangChain (OpenAI, Anthropic, Azure, etc.).

### P: E se eu não usar Databricks?

**R**: As ferramentas especialistas principais funcionam em qualquer lugar. Você precisará adaptar:
- Integração LLM (substituir `databricks_claude.py`)
- Gerenciamento de secrets (substituir `dbutils.secrets`)
- Estratégia de deployment (Docker, Kubernetes, etc.)

### P: Quanto esforço para adaptar?

**R**: Depende da similaridade com o sistema original:
- **Arquitetura similar**: 1-2 dias (atualizar nomes, base de conhecimento)
- **Arquitetura diferente**: 1-2 semanas (reestruturar entidades, workflows)
- **Reescrita completa**: Usar apenas como arquitetura de referência

### P: A anonimização é reversível?

**R**: Não. Todos os detalhes específicos da empresa foram permanentemente removidos. Você configurará SEU ambiente.

---

## Suporte

Para perguntas sobre adaptar isso ao seu ambiente:

1. **GitHub Issues**: Questões técnicas e bugs
2. **GitHub Discussions**: Questões de arquitetura e design
3. **Documentação**: Leia todos os docs na pasta `docs/`

---

## Licença

Este projeto é open-source sob Licença MIT. Você é livre para adaptá-lo para qualquer propósito, comercial ou não-comercial.

---

**Última Atualização**: 5 de Outubro de 2025  
**Versão**: 3.1.0
