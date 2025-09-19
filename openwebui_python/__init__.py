"""
OpenWebUI Python SDK

A client library for interacting with the OpenWebUI API.
"""

import logging
from .client import OpenWebUI, BaseClient
from .utils.logging import setup_logging

# Set up a null handler to avoid "No handler found" warnings
logging.getLogger('OpenWebUI').addHandler(logging.NullHandler())

# Package metadata
__version__ = '0.1.0'
__author__ = 'John Provost'
__all__ = ['OpenWebUI', 'BaseClient', 'setup_logging']
