# models.py

from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class Message:
    content: str
    role: str

@dataclass
class Choice:
    finish_reason: str
    index: int
    message: Message
    logprobs: Optional[Dict] = None

@dataclass
class ChatCompletion:
    id: str
    model: str
    object: str
    created: int
    choices: List[Choice]

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
