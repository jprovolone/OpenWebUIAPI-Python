"""
Logging utilities for the OpenWebUI Python SDK.
"""

import logging
import sys
from typing import Optional, Union

def setup_logging(
    level: Union[int, str] = logging.INFO,
    format_string: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging for the OpenWebUI SDK.
    
    Args:
        level: The logging level (default: INFO).
        format_string: Custom format string for log messages.
        log_file: Optional file path to write logs to.
        
    Returns:
        The configured logger instance.
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logger = logging.getLogger('OpenWebUI')
    logger.setLevel(level)
    
    # Remove existing handlers if any
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(console_handler)
    
    # Create file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(format_string))
        logger.addHandler(file_handler)
    
    return logger
