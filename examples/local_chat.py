#!/usr/bin/env python3
"""
DPL Agent v3.0 - Local Chat

Interactive chat interface for local development and testing.
Requires: ANTHROPIC_API_KEY environment variable
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Check API key
if "ANTHROPIC_API_KEY" not in os.environ:
    print("ERROR: ANTHROPIC_API_KEY environment variable not set")
    print("\nSet it with:")
    print('  export ANTHROPIC_API_KEY="sk-ant-api03-your-key"')
    sys.exit(1)

from data_pipeline_agent_lib.agent import create_simple_hdl_graph
from data_pipeline_agent_lib.agent.state import create_initial_state
from data_pipeline_agent_lib.utils.checkpointer import create_conversation_config


def print_welcome():
    """Print welcome message."""
    print("=" * 70)
    print("DPL AGENT V3.0 - LOCAL CHAT")
    print("=" * 70)
    print("\nInteractive chat with DPL specialist agent.")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("Type 'clear' to start a new conversation.")
    print("\n" + "=" * 70)


def chat_loop():
    """Main chat loop."""
    print_welcome()
    
    # Create agent
    print("\nInitializing agent...")
    agent = create_simple_hdl_graph()
    print("Agent ready!")
    
    # Session management
    session_id = "local_chat_001"
    config = create_conversation_config(session_id)
    turn_count = 0
    
    while True:
        # Get user input
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break
        
        # Handle commands
        if user_input.lower() in ['exit', 'quit']:
            print("\nGoodbye!")
            break
        
        if user_input.lower() == 'clear':
            session_id = f"local_chat_{turn_count + 1}"
            config = create_conversation_config(session_id)
            print("\nConversation cleared. Starting fresh.")
            continue
        
        if not user_input:
            continue
        
        # Process query
        try:
            print("\nAgent: ", end="", flush=True)
            
            state = create_initial_state(
                query=user_input,
                session_id=session_id
            )
            
            result = agent.invoke(state, config=config)
            response = result.get("final_response", "I couldn't generate a response.")
            
            print(response)
            turn_count += 1
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


def main():
    """Run chat interface."""
    try:
        chat_loop()
    except Exception as e:
        print(f"\nFatal error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify ANTHROPIC_API_KEY is set correctly")
        print("2. Check internet connection")
        print("3. Ensure data_pipeline_agent_lib is installed")
        sys.exit(1)


if __name__ == "__main__":
    main()
