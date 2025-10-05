#!/bin/bash
# DPL Agent v3.0 - Local Development Setup Script
# 
# Purpose: Initial environment setup for local development
# Usage: ./scripts/setup_venv.sh
# Note: Run this ONCE when first setting up the project
#
# What it does:
# - Creates Python virtual environment
# - Installs dependencies (core + dev)
# - Configures pre-commit hooks
# - Creates necessary directories
# - Sets up .env file from template
#

set -e  # Exit on error

echo "DPL Agent v3.0 - Local Development Setup"
echo "(Run this ONCE for initial setup)"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
echo "✓ Virtual environment created"

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"

# Install core dependencies
echo ""
echo "📚 Installing core dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Core dependencies installed"

# Install dev dependencies
echo ""
echo "🛠️  Installing development dependencies..."
pip install -r requirements-dev.txt --quiet
echo "✓ Development dependencies installed"

# Install pre-commit hooks
echo ""
echo "🔗 Installing pre-commit hooks..."
pre-commit install --quiet
echo "✓ Pre-commit hooks installed"

# Setup environment file
echo ""
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please configure your .env file with:"
    echo "   - ANTHROPIC_API_KEY"
    echo "   - OPENAI_API_KEY"
    echo "   - DATABRICKS_TOKEN"
    echo "   - Other required credentials"
else
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo ""
echo "📁 Creating data directories..."
mkdir -p data/chroma_db
mkdir -p logs
mkdir -p cache
echo "✓ Directories created"

# Load knowledge base
echo ""
echo "🧠 Loading DPL knowledge base into vector store..."
if [ -f "scripts/load_knowledge_base.py" ]; then
    python scripts/load_knowledge_base.py
    echo "✓ Knowledge base loaded"
else
    echo "⚠️  Knowledge base loader not found (will be created later)"
fi

# Summary
echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Configure your .env file with API keys"
echo "2. Activate venv: source venv/bin/activate"
echo "3. Run the agent: python run_agent.py"
echo ""
echo "Note: This setup script only needs to run ONCE."
echo "For subsequent sessions, just activate venv."
echo ""
echo "For more information, see README.md"
echo ""

