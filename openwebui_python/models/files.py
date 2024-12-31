# files.py

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union

@dataclass
class Meta:
    name: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    collection_name: Optional[str] = None

@dataclass
class FileData:
    content: Optional[str] = None

@dataclass
class OpenWebFile:
    id: str
    user_id: str
    filename: str
    created_at: int
    updated_at: int
    data: Optional[FileData] = None
    meta: Optional[Meta] = None
    hash: Optional[List[str]] = None
    path: Optional[str] = None
    success: Optional[bool] = False

@dataclass
class ValidationErrorItem:
    success: bool
    content: str = None
    message: str = None
    detail: Optional[str] = None
    loc: Optional[Union[str, int]] = None

