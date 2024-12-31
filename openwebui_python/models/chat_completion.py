# models.py

from dataclasses import dataclass, field, asdict, MISSING
from typing import List, Optional, Dict, Any

@dataclass
class Message:
    content: str
    role: str
    refusal: Optional[Any] = None

@dataclass
class Choice:
    index: int
    message: Message
    logprobs: Optional[Dict] = None
    finish_reason: Optional[str] = None

@dataclass
class ChatCompletion:
    choices: List[Choice]
    id: Optional[str] = None
    model: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    usage: Optional[Dict[str, Any]] = None
    system_fingerprint: Optional[str] = None
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, *args, **kwargs):
        # Extract known fields from kwargs
        known_fields = {f.name for f in self.__dataclass_fields__.values() if f.name != 'extra_fields'}
        known_args = {k: kwargs.pop(k) for k in list(kwargs) if k in known_fields}
        
        # Initialize class in typical dataclass fashion
        super().__setattr__('extra_fields', kwargs)  # Any extra fields go here
        
        # Handle known fields
        for field, value in known_args.items():
            super().__setattr__(field, value)
        
        # Manage any defaults not passed explicitly
        for field, field_def in self.__dataclass_fields__.items():
            if field not in known_args and field != 'extra_fields':
                if field_def.default_factory is not MISSING:
                    super().__setattr__(field, field_def.default_factory())
                elif field_def.default is not MISSING:
                    super().__setattr__(field, field_def.default)

    def __post_init__(self):
        # Detect and store unexpected keyword arguments
        defined_fields = {f.name for f in self.__dataclass_fields__.values()}
        all_arguments = self.__dict__.copy()
        extras = {k: v for k, v in all_arguments.items() if k not in defined_fields}
        if extras:
            # Clear existing attributes to prevent duplication
            for extra in extras:
                del self.__dict__[extra]
            self.extra_fields.update(extras)

@dataclass
class ChatWithFile:
    detail: str

@dataclass
class ChatWithCollection:
    id: str
    model: str
    object: str
    created: int
    choices: List[dict]
