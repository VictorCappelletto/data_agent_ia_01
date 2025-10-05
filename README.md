# Data Pipeline Agent

Um agent AI inteligente especializado em troubleshooting, monitoramento e otimização de operações de pipeline de dados.

## Visão Geral

O Data Pipeline Agent (DPL Agent) é um sistema AI pronto para produção construído com princípios de Clean Architecture, apresentando:

- **7 Ferramentas Especializadas** para operações de pipeline
- **Sistema RAG** com busca semântica sobre 66 documentos da base de conhecimento
- **Orquestração LangGraph** para workflows multi-agent com estado
- **Arquitetura Limpa** com clara separação de responsabilidades
- **136 Testes Unitários** com 51% de cobertura de código
- **Deploy em Produção** pronto para clusters Databricks

## Funcionalidades

### Capacidades Principais

1. **Troubleshooting**: Diagnosticar erros e problemas de pipeline
2. **Resolução de Bugs**: Fornecer correções passo a passo para problemas comuns
3. **Otimização de Performance**: Analisar e melhorar eficiência de pipeline
4. **Garantia de Qualidade**: Validar qualidade e completude de dados
5. **Execução de Workflow**: Monitorar e controlar workflows de pipeline
6. **Documentação**: Acessar documentação de componentes e melhores práticas
7. **Coordenação**: Gerenciar reprocessamento e recuperação de dados

### Sistema RAG (Retrieval-Augmented Generation)

O DPL Agent utiliza **RAG** para fornecer respostas fundamentadas em documentação real:

- 🔍 **Retrieval**: Busca semântica com embeddings vetoriais (Sentence Transformers)
- 🧠 **Augmentation**: Injeta contexto recuperado no prompt do LLM
- ✨ **Generation**: LLM gera respostas baseadas na documentação DPL específica

**Benefícios**:
- ✅ Respostas específicas do DPL (não genéricas)
- ✅ Fundamentadas em documentação real com citações
- ✅ Reduz "alucinações" do LLM
- ✅ Conhecimento atualizado sem retreinar modelo

### Stack Técnico

- **LangChain/LangGraph**: Orquestração de agent e integração de ferramentas
- **RAG System**: ChromaDB + Sentence Transformers (all-MiniLM-L6-v2, 384D)
- **Claude (Anthropic)**: LLM para compreensão de linguagem natural
- **Pydantic**: Validação e serialização de dados
- **pytest**: Framework de testes abrangente
- **MkDocs**: Documentação profissional

## Início Rápido

### Instalação

```bash
# Clonar o repositório
git clone https://github.com/VictorCappelletto/data_agent_ia_01.git
cd data_agent_ia_01

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### Uso Básico

```python
from dpl_agent_lib.agent import create_agent

# Inicializar o agent
agent = create_agent()

# Fazer uma pergunta
response = agent.invoke({
    "messages": [{"role": "user", "content": "Por que o pipeline Orders está falhando?"}]
})

print(response["messages"][-1]["content"])
```

### Executar Chat Interativo

```bash
python run_agent.py
```

## Arquitetura

### Camadas de Arquitetura Limpa

```
dpl_agent_lib/
├── domain/              # Entidades e regras de negócio
│   ├── entities/        # Objetos de domínio principais
│   ├── value_objects.py # Tipos de valor imutáveis
│   └── ports/           # Definições de interface
├── application/         # Casos de uso e orquestração
│   └── services/        # Serviços de aplicação (RAG, etc.)
├── infrastructure/      # Integrações externas
│   ├── llm/             # Provedores LLM (Claude, Databricks)
│   └── vector_store/    # Integração de banco de dados vetorial
└── specialists/         # 7 ferramentas especializadas
```

### Fluxo de Dados

1. **Consulta do Usuário** → Agent recebe pergunta em linguagem natural
2. **Análise de Intenção** → LangGraph determina quais especialistas invocar
3. **Recuperação RAG** → Busca semântica encontra documentação relevante
4. **Execução de Ferramenta** → Especialistas executam com contexto aprimorado
5. **Geração de Resposta** → Resposta estruturada com fontes

## Especialistas

### 1. Troubleshooter
Diagnostica erros e fornece análise de causa raiz.

```python
from dpl_agent_lib.specialists import troubleshoot_pipeline_error

result = troubleshoot_pipeline_error(
    error_message="Timeout de conexão ao banco de dados",
    pipeline_name="orders-ingestion"
)
```

### 2. Bug Resolver
Fornece soluções passo a passo para problemas conhecidos.

### 3. Performance Advisor
Analisa performance de pipeline e sugere otimizações.

### 4. Quality Assistant
Valida qualidade de dados e identifica anomalias.

### 5. Pipeline Commander
Monitora e controla execuções de workflow.

### 6. Ecosystem Assistant
Fornece documentação e melhores práticas.

### 7. Pipeline Coordinator
Gerencia operações de reprocessamento e recuperação de dados.

## Configuração

### Variáveis de Ambiente

```bash
# Necessário para desenvolvimento local
export ANTHROPIC_API_KEY="sua-chave-api-aqui"

# Opcional: Configuração customizada
export DPL_ENVIRONMENT="production"
export VECTOR_STORE_PATH="./chroma_db"
```

### Deploy no Databricks

O agent integra nativamente com Databricks Serving Endpoints para uso em produção:

```python
from dpl_agent_lib.infrastructure.llm import get_databricks_claude

# Usa serving LLM nativo do Databricks
llm = get_databricks_claude(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    max_tokens=4096
)
```

Veja `databricks_examples/` para notebooks completos.

## Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=dpl_agent_lib --cov-report=html

# Executar apenas testes unitários
pytest tests/unit/

# Executar testes E2E
pytest tests/e2e/ -v
```

## Documentação

Documentação completa está disponível em `docs/` e pode ser servida localmente:

```bash
/Users/victorcappelleto/Library/Python/3.9/bin/mkdocs serve
# Abrir navegador em http://127.0.0.1:8000
```

Ou use o script auxiliar:

```bash
./start_docs.sh
```

**Documentação Online**: https://victorcappelletto.github.io/data_agent_ia_01/

## Desenvolvimento

### Configurar Ambiente de Desenvolvimento

```bash
# Instalar dependências de dev
pip install -r requirements-dev.txt

# Instalar hooks pre-commit
pre-commit install

# Executar verificações de qualidade de código
pre-commit run --all-files
```

### Estrutura do Projeto

- `dpl_agent_lib/` - Pacote Python principal
- `docs/` - Documentação MkDocs
- `tests/` - Testes unitários, integração e E2E
- `examples/` - Exemplos de uso
- `databricks_examples/` - Notebooks de deploy Databricks
- `workflow_hdl/` - Configurações de workflow de exemplo

## Deploy

### Construir Pacote Wheel

```bash
python setup.py bdist_wheel
```

O arquivo `.whl` será criado em `dist/` e pode ser instalado em clusters Databricks:

```python
# Em notebook Databricks
%pip install /path/to/data_pipeline_agent_lib-3.1.0-py3-none-any.whl
```

### Checklist de Produção

- [ ] Definir variáveis de ambiente de produção
- [ ] Configurar serving endpoints do Databricks
- [ ] Carregar base de conhecimento no vector store
- [ ] Executar suite completa de testes
- [ ] Deploy do pacote wheel no cluster
- [ ] Monitorar respostas iniciais do agent

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça fork do repositório
2. Crie uma branch de feature (`git checkout -b feature/funcionalidade-incrivel`)
3. Commit suas mudanças (`git commit -m 'Adicionar funcionalidade incrível'`)
4. Push para a branch (`git push origin feature/funcionalidade-incrivel`)
5. Abra um Pull Request

### Padrões de Código

- Use type hints para todas as funções
- Adicione docstrings seguindo estilo Google
- Escreva testes unitários para novas funcionalidades
- Execute hooks pre-commit antes de commitar
- Siga princípios de Clean Architecture
- Use logging profissional (sem declarações print)

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Agradecimentos

Construído com:
- [LangChain](https://github.com/langchain-ai/langchain) - Framework de aplicação LLM
- [LangGraph](https://github.com/langchain-ai/langgraph) - Orquestração de agent com estado
- [Anthropic Claude](https://www.anthropic.com/) - Modelo de linguagem grande
- [ChromaDB](https://www.trychroma.com/) - Banco de dados vetorial
- [MkDocs](https://www.mkdocs.org/) - Gerador de documentação

## Suporte

Para problemas, questões ou contribuições:
- Abra uma issue no GitHub
- Verifique a documentação em `/docs` ou online
- Revise exemplos em `/examples`

---

**Versão**: 3.1.0  
**Status**: Pronto para Produção  
**Última Atualização**: 2025-10-05
