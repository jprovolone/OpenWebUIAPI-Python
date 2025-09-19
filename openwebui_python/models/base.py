"""
Base model classes for the OpenWebUI Python SDK.

This module provides base classes for data models used throughout the SDK.
"""

from dataclasses import dataclass, field, MISSING, fields, is_dataclass
from typing import Dict, Any, Set, Optional, TypeVar, Type, cast, get_type_hints

T = TypeVar('T', bound='BaseModel')

@dataclass
class BaseModel:
    """
    Base model class with common functionality for all models.
    
    This class handles the storage of extra fields that are not explicitly defined
    in the model class, making the SDK more resilient to API changes.
    """
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """
        Process any extra fields provided to the constructor.
        
        This method identifies fields that are not part of the dataclass definition
        and moves them to the extra_fields dictionary.
        """
        # No processing needed as extra fields are handled in from_dict
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model to a dictionary.
        
        Returns:
            A dictionary representation of the model.
        """
        result = {}
        for key, value in self.__dict__.items():
            if key != 'extra_fields':
                if hasattr(value, 'to_dict'):
                    result[key] = value.to_dict()
                else:
                    result[key] = value
        
        # Add any extra fields
        result.update(self.extra_fields)
        
        return result
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Create a model instance from a dictionary.
        
        This method handles unknown fields by storing them in the extra_fields dictionary.
        
        Args:
            data: Dictionary containing model data.
            
        Returns:
            A model instance.
        """
        if not is_dataclass(cls):
            raise TypeError(f"{cls.__name__} must be a dataclass")
        
        # Get the field names defined in the dataclass
        defined_fields = {f.name for f in fields(cls)}
        
        # Separate known and unknown fields
        known_fields = {}
        unknown_fields = {}
        
        for key, value in data.items():
            if key in defined_fields:
                known_fields[key] = value
            else:
                unknown_fields[key] = value
        
        # Create the instance with known fields
        instance = cls(**known_fields)
        
        # Add unknown fields to extra_fields
        instance.extra_fields.update(unknown_fields)
        
        return instance
