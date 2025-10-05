#!/usr/bin/env python3
"""
DPL Agent v3.0 - Local CLI Interface
Standalone LangGraph agent for DPL operations
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

# Rich console for beautiful output
console = Console()


def check_environment() -> bool:
    """Check if required environment variables are set."""
    required_vars = [
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        console.print("\n[bold red]❌ Missing required environment variables:[/bold red]")
        for var in missing_vars:
            console.print(f"  - {var}")
        console.print("\n[yellow]Please configure your .env file with the required API keys.[/yellow]")
        console.print("[yellow]See .env.example for reference.[/yellow]\n")
        return False
    
    return True


def print_welcome():
    """Print welcome message."""
    welcome_text = """
# 🤖 DPL Agent v3.0

**LangGraph-powered standalone specialist for DPL operations**

Available commands:
- Ask anything about DPL pipelines, workflows, or troubleshooting
- Type `exit` or `quit` to end the session
- Type `clear` to clear conversation history
- Type `help` for more information

**Examples:**
- "Why is the visits streaming pipeline failing?"
- "How do I optimize the tasks batch pipeline?"
- "What's the current status of DPL workflows?"
    """
    
    console.print(Panel(
        Markdown(welcome_text),
        title="[bold blue]Welcome[/bold blue]",
        border_style="blue"
    ))


def print_help():
    """Print help information."""
    help_text = """
# DPL Agent Help

## Available Commands
- `exit` / `quit` - End the session
- `clear` - Clear conversation history
- `help` - Show this help message

## DPL Specialists
The agent has access to 7 specialized assistants:
1. **Troubleshooter** - Pipeline error diagnosis
2. **Bug Resolver** - Automated problem resolution
3. **Performance Advisor** - Optimization recommendations
4. **Quality Assistant** - Data quality validation
5. **DPL Commander** - Workflow execution
6. **Ecosystem Assistant** - Documentation & guidance
7. **DPL Coordinator** - Multi-task orchestration

## Example Queries
- "Debug the visits streaming pipeline timeout"
- "Show me SCD2 merge best practices"
- "What's the difference between batch and streaming ingestion?"
- "Check data quality for tasks entity"
    """
    
    console.print(Panel(
        Markdown(help_text),
        title="[bold green]Help[/bold green]",
        border_style="green"
    ))


async def run_chat_loop():
    """Run the interactive chat loop."""
    # Import here to avoid circular imports
    try:
        from data_pipeline_agent_lib.agent.graph import create_data_pipeline_agent_graph
    except ImportError:
        console.print("\n[bold red]❌ Error: DPL Agent library not found.[/bold red]")
        console.print("[yellow]The agent implementation is not yet complete.[/yellow]")
        console.print("[yellow]This is a placeholder for the full implementation.[/yellow]\n")
        return
    
    # Create agent
    console.print("\n[cyan]🔄 Initializing DPL Agent...[/cyan]")
    
    try:
        agent = create_data_pipeline_agent_graph()
        console.print("[green]✅ Agent ready![/green]\n")
    except Exception as e:
        console.print(f"\n[bold red]❌ Error initializing agent:[/bold red] {e}\n")
        return
    
    # Chat configuration
    config = {"configurable": {"thread_id": "local-session"}}
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = console.input("\n[bold blue]You:[/bold blue] ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ["exit", "quit"]:
                console.print("\n[green]👋 Goodbye![/green]\n")
                break
            
            if user_input.lower() == "clear":
                config["configurable"]["thread_id"] = f"session-{asyncio.get_event_loop().time()}"
                console.print("\n[green]✓ Conversation history cleared[/green]")
                continue
            
            if user_input.lower() == "help":
                print_help()
                continue
            
            # Process query
            console.print("\n[cyan]DPL Agent:[/cyan] ", end="")
            
            # Stream response
            async for chunk in agent.astream(
                {"messages": [{"role": "user", "content": user_input}]},
                config
            ):
                if "messages" in chunk:
                    content = chunk["messages"][-1].get("content", "")
                    console.print(content, end="", markup=False)
            
            console.print()  # New line after response
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
        except Exception as e:
            console.print(f"\n[bold red]❌ Error:[/bold red] {e}\n")


def main():
    """Main entry point."""
    # Print welcome
    print_welcome()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run chat loop
    try:
        asyncio.run(run_chat_loop())
    except KeyboardInterrupt:
        console.print("\n\n[green]👋 Goodbye![/green]\n")
    except Exception as e:
        console.print(f"\n[bold red]❌ Fatal error:[/bold red] {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

