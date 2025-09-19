"""
Chat-related data models for the OpenWebUI Python SDK.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from .base import BaseModel

@dataclass
class Message(BaseModel):
    """
    Represents a message in a chat conversation.
    """
    content: str = field(default=None)  # Add default to fix dataclass order
    role: str = field(default=None)     # Add default to fix dataclass order
    refusal: Optional[Any] = None
    
    def __post_init__(self):
        """Validate required fields and call parent post_init"""
        if self.content is None:
            raise ValueError("content cannot be None")
        if self.role is None:
            raise ValueError("role cannot be None")
        super().__post_init__()

@dataclass
class Choice(BaseModel):
    """
    Represents a response choice returned by the chat completion API.
    """
    index: int = field(default=None)    # Add default to fix dataclass order
    message: Message = field(default=None)  # Add default to fix dataclass order
    logprobs: Optional[Dict] = None
    finish_reason: Optional[str] = None
    
    def __post_init__(self):
        """Validate required fields and call parent post_init"""
        if self.index is None:
            raise ValueError("index cannot be None")
        if self.message is None:
            raise ValueError("message cannot be None")
        super().__post_init__()

@dataclass
class ChatCompletion(BaseModel):
    """
    Represents a chat completion response from the API.
    """
    choices: List[Choice] = field(default_factory=list)
    id: Optional[str] = None
    model: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    usage: Optional[Dict[str, Any]] = None
    system_fingerprint: Optional[str] = None
    
    def __post_init__(self):
        """Validate required fields and call parent post_init"""
        if not self.choices:
            raise ValueError("choices cannot be empty")
        super().__post_init__()

@dataclass
class ChatWithFile(BaseModel):
    """
    Represents a chat with file response.
    """
    detail: str = field(default=None)  # Add default to fix dataclass order
    
    def __post_init__(self):
        """Validate required fields and call parent post_init"""
        if self.detail is None:
            raise ValueError("detail cannot be None")
        super().__post_init__()

@dataclass
class ChatWithCollection(BaseModel):
    """
    Represents a chat with collection response.
    """
    id: str = field(default=None)  # Add default to fix dataclass order
    model: str = field(default=None)  # Add default to fix dataclass order
    object: str = field(default=None)  # Add default to fix dataclass order
    created: int = field(default=None)  # Add default to fix dataclass order
    choices: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate required fields and call parent post_init"""
        if self.id is None:
            raise ValueError("id cannot be None")
        if self.model is None:
            raise ValueError("model cannot be None")
        if self.object is None:
            raise ValueError("object cannot be None")
        if self.created is None:
            raise ValueError("created cannot be None")
        if not self.choices:
            raise ValueError("choices cannot be empty")
        super().__post_init__()
