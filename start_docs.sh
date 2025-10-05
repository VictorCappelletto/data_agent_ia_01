#!/bin/bash
#
# start_docs.sh - MkDocs Documentation Server
#
# Purpose: Start MkDocs server for DPL Agent documentation
# Usage: ./start_docs.sh
# Access: http://127.0.0.1:8000
#

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "=================================="
echo "DPL Agent - DataHub Documentation"
echo "=================================="
echo ""

# Change to project directory
cd "$SCRIPT_DIR"

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "✓ venv activated"
else
    echo "WARNING: venv not found, using global Python"
fi

echo ""
echo "Starting MkDocs server..."
echo "Server: http://127.0.0.1:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""
echo "=================================="
echo ""

# Start server
mkdocs serve

