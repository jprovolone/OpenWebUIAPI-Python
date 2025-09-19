"""
Knowledge-related data models for the OpenWebUI Python SDK.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .base import BaseModel
from .file import OpenWebFile
from .user import User

@dataclass
class Knowledge(BaseModel):
    """
    Represents a knowledge item in the OpenWebUI API.
    """
    id: Optional[str] = None
    user_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    files: List[OpenWebFile] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)
    access_control: Dict[str, Any] = field(default_factory=dict)
    user: Optional[User] = None
