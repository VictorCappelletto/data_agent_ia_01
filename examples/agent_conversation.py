#!/usr/bin/env python3
"""
DPL Agent v3.0 - Agent Conversation

Demonstrates full agent with LangGraph orchestration and conversation memory.
Requires: ANTHROPIC_API_KEY environment variable
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data_pipeline_agent_lib.agent import create_simple_hdl_graph
from data_pipeline_agent_lib.agent.state import create_initial_state
from data_pipeline_agent_lib.utils.checkpointer import create_conversation_config

# Check API key
if "ANTHROPIC_API_KEY" not in os.environ:
    print("ERROR: ANTHROPIC_API_KEY environment variable not set")
    print("\nSet it with:")
    print('  export ANTHROPIC_API_KEY="sk-ant-api03-your-key"')
    sys.exit(1)


def print_section(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"{title}")
    print("=" * 70)


def example_1_simple_query():
    """Example 1: Simple query without memory."""
    print_section("EXAMPLE 1: Simple Query")
    
    # Create agent
    print("\nCreating agent...")
    agent = create_simple_hdl_graph()
    
    # Query
    query = "What is SCD2 in DPL?"
    print(f"\nQuery: {query}")
    
    # Create state and invoke
    state = create_initial_state(query=query, session_id="session_001")
    result = agent.invoke(state)
    
    # Print response
    print("\nResponse:")
    print(result.get("final_response", "No response generated"))
    
    print("\nDone!")


def example_2_conversation_memory():
    """Example 2: Multi-turn conversation with memory."""
    print_section("EXAMPLE 2: Conversation with Memory")
    
    # Create agent
    print("\nCreating agent...")
    agent = create_simple_hdl_graph()
    
    # Create config with thread ID for memory
    thread_id = "thread_001"
    config = create_conversation_config(thread_id)
    
    # First question
    query1 = "What is SCD2?"
    print(f"\nUser: {query1}")
    
    state1 = create_initial_state(query=query1, session_id=thread_id)
    result1 = agent.invoke(state1, config=config)
    
    print(f"Agent: {result1.get('final_response', 'No response')[:200]}...")
    
    # Follow-up question (uses memory!)
    query2 = "How is it implemented in DPL?"
    print(f"\nUser: {query2}")
    
    state2 = create_initial_state(query=query2, session_id=thread_id)
    result2 = agent.invoke(state2, config=config)
    
    print(f"Agent: {result2.get('final_response', 'No response')[:200]}...")
    
    print("\nDone! Agent remembered context from first question.")


def example_3_troubleshooting():
    """Example 3: Real-world troubleshooting scenario."""
    print_section("EXAMPLE 3: Troubleshooting Scenario")
    
    # Create agent
    print("\nCreating agent...")
    agent = create_simple_hdl_graph()
    
    # Troubleshooting query
    query = "URGENT: Sessions streaming pipeline timed out after 90 minutes. How do I troubleshoot this?"
    print(f"\nQuery: {query}")
    
    # Create state and invoke
    state = create_initial_state(query=query, session_id="troubleshoot_001")
    result = agent.invoke(state)
    
    # Print response
    print("\nAgent Response:")
    print(result.get("final_response", "No response generated"))
    
    # Print reasoning if available
    if "reasoning" in result and result["reasoning"]:
        print("\nReasoning Steps:")
        for step in result["reasoning"]:
            print(f"  - {step}")
    
    print("\nDone!")


def main():
    """Run all examples."""
    print("DPL AGENT V3.0 - AGENT CONVERSATION EXAMPLES")
    print("Full LangGraph orchestration with memory")
    
    try:
        # Run examples
        example_1_simple_query()
        example_2_conversation_memory()
        example_3_troubleshooting()
        
        # Summary
        print_section("SUMMARY")
        print("All examples completed successfully!")
        print("\nWhat you learned:")
        print("- Simple queries with agent")
        print("- Multi-turn conversations with memory")
        print("- Real-world troubleshooting scenarios")
        print("\nNext steps:")
        print("- Try local_chat.py for interactive chat")
        print("- See databricks_deployment.py for production")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Verify ANTHROPIC_API_KEY is set correctly")
        print("2. Check internet connection")
        print("3. Ensure data_pipeline_agent_lib is installed")


if __name__ == "__main__":
    main()

