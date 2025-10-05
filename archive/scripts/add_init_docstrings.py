#!/usr/bin/env python3
"""
Script to add docstrings to empty __init__.py files.

Usage:
    python scripts/add_init_docstrings.py [--dry-run]
"""

import sys
from pathlib import Path
from typing import Dict

# Docstrings for each package
DOCSTRINGS: Dict[str, str] = {
    "configs": '''"""
Configuration module for DPL Agent.

Contains configuration files and settings for the agent.
"""
''',
    "application": '''"""
Application layer for DPL Agent.

Contains use cases and application services that orchestrate domain logic.
Implements the application-specific business rules.
"""
''',
    "application/use_cases": '''"""
Use cases for DPL Agent application layer.

Contains application-specific use case implementations.
"""
''',
    "application/services": '''"""
Application services for DPL Agent.

Contains services that coordinate domain logic for specific application needs.
"""
''',
    "infrastructure": '''"""
Infrastructure layer for DPL Agent.

Contains implementations for external integrations:
- LLM providers (Claude, OpenAI)
- Vector stores (ChromaDB, Qdrant)
- Databricks integration
- MCP (Model Context Protocol)
"""
''',
    "infrastructure/databricks": '''"""
Databricks integration infrastructure.

Contains adapters and implementations for Databricks platform integration.
"""
''',
    "infrastructure/mcp": '''"""
Model Context Protocol (MCP) infrastructure.

Contains implementations for MCP integration and communication.
"""
''',
    "domain/ports": '''"""
Domain layer ports (interfaces) for DPL Agent.

Defines abstract interfaces that the domain layer uses to interact
with external systems, following the Dependency Inversion Principle.
"""
''',
    "domain/services": '''"""
Domain services for DPL Agent.

Contains business logic that doesn't naturally fit within a single entity.
Encapsulates complex domain operations and rules.
"""
''',
    "domain/entities": '''"""
Domain entities for DPL Agent.

Contains core business entities representing DPL concepts:
- DPLTable: Data layer tables
- DPLPipeline: Processing pipelines
- DPLWorkflow: Databricks workflows
- DPLError: Error representations
"""
''',
}

def add_docstring_to_file(file_path: Path, dry_run: bool = False) -> bool:
    """Add docstring to an empty __init__.py file."""
    # Read current content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    if content:
        print(f"⏭️  Skipping {file_path} (not empty)")
        return False
    
    # Find matching docstring
    relative_path = file_path.parent.relative_to(file_path.parent.parent.parent)
    key = str(relative_path).replace('data_pipeline_agent_lib/', '')
    
    docstring = DOCSTRINGS.get(key)
    if not docstring:
        print(f"⚠️  No docstring defined for {key}")
        return False
    
    print(f"✅ Adding docstring to {file_path}")
    print(f"   Key: {key}")
    
    if dry_run:
        print(f"   Docstring preview: {docstring[:60]}...")
        return True
    
    # Write docstring
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(docstring)
    
    return True

def main():
    """Main function."""
    dry_run = '--dry-run' in sys.argv
    
    print("=" * 60)
    print("DPL Agent - __init__.py Docstring Addition")
    print("=" * 60)
    
    if dry_run:
        print("\n🔍 DRY RUN MODE (no files will be modified)")
    
    # Find all empty __init__.py files
    root_path = Path(__file__).parent.parent / "data_pipeline_agent_lib"
    init_files = list(root_path.rglob("__init__.py"))
    
    print(f"\nScanning {len(init_files)} __init__.py files...")
    
    files_modified = 0
    
    for init_file in sorted(init_files):
        if add_docstring_to_file(init_file, dry_run):
            files_modified += 1
    
    print("\n" + "=" * 60)
    print(f"✅ {'Simulation' if dry_run else 'Addition'} complete!")
    print(f"   Files scanned: {len(init_files)}")
    print(f"   Files modified: {files_modified}")
    print("=" * 60)
    
    if dry_run:
        print("\n💡 Run without --dry-run to apply changes")

if __name__ == "__main__":
    main()

