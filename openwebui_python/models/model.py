"""
Model-related data models for the OpenWebUI Python SDK.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from .base import BaseModel

@dataclass
class Pipe(BaseModel):
    """
    Represents a model pipe configuration.
    """
    type: Optional[str] = None
    name: Optional[str] = None

@dataclass
class Architecture(BaseModel):
    """
    Represents a model architecture.
    """
    instruct_type: Optional[str] = None
    modality: Optional[str] = None
    tokenizer: Optional[str] = None

@dataclass
class Pricing(BaseModel):
    """
    Represents model pricing information.
    """
    completion: Optional[str] = None
    image: Optional[str] = None
    prompt: Optional[str] = None
    request: Optional[str] = None

@dataclass
class TopProvider(BaseModel):
    """
    Represents top provider information.
    """
    context_length: Optional[int] = None
    is_moderated: Optional[bool] = None
    max_completion_tokens: Optional[int] = None

@dataclass
class AccessControl(BaseModel):
    """
    Represents access control configuration.
    """
    group_ids: List[str] = field(default_factory=list)
    user_ids: List[str] = field(default_factory=list)

@dataclass
class Meta(BaseModel):
    """
    Represents metadata.
    """
    description: Optional[str] = None
    profile_image_url: Optional[str] = None
    model_ids: Optional[List[str]] = None

@dataclass
class Info(BaseModel):
    """
    Represents model information.
    """
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

@dataclass
class Details(BaseModel):
    """
    Represents model details.
    """
    families: List[str] = field(default_factory=list)
    family: Optional[str] = None
    format: Optional[str] = None
    parameter_size: Optional[str] = None
    parent_model: Optional[str] = None
    quantization_level: Optional[str] = None

@dataclass
class Ollama(BaseModel):
    """
    Represents Ollama model information.
    """
    details: Optional[Details] = None
    digest: Optional[str] = None
    model: Optional[str] = None
    modified_at: Optional[str] = None
    name: Optional[str] = None
    size: Optional[int] = None
    urls: List[int] = field(default_factory=list)

@dataclass
class OpenAI(BaseModel):
    """
    Represents OpenAI model information.
    """
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
    openai: Optional[str] = None
    urlIdx: Optional[Any] = None

@dataclass
class Action(BaseModel):
    """
    Represents an available action for a model.
    """
    description: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    icon_url: Optional[str] = None

@dataclass
class Model(BaseModel):
    """
    Represents a model in the OpenWebUI API.
    """
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
