#!/bin/bash
# Script para fazer deploy da documentação atualizada para GitHub Pages

set -e  # Exit on error

echo "=========================================="
echo "Deploy da Documentação para GitHub Pages"
echo "=========================================="
echo ""

# Check if mkdocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo "❌ MkDocs não está instalado."
    echo ""
    echo "Instale com:"
    echo "  pip install mkdocs mkdocs-material mkdocstrings[python]"
    echo ""
    exit 1
fi

echo "✅ MkDocs encontrado"
echo ""

# Check if in git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Não está em um repositório Git"
    exit 1
fi

echo "✅ Repositório Git encontrado"
echo ""

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "⚠️  Você tem mudanças não commitadas:"
    git status -s
    echo ""
    read -p "Deseja continuar com o deploy? (s/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Deploy cancelado."
        exit 1
    fi
fi

echo "📦 Buildando documentação localmente..."
mkdocs build --clean

if [ $? -ne 0 ]; then
    echo "❌ Erro no build da documentação"
    exit 1
fi

echo "✅ Build local concluído"
echo ""

echo "🚀 Fazendo deploy para GitHub Pages..."
mkdocs gh-deploy --clean

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Deploy concluído com sucesso!"
    echo "=========================================="
    echo ""
    echo "Seu site estará disponível em alguns minutos em:"
    echo "https://victorcappelletto.github.io/data_agent_ia_01/"
    echo ""
    echo "Navegue para:"
    echo "  - https://victorcappelletto.github.io/data_agent_ia_01/#sistema-rag"
    echo "  - https://victorcappelletto.github.io/data_agent_ia_01/architecture/clean-architecture/"
    echo "  - https://victorcappelletto.github.io/data_agent_ia_01/architecture/rag-explained/"
    echo ""
else
    echo ""
    echo "❌ Erro no deploy"
    exit 1
fi

