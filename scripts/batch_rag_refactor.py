"""
Batch RAG Refactor Script

Applies RAG integration pattern to remaining 4 specialists.
"""

import os
from pathlib import Path

# RAG integration template
RAG_IMPORT = """from ..application.services import get_hdl_retriever_service"""

RAG_CLASS_INIT = """
    # RAG service (lazy-loaded)
    _rag_service = None
    
    @classmethod
    def _get_rag_service(cls):
        \"\"\"Lazy initialization of RAG service.\"\"\"
        if cls._rag_service is None:
            try:
                cls._rag_service = get_hdl_retriever_service()
                logger.debug("RAG service initialized for {}")
            except Exception as e:
                logger.warning("RAG service initialization failed", error=str(e))
                cls._rag_service = None
        return cls._rag_service
"""

def add_rag_imports(file_path: Path, class_name: str):
    """Add RAG import to file."""
    content = file_path.read_text()
    
    if "get_hdl_retriever_service" in content:
        print(f"  ✅ {file_path.name} - RAG import already present")
        return
    
    # Add import after existing imports
    import_line = "from ..utils import get_logger"
    if import_line in content:
        content = content.replace(
            import_line,
            f"{import_line}\n{RAG_IMPORT}"
        )
    
    # Add class-level RAG initialization
    class_def_pattern = f"class {class_name}:"
    if class_def_pattern in content:
        # Find the position after class docstring
        class_pos = content.find(class_def_pattern)
        next_triple_quote = content.find('"""', class_pos + len(class_def_pattern))
        if next_triple_quote > 0:
            next_triple_quote = content.find('"""', next_triple_quote + 3)
            insertion_pos = next_triple_quote + 3
            rag_init = RAG_CLASS_INIT.format(class_name)
            content = content[:insertion_pos] + rag_init + content[insertion_pos:]
    
    file_path.write_text(content)
    print(f"  ✅ {file_path.name} - RAG integration added")


if __name__ == "__main__":
    specialists_dir = Path(__file__).parent.parent / "data_pipeline_agent_lib" / "specialists"
    
    refactor_targets = [
        ("quality_assistant.py", "QualityAssistant"),
        ("hdl_commander.py", None),  # No class, direct tools
        ("ecosystem_assistant.py", None),  # No class, direct tools
        ("hdl_coordinator.py", None),  # No class, direct tools
    ]
    
    print("Batch RAG Refactor")
    print("=" * 50)
    
    for filename, class_name in refactor_targets:
        file_path = specialists_dir / filename
        if file_path.exists():
            print(f"\nProcessing: {filename}")
            if class_name:
                add_rag_imports(file_path, class_name)
            else:
                print(f"  ⏭️  Skipped (direct tool, manual refactor needed)")
        else:
            print(f"  ❌ Not found: {filename}")
    
    print("\n" + "=" * 50)
    print("Batch refactor complete!")

