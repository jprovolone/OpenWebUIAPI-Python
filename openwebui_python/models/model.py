# model.py

from dataclasses import dataclass, field, MISSING
from typing import List, Optional, Dict, Any

@dataclass
class Pipe:
    type: Optional[str] = None
    name: Optional[str] = None
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
class Architecture:
    instruct_type: Optional[str] = None
    modality: Optional[str] = None
    tokenizer: Optional[str] = None
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
class Pricing:
    completion: Optional[str] = None
    image: Optional[str] = None
    prompt: Optional[str] = None
    request: Optional[str] = None
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
class TopProvider:
    context_length: Optional[int] = None
    is_moderated: Optional[bool] = None
    max_completion_tokens: Optional[int] = None
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
class OpenAI:
    created: Optional[int] = None
    id: Optional[str] = None
    name: Optional[str] = None
    context_length: Optional[int] = None
    architecture: Optional[Architecture] = None
    pricing: Optional[Pricing] = None
    top_provider: Optional[TopProvider] = None
    description: Optional[str] = None
    object: Optional[str] = None
    owned_by: Optional[str] = None
    per_request_limits: Optional[Dict[str, str]] = None
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
class Action:
    description: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    icon_url: Optional[str] = None
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
class AccessControl:
    group_ids: List[str] = field(default_factory=list)
    user_ids: List[str] = field(default_factory=list)
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
class Meta:
    description: Optional[str] = None
    profile_image_url: Optional[str] = None
    model_ids: Optional[List[str]] = None
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
class Info:
    access_control: Optional[AccessControl] = None
    base_model_id: Optional[str] = None
    created_at: Optional[int] = None
    id: Optional[str] = None
    is_active: Optional[bool] = None
    meta: Optional[Meta] = None
    name: Optional[str] = None
    params: Optional[dict] = None
    updated_at: Optional[int] = None
    user_id: Optional[str] = None
    description: Optional[str] = None
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
        defined_fields = {f.name for f in self.__dataclass_fields__.values()}
        all_arguments = self.__dict__.copy()
        extras = {k: v for k, v in all_arguments.items() if k not in defined_fields}
        if extras:
            for extra in extras:
                del self.__dict__[extra]
            self.extra_fields.update(extras)

@dataclass
class Details:
    families: List[str] = field(default_factory=list)
    family: Optional[str] = None
    format: Optional[str] = None
    parameter_size: Optional[str] = None
    parent_model: Optional[str] = None
    quantization_level: Optional[str] = None
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
class Ollama:
    details: Optional[Details] = None
    digest: Optional[str] = None
    model: Optional[str] = None
    modified_at: Optional[str] = None
    name: Optional[str] = None
    size: Optional[int] = None
    urls: List[int] = field(default_factory=list)
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
class Model:
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None
    owned_by: Optional[str] = None
    urlIdx: int = 0
    created: int = 0
    actions: List[Action] = field(default_factory=list)
    arena: bool = False
    pipe: Optional[Pipe] = None
    openai: Optional[OpenAI] = None
    info: Optional[Info] = None
    ollama: Optional[Ollama] = None
    preset: bool = False
    description: Optional[str] = None
    context_length: Optional[int] = None
    architecture: Optional[Architecture] = None
    pricing: Optional[Pricing] = None
    top_provider: Optional[TopProvider] = None
    per_request_limits: Optional[Dict[str, str]] = None
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
