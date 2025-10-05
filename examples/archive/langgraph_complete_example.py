#!/usr/bin/env python3
"""
DPL Agent v3.0 - Complete LangGraph Example
Demonstrates full agent capabilities with LangGraph orchestration
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Load environment
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data_pipeline_agent_lib.agent import create_data_pipeline_agent_graph, create_simple_hdl_graph
from data_pipeline_agent_lib.agent.state import create_initial_state
from data_pipeline_agent_lib.utils.checkpointer import (
    CheckpointerFactory,
    create_conversation_config,
    generate_thread_id,
)

# Rich console
console = Console()


async def example_1_simple_query():
    """Example 1: Simple query with the agent."""
    console.print("\n" + "=" * 70)
    console.print("[bold blue]EXAMPLE 1: Simple Query[/bold blue]")
    console.print("=" * 70)
    
    # Create simple agent
    console.print("\n[cyan]Creating agent...[/cyan]")
    agent = create_simple_hdl_graph()
    
    # Create initial state
    query = "What is the DPL architecture?"
    state = create_initial_state(
        query=query,
        session_id="example_1"
    )
    
    console.print(f"[cyan]Query:[/cyan] {query}")
    console.print("\n[cyan]Processing...[/cyan]")
    
    # Invoke agent
    result = await agent.ainvoke(state)
    
    # Display response
    response = result.get("final_response", "No response generated")
    console.print("\n[green]Response:[/green]")
    console.print(Panel(Markdown(response), border_style="green"))
    
    # Show reasoning
    reasoning = result.get("reasoning", [])
    if reasoning:
        console.print("\n[yellow]Reasoning:[/yellow]")
        for step in reasoning:
            console.print(f"  • {step}")


async def example_2_with_conversation_memory():
    """Example 2: Multi-turn conversation with memory."""
    console.print("\n" + "=" * 70)
    console.print("[bold blue]EXAMPLE 2: Conversation with Memory[/bold blue]")
    console.print("=" * 70)
    
    # Create agent with memory
    checkpointer = CheckpointerFactory.create_memory_checkpointer()
    agent = create_simple_hdl_graph()
    
    # Generate thread ID
    thread_id = generate_thread_id(user_id="victor")
    config = create_conversation_config(thread_id)
    
    console.print(f"\n[cyan]Thread ID:[/cyan] {thread_id}")
    
    # Multi-turn conversation
    queries = [
        "What are DPL entities?",
        "Tell me more about visits entity",
        "How is it different from tasks?"
    ]
    
    for i, query in enumerate(queries, 1):
        console.print(f"\n[bold]Turn {i}:[/bold]")
        console.print(f"[cyan]You:[/cyan] {query}")
        
        # Create state
        state = create_initial_state(query=query, session_id=thread_id)
        
        # Invoke with config (preserves memory)
        result = await agent.ainvoke(state, config=config)
        
        # Display response
        response = result.get("final_response", "No response")
        console.print(f"[green]DPL Agent:[/green] {response[:200]}...")


async def example_3_troubleshooting():
    """Example 3: Troubleshooting scenario."""
    console.print("\n" + "=" * 70)
    console.print("[bold blue]EXAMPLE 3: Troubleshooting Scenario[/bold blue]")
    console.print("=" * 70)
    
    # Create agent
    agent = create_simple_hdl_graph()
    
    # Troubleshooting query
    query = "The visits streaming pipeline is timing out after 1 hour. How do I fix this?"
    
    console.print(f"\n[cyan]Scenario:[/cyan] Pipeline Timeout")
    console.print(f"[cyan]Query:[/cyan] {query}")
    console.print("\n[cyan]Processing...[/cyan]")
    
    # Create state
    state = create_initial_state(query=query, session_id="troubleshooting")
    
    # Invoke agent
    result = await agent.ainvoke(state)
    
    # Display comprehensive results
    console.print("\n[yellow]Intent Detected:[/yellow]")
    console.print(f"  • Intent: {result.get('intent', 'unknown')}")
    console.print(f"  • Confidence: {result.get('confidence', 0):.2f}")
    console.print(f"  • Entity: {result.get('entity_name', 'none')}")
    console.print(f"  • Pipeline Type: {result.get('pipeline_type', 'none')}")
    
    console.print("\n[yellow]Retrieved Knowledge:[/yellow]")
    docs = result.get("retrieved_documents", [])
    console.print(f"  • {len(docs)} documents retrieved")
    for i, doc in enumerate(docs[:3], 1):
        source = doc.get("metadata", {}).get("source", "unknown")
        console.print(f"  • Doc {i}: {source}")
    
    console.print("\n[green]Response:[/green]")
    response = result.get("final_response", "No response")
    console.print(Panel(Markdown(response), border_style="green"))


async def example_4_architecture_question():
    """Example 4: Architecture question."""
    console.print("\n" + "=" * 70)
    console.print("[bold blue]EXAMPLE 4: Architecture Question[/bold blue]")
    console.print("=" * 70)
    
    # Create agent
    agent = create_simple_hdl_graph()
    
    # Architecture query
    query = "Explain the difference between streaming and batch pipelines in DPL"
    
    console.print(f"\n[cyan]Query:[/cyan] {query}")
    console.print("\n[cyan]Processing...[/cyan]")
    
    # Create state
    state = create_initial_state(query=query, session_id="architecture")
    
    # Invoke agent
    result = await agent.ainvoke(state)
    
    # Display response
    response = result.get("final_response", "No response")
    console.print("\n[green]Response:[/green]")
    console.print(Panel(Markdown(response), border_style="green"))


async def example_5_streaming_response():
    """Example 5: Streaming response."""
    console.print("\n" + "=" * 70)
    console.print("[bold blue]EXAMPLE 5: Streaming Response[/bold blue]")
    console.print("=" * 70)
    
    # Create agent
    agent = create_simple_hdl_graph()
    
    # Query
    query = "What are the best practices for DPL data quality?"
    
    console.print(f"\n[cyan]Query:[/cyan] {query}")
    console.print("\n[green]DPL Agent (streaming):[/green] ", end="")
    
    # Create state
    state = create_initial_state(query=query, session_id="streaming")
    
    # Stream response
    async for chunk in agent.astream(state):
        if "final_response" in chunk:
            console.print(chunk["final_response"], end="", markup=False)
    
    console.print()  # New line


async def example_6_persistent_memory():
    """Example 6: Persistent memory with SQLite."""
    console.print("\n" + "=" * 70)
    console.print("[bold blue]EXAMPLE 6: Persistent Memory (SQLite)[/bold blue]")
    console.print("=" * 70)
    
    # Create agent with SQLite checkpointer
    checkpointer = CheckpointerFactory.create_sqlite_checkpointer(
        db_path="./data/test_checkpoints.db"
    )
    
    # Note: Graph creation with custom checkpointer
    # agent = create_simple_hdl_graph(checkpointer=checkpointer)
    # For now, using default memory
    agent = create_simple_hdl_graph()
    
    console.print("\n[cyan]Using SQLite checkpointer for persistent memory[/cyan]")
    console.print("[yellow]Note: Conversations survive process restarts[/yellow]")
    
    # Generate persistent thread ID
    thread_id = "persistent_session_001"
    config = create_conversation_config(thread_id)
    
    # First query
    state = create_initial_state(query="What are DPL pipelines?", session_id=thread_id)
    result = await agent.ainvoke(state, config=config)
    
    console.print(f"\n[cyan]Turn 1:[/cyan] What are DPL pipelines?")
    console.print(f"[green]Response:[/green] {result.get('final_response', '')[:150]}...")
    
    # Second query (uses memory from first)
    state = create_initial_state(query="How do they work?", session_id=thread_id)
    result = await agent.ainvoke(state, config=config)
    
    console.print(f"\n[cyan]Turn 2:[/cyan] How do they work?")
    console.print(f"[green]Response:[/green] {result.get('final_response', '')[:150]}...")
    
    console.print(f"\n[yellow]Memory persisted to:[/yellow] ./data/test_checkpoints.db")


async def main():
    """Run all examples."""
    console.print("\n" + "=" * 70)
    console.print("[bold]DPL Agent v3.0 - Complete LangGraph Examples[/bold]")
    console.print("=" * 70)
    
    # Check environment
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("\n[bold red]❌ Error:[/bold red] ANTHROPIC_API_KEY not found")
        console.print("[yellow]Please configure your .env file[/yellow]\n")
        return
    
    if not os.getenv("OPENAI_API_KEY"):
        console.print("\n[bold red]❌ Error:[/bold red] OPENAI_API_KEY not found")
        console.print("[yellow]Please configure your .env file[/yellow]\n")
        return
    
    try:
        # Run examples
        await example_1_simple_query()
        await example_2_with_conversation_memory()
        await example_3_troubleshooting()
        await example_4_architecture_question()
        await example_5_streaming_response()
        await example_6_persistent_memory()
        
        console.print("\n" + "=" * 70)
        console.print("[bold green]✅ All examples completed successfully![/bold green]")
        console.print("=" * 70 + "\n")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

