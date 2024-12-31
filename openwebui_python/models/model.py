# model.py

from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class Pipe:
    type: str

@dataclass
class Architecture:
    instruct_type: Optional[str] = None
    modality: Optional[str] = None
    tokenizer: Optional[str] = None

@dataclass
class Pricing:
    completion: Optional[str] = None
    image: Optional[str] = None
    prompt: Optional[str] = None
    request: Optional[str] = None

@dataclass
class TopProvider:
    context_length: Optional[int] = None
    is_moderated: Optional[bool] = None
    max_completion_tokens: Optional[int] = None

@dataclass
class OpenAI:
    created: int
    id: str
    name: Optional[str] = None
    context_length: Optional[int] = None
    architecture: Optional[Architecture] = None
    pricing: Optional[Pricing] = None
    top_provider: Optional[TopProvider] = None
    description: Optional[str] = None
    object: Optional[str] = None
    owned_by: Optional[str] = None
    per_request_limits: Optional[Dict[str, str]] = None

@dataclass
class Action:
    description: str
    id: str
    name: str
    icon_url: Optional[str]

@dataclass
class AccessControl:
    group_ids: List[str]
    user_ids: List[str]

@dataclass
class Meta:
    description: str
    profile_image_url: str
    model_ids: Optional[List[str]]

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

@dataclass
class Details:
    families: List[str]
    family: str
    format: str
    parameter_size: str
    parent_model: str
    quantization_level: str

@dataclass
class Ollama:
    details: Details
    digest: str
    model: str
    modified_at: str
    name: str
    size: int
    urls: List[int]

@dataclass
class Model:
    id: str
    name: str
    object: str
    owned_by: str
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
    description: Optional[str] = None
    object: Optional[str] = None
    owned_by: Optional[str] = None
    per_request_limits: Optional[Dict[str, str]] = None