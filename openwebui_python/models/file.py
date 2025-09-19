"""
File-related data models for the OpenWebUI Python SDK.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union, Any
from .base import BaseModel

@dataclass
class FileMeta(BaseModel):
    """
    Represents metadata for a file.
    """
    name: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    collection_name: Optional[str] = None
    type: Optional[str] = None

@dataclass
class FileData(BaseModel):
    """
    Represents file data.
    """
    content: Optional[str] = None

@dataclass
class OpenWebFile(BaseModel):
    """
    Represents a file in the OpenWebUI API.
    """
    id: Optional[str] = None
    user_id: Optional[str] = None
    filename: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    data: Optional[FileData] = None
    meta: Optional[FileMeta] = None
    hash: Optional[List[str]] = field(default_factory=list)
    path: Optional[str] = None
    success: Optional[bool] = False
