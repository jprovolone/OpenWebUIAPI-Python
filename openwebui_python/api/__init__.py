"""
API modules for interacting with the OpenWebUI API endpoints.

This package contains modules for each API domain offered by OpenWebUI.
"""

from .models import ModelsAPI
from .chat import ChatAPI
from .files import FilesAPI
from .knowledge import KnowledgeAPI
from .users import UsersAPI
from .audio import AudioAPI

__all__ = [
    'ModelsAPI',
    'ChatAPI',
    'FilesAPI',
    'KnowledgeAPI',
    'UsersAPI',
    'AudioAPI',
]
