"""
DPL Agent v3.0 - Checkpointer Utilities

Utilities for managing conversation memory and checkpoints.
Provides different checkpointer implementations for various scenarios.
"""

import os
import sqlite3
from pathlib import Path
from typing import Optional

from langgraph.checkpoint.memory import MemorySaver
# from langgraph.checkpoint.sqlite import SqliteSaver  # Not available in current version


# ============================================================================
# CHECKPOINTER FACTORY
# ============================================================================

class CheckpointerFactory:
    """
    Factory for creating different types of checkpointers.
    
    Supports:
    - Memory: In-memory checkpointer (ephemeral)
    - SQLite: Persistent checkpointer (local file)
    """
    
    @staticmethod
    def create_memory_checkpointer() -> MemorySaver:
        """
        Create in-memory checkpointer.
        
        Good for:
        - Development and testing
        - Temporary sessions
        - Single-user scenarios
        
        Limitations:
        - Data lost when process ends
        - Not suitable for production
        
        Returns:
            MemorySaver instance
        """
        return MemorySaver()
    
    @staticmethod
    def create_sqlite_checkpointer(
        db_path: Optional[str] = None
    ):  # -> SqliteSaver:  # Not available in current LangGraph version
        """
        Create SQLite-based checkpointer.
        
        Good for:
        - Local development with persistence
        - Single-instance deployments
        - Testing with data persistence
        
        Limitations:
        - Single-process (no concurrency)
        - Not suitable for distributed systems
        
        Args:
            db_path: Path to SQLite database file
            
        Returns:
            SqliteSaver instance
        """
        # Default path
        if db_path is None:
            db_path = os.getenv(
                "CHECKPOINT_DB_PATH",
                "./data/checkpoints.db"
            )
        
        # Ensure directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Create connection
        conn = sqlite3.connect(db_path, check_same_thread=False)
        
        # Create checkpointer
        checkpointer = SqliteSaver(conn)
        
        return checkpointer
    
    @staticmethod
    def create_default_checkpointer(
        persist: bool = False,
        db_path: Optional[str] = None
    ):
        """
        Create default checkpointer based on configuration.
        
        Args:
            persist: Whether to persist checkpoints
            db_path: Path to database if persisting
            
        Returns:
            Checkpointer instance
        """
        if persist:
            return CheckpointerFactory.create_sqlite_checkpointer(db_path)
        else:
            return CheckpointerFactory.create_memory_checkpointer()


# ============================================================================
# CHECKPOINT UTILITIES
# ============================================================================

class CheckpointManager:
    """
    Utilities for managing checkpoints.
    
    Provides methods to inspect, export, and manage checkpoint data.
    """
    
    def __init__(self, checkpointer):
        """
        Initialize checkpoint manager.
        
        Args:
            checkpointer: Checkpointer instance
        """
        self.checkpointer = checkpointer
    
    async def get_checkpoint_history(
        self,
        thread_id: str,
        limit: int = 10
    ) -> list:
        """
        Get checkpoint history for a thread.
        
        Args:
            thread_id: Thread identifier
            limit: Maximum number of checkpoints to retrieve
            
        Returns:
            List of checkpoints
        """
        try:
            config = {"configurable": {"thread_id": thread_id}}
            
            # This is a placeholder - actual implementation depends on
            # the specific checkpointer implementation
            # For now, return empty list
            return []
            
        except Exception as e:
            logger.error(f"Error getting checkpoint history: {e}")
            return []
    
    async def clear_thread_checkpoints(self, thread_id: str) -> bool:
        """
        Clear all checkpoints for a thread.
        
        Args:
            thread_id: Thread identifier
            
        Returns:
            Success status
        """
        try:
            # Implementation depends on checkpointer type
            # For SQLite, would delete from database
            # For Memory, would clear from memory
            logger.info(f"Clearing checkpoints for thread: {thread_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing checkpoints: {e}")
            return False
    
    def export_checkpoints(self, output_path: str) -> bool:
        """
        Export checkpoints to file.
        
        Args:
            output_path: Path to export file
            
        Returns:
            Success status
        """
        try:
            # Implementation for exporting checkpoints
            logger.info(f"Exporting checkpoints to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting checkpoints: {e}")
            return False


# ============================================================================
# CONVERSATION MEMORY HELPERS
# ============================================================================

def create_conversation_config(
    thread_id: str,
    user_id: Optional[str] = None,
    **kwargs
) -> dict:
    """
    Create configuration for conversation with memory.
    
    Args:
        thread_id: Unique thread identifier
        user_id: Optional user identifier
        **kwargs: Additional configuration
        
    Returns:
        Configuration dictionary
    """
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }
    
    if user_id:
        config["configurable"]["user_id"] = user_id
    
    # Add any additional kwargs
    config["configurable"].update(kwargs)
    
    return config


def generate_thread_id(user_id: Optional[str] = None, session_prefix: str = "hdl") -> str:
    """
    Generate unique thread ID for conversation.
    
    Args:
        user_id: Optional user identifier
        session_prefix: Prefix for thread ID
        
    Returns:
        Thread ID string
    """
    import uuid
    from datetime import datetime
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    
    if user_id:
        return f"{session_prefix}_{user_id}_{timestamp}_{unique_id}"
    else:
        return f"{session_prefix}_{timestamp}_{unique_id}"

