"""
Data models for the OpenWebUI Python SDK.

This package contains all the data models used throughout the SDK.
"""

from .base import BaseModel
from .error import ValidationErrorItem, OpenWebUIError, AuthenticationError, ResourceNotFoundError, ValidationError, APIError, RateLimitError, ServerError
from .model import Model, Action, Pipe, Info, Meta, Ollama, OpenAI, TopProvider, Pricing, Architecture, Details, AccessControl
from .chat import Message, Choice, ChatCompletion, ChatWithFile, ChatWithCollection
from .file import OpenWebFile, FileData, FileMeta
from .user import User
from .knowledge import Knowledge

__all__ = [
    'BaseModel',
    'ValidationErrorItem',
    'OpenWebUIError',
    'AuthenticationError',
    'ResourceNotFoundError',
    'ValidationError',
    'APIError',
    'RateLimitError',
    'ServerError',
    'Model',
    'Action',
    'Pipe',
    'Info',
    'Meta',
    'Ollama',
    'OpenAI',
    'TopProvider',
    'Pricing',
    'Architecture',
    'Details',
    'AccessControl',
    'Message',
    'Choice',
    'ChatCompletion',
    'ChatWithFile',
    'ChatWithCollection',
    'OpenWebFile',
    'FileData',
    'FileMeta',
    'User',
    'Knowledge',
]
