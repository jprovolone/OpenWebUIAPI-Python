"""
Error models for the OpenWebUI Python SDK.

This module defines error models and exceptions used throughout the SDK.
"""

from dataclasses import dataclass, field
from typing import Optional, Union, Dict, Any
from .base import BaseModel

@dataclass
class ValidationErrorItem(BaseModel):
    """
    Represents a validation error returned by the API.
    """
    success: bool = False
    content: Optional[str] = None
    message: Optional[str] = None
    detail: Optional[str] = None
    loc: Optional[Union[str, int]] = None
    id: Optional[str] = None  # Added to handle response with id field

class OpenWebUIError(Exception):
    """
    Base exception class for OpenWebUI API errors.
    """
    def __init__(self, message: str, response=None):
        self.message = message
        self.response = response
        super().__init__(message)

class AuthenticationError(OpenWebUIError):
    """
    Raised when authentication fails.
    """
    pass

class ResourceNotFoundError(OpenWebUIError):
    """
    Raised when a requested resource is not found.
    """
    pass

class ValidationError(OpenWebUIError):
    """
    Raised when request validation fails.
    """
    def __init__(self, message: str, errors=None, response=None):
        self.errors = errors
        super().__init__(message, response)

class APIError(OpenWebUIError):
    """
    Raised when the API returns an error.
    """
    pass

class RateLimitError(OpenWebUIError):
    """
    Raised when the API rate limit is exceeded.
    """
    pass

class ServerError(OpenWebUIError):
    """
    Raised when the API server encounters an error.
    """
    pass
