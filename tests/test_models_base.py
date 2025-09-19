"""
Tests for the base model module.
"""

import pytest
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from openwebui_python.models.base import BaseModel

@dataclass
class TestModel(BaseModel):
    """
    Test model for BaseModel tests.
    """
    id: Optional[str] = None
    name: Optional[str] = None
    value: int = 0
    items: List[str] = field(default_factory=list)

class TestBaseModel:
    """
    Tests for the BaseModel class.
    """
    
    def test_init_with_known_fields(self):
        """Test initialization with known fields."""
        model = TestModel(id="123", name="test", value=42)
        assert model.id == "123"
        assert model.name == "test"
        assert model.value == 42
        assert model.items == []
        assert model.extra_fields == {}
    
    def test_init_with_unknown_fields(self):
        """Test initialization with unknown fields."""
        data = {
            "id": "123", 
            "name": "test", 
            "value": 42,
            "unknown_field": "unknown",
            "another_field": {"key": "value"}
        }
        model = TestModel.from_dict(data)
        assert model.id == "123"
        assert model.name == "test"
        assert model.value == 42
        assert model.items == []
        assert model.extra_fields == {
            "unknown_field": "unknown",
            "another_field": {"key": "value"}
        }
    
    def test_init_with_missing_fields(self):
        """Test initialization with missing fields."""
        model = TestModel(id="123")
        assert model.id == "123"
        assert model.name is None
        assert model.value == 0
        assert model.items == []
        assert model.extra_fields == {}
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        data = {
            "id": "123", 
            "name": "test", 
            "value": 42,
            "unknown_field": "unknown"
        }
        model = TestModel.from_dict(data)
        result = model.to_dict()
        assert result == {
            "id": "123",
            "name": "test",
            "value": 42,
            "items": [],
            "unknown_field": "unknown"
        }
    
    def test_nested_models(self):
        """Test handling of nested models."""
        @dataclass
        class NestedModel(BaseModel):
            nested_id: str = "nested"
            extra_data: Dict[str, Any] = field(default_factory=dict)
        
        # Create nested model with unknown fields
        nested_data = {
            "nested_id": "nested-123",
            "future_field": "future"
        }
        nested_model = NestedModel.from_dict(nested_data)
        
        # Create main model with nested model and unknown fields
        data = {
            "id": "123",
            "name": "test",
            "nested": nested_model,
            "future_api_field": {"key": "value"}
        }
        model = TestModel.from_dict(data)
        
        assert model.id == "123"
        assert model.name == "test"
        assert model.extra_fields["nested"].nested_id == "nested-123"
        assert model.extra_fields["nested"].extra_fields["future_field"] == "future"
        assert model.extra_fields["future_api_field"] == {"key": "value"}
        
        # Test to_dict with nested models
        result = model.to_dict()
        assert result["id"] == "123"
        assert result["future_api_field"] == {"key": "value"}
        
        # The nested model should have been converted to a dict too
        assert "nested" in result
        
        # Check that the nested model was properly converted to a dictionary
        nested_dict = result["nested"].to_dict() if hasattr(result["nested"], "to_dict") else result["nested"]
        assert nested_dict["nested_id"] == "nested-123"
        assert "future_field" in nested_dict
        assert nested_dict["future_field"] == "future"
    
    def test_api_evolution_simulation(self):
        """
        Test that the model can handle API changes over time.
        
        This test simulates how the API might evolve over time, adding new fields
        that our client doesn't know about yet.
        """
        # Initial API response with only known fields
        api_response_v1 = {
            "id": "item-123",
            "name": "Test Item",
            "value": 42
        }
        
        model_v1 = TestModel.from_dict(api_response_v1)
        assert model_v1.id == "item-123"
        assert model_v1.name == "Test Item"
        assert model_v1.value == 42
        assert model_v1.extra_fields == {}
        
        # API adds a new field in v2
        api_response_v2 = {
            "id": "item-123",
            "name": "Test Item",
            "value": 42,
            "created_at": 1625097807  # New field
        }
        
        model_v2 = TestModel.from_dict(api_response_v2)
        assert model_v2.id == "item-123"
        assert model_v2.name == "Test Item"
        assert model_v2.value == 42
        assert model_v2.extra_fields == {"created_at": 1625097807}
        
        # API adds more complex fields in v3
        api_response_v3 = {
            "id": "item-123",
            "name": "Test Item",
            "value": 42,
            "created_at": 1625097807,
            "metadata": {  # New nested field
                "source": "api",
                "version": "3.0"
            },
            "tags": ["new", "feature"]  # New array field
        }
        
        model_v3 = TestModel.from_dict(api_response_v3)
        assert model_v3.id == "item-123"
        assert model_v3.name == "Test Item"
        assert model_v3.value == 42
        assert model_v3.extra_fields["created_at"] == 1625097807
        assert model_v3.extra_fields["metadata"] == {"source": "api", "version": "3.0"}
        assert model_v3.extra_fields["tags"] == ["new", "feature"]
        
        # Conversion to dict should include all fields
        result_v3 = model_v3.to_dict()
        assert result_v3["id"] == "item-123"
        assert result_v3["created_at"] == 1625097807
        assert result_v3["metadata"] == {"source": "api", "version": "3.0"}
        assert result_v3["tags"] == ["new", "feature"]
