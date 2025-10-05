#!/usr/bin/env python3
"""
DPL Agent v3.0 - Databricks Deployment

Production deployment patterns for Databricks environment.
Shows package installation, secret management, and usage patterns.
"""

import sys
from pathlib import Path

# Add project root to path (not needed in Databricks after install)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def print_section(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"{title}")
    print("=" * 70)


def demo_1_installation():
    """Demo 1: Package installation."""
    print_section("DEMO 1: Package Installation")
    
    print("\nInstallation command:")
    print("  %pip install /dbfs/FileStore/libraries/data_pipeline_agent_lib-3.0.0-py3-none-any.whl")
    print("  dbutils.library.restartPython()")
    
    print("\nVerification:")
    print("  import data_pipeline_agent_lib")
    print("  print(f'DPL Agent v{data_pipeline_agent_lib.__version__}')")


def demo_2_secret_configuration():
    """Demo 2: API key configuration with secrets."""
    print_section("DEMO 2: API Key Configuration")
    
    print("\nCreate secret scope (CLI):")
    print("  databricks secrets create-scope --scope hdl-agent-secrets")
    
    print("\nAdd API key (CLI):")
    print("  databricks secrets put-secret \\")
    print("    --scope hdl-agent-secrets \\")
    print("    --key anthropic-api-key \\")
    print('    --string-value "sk-ant-api03-your-key"')
    
    print("\nUse in notebook:")
    print("  import os")
    print('  api_key = dbutils.secrets.get("hdl-agent-secrets", "anthropic-api-key")')
    print('  os.environ["ANTHROPIC_API_KEY"] = api_key')


def demo_3_specialist_usage():
    """Demo 3: Using specialists in Databricks."""
    print_section("DEMO 3: Specialist Usage")
    
    print("\nImport specialists:")
    print("  from data_pipeline_agent_lib.specialists import (")
    print("      troubleshoot_hdl_error,")
    print("      coordinate_hdl_reprocessing,")
    print("  )")
    
    print("\nDiagnose error:")
    print('  diagnosis = troubleshoot_hdl_error(')
    print('      "Pipeline timed out after 90 minutes"')
    print('  )')
    print('  print(diagnosis)')
    
    print("\nCoordinate reprocessing:")
    print('  plan = coordinate_hdl_reprocessing(')
    print('      "TASKS for October 4th. Notify KPI team."')
    print('  )')
    print('  print(plan)')


def demo_4_full_agent():
    """Demo 4: Full agent in Databricks."""
    print_section("DEMO 4: Full Agent Usage")
    
    print("\nImport agent components:")
    print("  from data_pipeline_agent_lib.agent import create_simple_hdl_graph")
    print("  from data_pipeline_agent_lib.agent.state import create_initial_state")
    
    print("\nCreate and use agent:")
    print("  agent = create_simple_hdl_graph()")
    print("  ")
    print('  state = create_initial_state(')
    print('      query="How do I troubleshoot timeout in visits?",')
    print('      session_id="notebook_session"')
    print('  )')
    print("  ")
    print("  result = agent.invoke(state)")
    print('  print(result["final_response"])')


def demo_5_production_patterns():
    """Demo 5: Production best practices."""
    print_section("DEMO 5: Production Patterns")
    
    print("\n1. Cluster Configuration:")
    print("   - Install library at cluster level")
    print("   - Use init scripts for automatic setup")
    print("   - Configure secrets before notebook execution")
    
    print("\n2. Error Handling:")
    print("   try:")
    print("       result = troubleshoot_hdl_error(error_msg)")
    print("   except Exception as e:")
    print('       print(f"Error: {e}")')
    print("       # Fallback to manual process")
    
    print("\n3. Logging:")
    print("   from data_pipeline_agent_lib.utils import get_logger")
    print('   logger = get_logger(__name__)')
    print('   logger.info("Starting DPL analysis")')
    
    print("\n4. Performance:")
    print("   - Use specialists directly when possible (no LLM call)")
    print("   - Cache agent instance for multiple queries")
    print("   - Monitor token usage for cost control")


def main():
    """Run all Databricks demos."""
    print("DPL AGENT V3.0 - DATABRICKS DEPLOYMENT")
    print("Production patterns and best practices")
    
    # Run demos
    demo_1_installation()
    demo_2_secret_configuration()
    demo_3_specialist_usage()
    demo_4_full_agent()
    demo_5_production_patterns()
    
    # Summary
    print_section("SUMMARY")
    print("Databricks deployment patterns demonstrated!")
    print("\nWhat you learned:")
    print("- Package installation in Databricks")
    print("- Secret management for API keys")
    print("- Using specialists in notebooks")
    print("- Full agent deployment")
    print("- Production best practices")
    print("\nNext steps:")
    print("- Install package in your Databricks cluster")
    print("- Configure secrets for API keys")
    print("- Try specialists in your notebooks")
    print("- Deploy full agent for interactive queries")


if __name__ == "__main__":
    main()

