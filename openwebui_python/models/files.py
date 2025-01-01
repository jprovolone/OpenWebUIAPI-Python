# files.py

from dataclasses import dataclass, field, MISSING
from typing import List, Optional, Dict, Union, Any

@dataclass
class Meta:
    name: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    collection_name: Optional[str] = None
    type: Optional[str] = None
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
class FileData:
    content: Optional[str] = None
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
class OpenWebFile:
    id: Optional[str] = None
    user_id: Optional[str] = None
    filename: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    data: Optional[FileData] = None
    meta: Optional[Meta] = None
    hash: Optional[List[str]] = field(default_factory=list)
    path: Optional[str] = None
    success: Optional[bool] = False
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
class ValidationErrorItem:
    success: bool = False
    content: Optional[str] = None
    message: Optional[str] = None
    detail: Optional[str] = None
    loc: Optional[Union[str, int]] = None
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        defined_fields = {f.name for f in self.__dataclass_fields__.values()}
        all_arguments = self.__dict__.copy()
        extras = {k: v for k, v in all_arguments.items() if k not in defined_fields}
        if extras:
            for extra in extras:
                del self.__dict__[extra]
            self.extra_fields.update(extras)
