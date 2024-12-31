# knowlegde.py

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .files import OpenWebFile

@dataclass
class User:
    id: str
    name: str
    email: str
    role: str
    profile_image_url: str
    last_active_at: Optional[int]
    updated_at: Optional[int]
    created_at: Optional[int]
    api_key: Optional[str] = None
    settings: Dict[str, Any] = field(default_factory=dict)
    info: Dict[str, Any] = field(default_factory=dict)
    oauth_sub: Optional[str] = None


@dataclass
class Knowledge:
    id: str
    user_id: str
    name: str
    description: str
    created_at: int
    updated_at: int
    files: List[OpenWebFile] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)
    access_control: Dict[str, Any] = field(default_factory=dict)
    user: Optional[User] = None