"""
DPL Agent v3.0 - Logging Configuration

Centralized logging system for DPL Agent with:
- Structured logging
- Multiple log levels
- Environment-aware configuration
- Correlation ID support
"""

import logging
import sys
from typing import Optional, Dict, Any
from datetime import datetime
import json


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

class DPLLogger:
    """
    Centralized logger for DPL Agent.
    
    Provides structured logging with different levels and formats
    for development vs production environments.
    """
    
    def __init__(self, name: str, level: any = "INFO"):
        """
        Initialize DPL Logger.
        
        Args:
            name: Logger name (usually __name__)
            level: Log level (string like "INFO" or int like logging.INFO)
        """
        self.logger = logging.getLogger(f"data_pipeline_agent.{name}")
        
        # Handle both string and int levels
        if isinstance(level, str):
            self.logger.setLevel(getattr(logging, level.upper()))
        else:
            self.logger.setLevel(level)
        
        # Add handler if not already added
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = DPLFormatter()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def debug(self, msg: str, **kwargs):
        """
        Log debug message (development only).
        
        Args:
            msg: Log message
            **kwargs: Additional context as key-value pairs
        """
        self.logger.debug(msg, extra={"context": kwargs})
    
    def info(self, msg: str, **kwargs):
        """
        Log info message (normal operations).
        
        Args:
            msg: Log message
            **kwargs: Additional context as key-value pairs
        """
        self.logger.info(msg, extra={"context": kwargs})
    
    def warning(self, msg: str, **kwargs):
        """
        Log warning message (attention needed).
        
        Args:
            msg: Log message
            **kwargs: Additional context as key-value pairs
        """
        self.logger.warning(msg, extra={"context": kwargs})
    
    def error(self, msg: str, exc_info: bool = True, **kwargs):
        """
        Log error message (something failed).
        
        Args:
            msg: Log message
            exc_info: Include exception traceback
            **kwargs: Additional context as key-value pairs
        """
        self.logger.error(msg, exc_info=exc_info, extra={"context": kwargs})
    
    def critical(self, msg: str, exc_info: bool = True, **kwargs):
        """
        Log critical message (system failure).
        
        Args:
            msg: Log message
            exc_info: Include exception traceback
            **kwargs: Additional context as key-value pairs
        """
        self.logger.critical(msg, exc_info=exc_info, extra={"context": kwargs})
    
    def log_timing(self, start_time: datetime, operation_name: str, **kwargs):
        """
        Log the duration of an operation.
        
        Args:
            start_time: Start time of the operation
            operation_name: Name of the operation
            **kwargs: Additional context
        """
        duration = (datetime.utcnow() - start_time).total_seconds()
        self.info(f"Operation '{operation_name}' completed", duration_seconds=duration, **kwargs)


class DPLFormatter(logging.Formatter):
    """
    Custom formatter for DPL Agent logs.
    
    Provides structured output with timestamp, level, logger name,
    and optional context data.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record.
        
        Args:
            record: Log record to format
            
        Returns:
            Formatted log string
        """
        # Base format
        timestamp = datetime.fromtimestamp(record.created).isoformat()
        level = record.levelname
        name = record.name
        message = record.getMessage()
        
        # Build log entry
        log_parts = [
            f"[{timestamp}]",
            f"[{level}]",
            f"[{name}]",
            message
        ]
        
        # Add context if available
        if hasattr(record, "context") and record.context:
            context_str = " ".join(f"{k}={v}" for k, v in record.context.items())
            log_parts.append(f"| {context_str}")
        
        # Add exception info if present
        if record.exc_info:
            log_parts.append("\n" + self.formatException(record.exc_info))
        
        return " ".join(log_parts)


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for production environments.
    
    Outputs logs in JSON format for easy parsing by log aggregation systems.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.
        
        Args:
            record: Log record to format
            
        Returns:
            JSON formatted log string
        """
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add context if available
        if hasattr(record, "context") and record.context:
            log_data["context"] = record.context
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_logger(name: str, level: str = "INFO") -> DPLLogger:
    """
    Get or create an DPL logger.
    
    Args:
        name: Logger name (usually __name__)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        DPLLogger instance
    """
    return DPLLogger(name, level)


def setup_logging(level: int = logging.INFO):
    """
    Configure the root logger for the DPL Agent.
    
    Args:
        level: Logging level (e.g., logging.INFO, logging.DEBUG)
    """
    # Ensure basic configuration is applied once
    if not logging.root.handlers:
        logging.basicConfig(
            level=level,
            stream=sys.stdout,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    # Set level for data_pipeline_agent specific loggers
    logging.getLogger("data_pipeline_agent").setLevel(level)


def configure_logging(
    level: str = "INFO",
    format_type: str = "standard",
    log_file: Optional[str] = None
):
    """
    Configure logging for DPL Agent.
    
    Args:
        level: Log level for all loggers
        format_type: "standard" or "json"
        log_file: Optional file path for log output
    """
    # Get root logger
    root_logger = logging.getLogger("data_pipeline_agent")
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    root_logger.handlers = []
    
    # Choose formatter
    if format_type == "json":
        formatter = JSONFormatter()
    else:
        formatter = DPLFormatter()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


# ============================================================================
# CONTEXT MANAGER FOR OPERATION LOGGING
# ============================================================================

class LogOperation:
    """
    Context manager for logging operations with timing.
    
    Usage:
        with LogOperation("Processing query", logger, query=query):
            result = process_query(query)
    """
    
    def __init__(
        self,
        operation_name: str,
        logger: DPLLogger,
        **context
    ):
        """
        Initialize operation logger.
        
        Args:
            operation_name: Name of the operation
            logger: DPL Logger instance
            **context: Additional context data
        """
        self.operation_name = operation_name
        self.logger = logger
        self.context = context
        self.start_time = None
    
    def __enter__(self):
        """Start operation logging."""
        self.start_time = datetime.now()
        self.logger.info(
            f"Starting operation: {self.operation_name}",
            **self.context
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Complete operation logging."""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.info(
                f"Completed operation: {self.operation_name}",
                duration_seconds=duration,
                **self.context
            )
        else:
            self.logger.error(
                f"Failed operation: {self.operation_name}",
                duration_seconds=duration,
                error_type=exc_type.__name__,
                **self.context
            )
        
        # Don't suppress exceptions
        return False

