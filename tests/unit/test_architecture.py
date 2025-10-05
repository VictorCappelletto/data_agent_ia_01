"""
Test Clean Architecture Compliance

Validates that the codebase follows Clean Architecture principles:
- Domain doesn't depend on Infrastructure
- Application depends on Domain ports, not Infrastructure
- Infrastructure implements Domain ports
- Dependency Injection is used correctly
"""

import pytest
from typing import get_type_hints
import inspect


def test_vector_store_port_exists():
    """Test that VectorStorePort is defined in domain layer."""
    from dpl_agent_lib.domain.ports import VectorStorePort
    
    assert VectorStorePort is not None
    assert inspect.isabstract(VectorStorePort)


def test_chroma_implements_port():
    """Test that ChromaVectorStore implements VectorStorePort correctly."""
    from dpl_agent_lib.domain.ports import VectorStorePort
    from dpl_agent_lib.infrastructure.vector_store import ChromaVectorStore
    
    # Check inheritance
    assert issubclass(ChromaVectorStore, VectorStorePort)
    
    # Check required methods are implemented
    port_methods = {
        name for name, method in inspect.getmembers(VectorStorePort, predicate=inspect.isfunction)
        if not name.startswith('_')
    }
    
    impl_methods = {
        name for name, method in inspect.getmembers(ChromaVectorStore, predicate=inspect.isfunction)
        if not name.startswith('_')
    }
    
    # All abstract methods must be implemented
    missing_methods = port_methods - impl_methods
    assert len(missing_methods) == 0, f"Missing implementations: {missing_methods}"


def test_dpl_retriever_uses_port():
    """Test that DPLRetriever depends on VectorStorePort (interface)."""
    from dpl_agent_lib.infrastructure.vector_store import DPLRetriever
    from dpl_agent_lib.domain.ports import VectorStorePort
    
    # Get type hints from __init__
    init_signature = inspect.signature(DPLRetriever.__init__)
    vector_store_param = init_signature.parameters.get('vector_store')
    
    assert vector_store_param is not None, "DPLRetriever must have vector_store parameter"
    assert vector_store_param.annotation == VectorStorePort, (
        f"DPLRetriever must accept VectorStorePort, not {vector_store_param.annotation}"
    )


def test_retriever_service_uses_dependency_injection():
    """Test that DPLRetrieverService receives dependencies via constructor."""
    from dpl_agent_lib.application.services.dpl_retriever_service import DPLRetrieverService
    from dpl_agent_lib.infrastructure.vector_store import DPLRetriever
    
    # Check constructor signature
    init_signature = inspect.signature(DPLRetrieverService.__init__)
    retriever_param = init_signature.parameters.get('retriever')
    
    assert retriever_param is not None, "Service must receive retriever via constructor"
    assert retriever_param.annotation == DPLRetriever, (
        "Service must be typed to receive DPLRetriever"
    )


def test_domain_has_no_infrastructure_imports():
    """Test that domain layer doesn't import from infrastructure."""
    import dpl_agent_lib.domain as domain_module
    import ast
    import os
    from pathlib import Path
    
    domain_path = Path(domain_module.__file__).parent
    violations = []
    
    for py_file in domain_path.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        with open(py_file, 'r') as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError:
                continue
                
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and 'infrastructure' in node.module:
                    violations.append(f"{py_file.name}: imports from {node.module}")
    
    assert len(violations) == 0, (
        f"Domain layer must NOT import from Infrastructure:\n" + "\n".join(violations)
    )


def test_factory_uses_dependency_injection():
    """Test that factory functions use proper Dependency Injection."""
    from dpl_agent_lib.infrastructure.vector_store import create_hdl_retriever
    from dpl_agent_lib.domain.ports import VectorStorePort
    
    # Check factory signature
    factory_signature = inspect.signature(create_hdl_retriever)
    vector_store_param = factory_signature.parameters.get('vector_store')
    
    assert vector_store_param is not None, "Factory must accept vector_store"
    assert vector_store_param.annotation == VectorStorePort, (
        "Factory must be typed to accept VectorStorePort interface"
    )


def test_get_hdl_retriever_composes_dependencies():
    """Test that get_hdl_retriever() properly composes the stack with DI."""
    from dpl_agent_lib.infrastructure.vector_store import get_hdl_retriever
    
    # This should work without errors (creates full stack with DI)
    retriever = get_hdl_retriever()
    
    assert retriever is not None
    assert hasattr(retriever, 'vector_store'), "Retriever must have vector_store attribute"
    
    # Check that vector_store is a VectorStorePort implementation
    from dpl_agent_lib.domain.ports import VectorStorePort
    assert isinstance(retriever.vector_store, VectorStorePort)


def test_application_service_can_be_instantiated_with_di():
    """Test that application service can be created with injected dependencies."""
    from dpl_agent_lib.application.services.dpl_retriever_service import DPLRetrieverService
    from dpl_agent_lib.infrastructure.vector_store import get_hdl_retriever
    
    # Create dependencies
    retriever = get_hdl_retriever()
    
    # Inject into service
    service = DPLRetrieverService(retriever)
    
    assert service is not None
    assert service.retriever is not None


def test_architecture_follows_dependency_rule():
    """
    Test the Dependency Rule:
    Infrastructure -> Application -> Domain
    (Dependencies point inward, never outward)
    """
    from dpl_agent_lib.domain.ports import VectorStorePort
    from dpl_agent_lib.infrastructure.vector_store import ChromaVectorStore, DPLRetriever
    from dpl_agent_lib.application.services.dpl_retriever_service import DPLRetrieverService
    
    # Infrastructure (ChromaVectorStore) depends on Domain (VectorStorePort)
    assert issubclass(ChromaVectorStore, VectorStorePort)
    
    # Infrastructure (DPLRetriever) depends on Domain (VectorStorePort)
    init_sig = inspect.signature(DPLRetriever.__init__)
    assert init_sig.parameters['vector_store'].annotation == VectorStorePort
    
    # Application (Service) depends on Infrastructure abstraction, not concrete impl
    service_sig = inspect.signature(DPLRetrieverService.__init__)
    assert service_sig.parameters['retriever'].annotation == DPLRetriever


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

