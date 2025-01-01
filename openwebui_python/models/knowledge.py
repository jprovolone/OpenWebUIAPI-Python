# knowlegde.py

from dataclasses import dataclass, field, MISSING
from typing import List, Dict, Any, Optional
from .files import OpenWebFile

@dataclass
class User:
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
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        defined_fields = {f.name for f in self.__dataclass_fields__.values()}
        all_arguments = self.__dict__.copy()
        extras = {k: v for k, v in all_arguments.items() if k not in defined_fields}
        if extras:
            for extra in extras:
                del self.__dict__[extra]
            self.extra_fields.update(extras)

@dataclass
class Knowledge:
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
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        defined_fields = {f.name for f in self.__dataclass_fields__.values()}
        all_arguments = self.__dict__.copy()
        extras = {k: v for k, v in all_arguments.items() if k not in defined_fields}
        if extras:
            for extra in extras:
                del self.__dict__[extra]
            self.extra_fields.update(extras)
