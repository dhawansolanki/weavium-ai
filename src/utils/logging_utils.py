"""
Logging utilities for the Autogen Agents Framework.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str = "autogen_framework",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with the specified configuration.
    
    Args:
        name: Name of the logger
        level: Logging level (e.g., logging.INFO, logging.DEBUG)
        log_file: Path to the log file (None for console only)
        log_format: Format string for log messages
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Default format if not specified
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if log_file is specified
    if log_file:
        # Ensure the directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_default_log_file() -> str:
    """
    Get the default log file path.
    
    Returns:
        Path to the default log file
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create a log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"autogen_framework_{timestamp}.log"
    
    return str(log_file)

def log_conversation(
    logger: logging.Logger,
    sender: str,
    receiver: str,
    message: str,
    conversation_id: Optional[str] = None
) -> None:
    """
    Log a conversation message.
    
    Args:
        logger: Logger instance
        sender: Name of the sender
        receiver: Name of the receiver
        message: Message content
        conversation_id: Optional conversation ID
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "conversation_id": conversation_id,
        "sender": sender,
        "receiver": receiver,
        "message": message
    }
    
    logger.info(f"CONVERSATION: {log_entry}")

def log_agent_action(
    logger: logging.Logger,
    agent_name: str,
    action_type: str,
    details: dict
) -> None:
    """
    Log an agent action.
    
    Args:
        logger: Logger instance
        agent_name: Name of the agent
        action_type: Type of action (e.g., "tool_use", "memory_access")
        details: Dictionary with action details
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": agent_name,
        "action_type": action_type,
        "details": details
    }
    
    logger.info(f"AGENT_ACTION: {log_entry}")

def log_error(
    logger: logging.Logger,
    error_type: str,
    error_message: str,
    context: Optional[dict] = None
) -> None:
    """
    Log an error.
    
    Args:
        logger: Logger instance
        error_type: Type of error
        error_message: Error message
        context: Optional context information
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "error_type": error_type,
        "error_message": error_message,
        "context": context or {}
    }
    
    logger.error(f"ERROR: {log_entry}")
