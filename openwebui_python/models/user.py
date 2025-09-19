"""
User-related data models for the OpenWebUI Python SDK.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from .base import BaseModel

@dataclass
class User(BaseModel):
    """
    Represents a user in the OpenWebUI API.
    """
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    profile_image_url: Optional[str] = None
    last_active_at: Optional[int] = None
    updated_at: Optional[int] = None
    created_at: Optional[int] = None
    api_key: Optional[str] = None
    settings: Dict[str, Any] = field(default_factory=dict)
    info: Dict[str, Any] = field(default_factory=dict)
    oauth_sub: Optional[str] = None
