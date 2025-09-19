"""
Tests for the models API module.
"""

import pytest
from unittest.mock import patch, MagicMock
from openwebui_python.api.models import ModelsAPI
from openwebui_python.models import Model, Action, Pipe, OpenAI, Info

class TestModelsAPI:
    """
    Tests for the ModelsAPI class.
    """
    
    def test_init(self, mock_http_client):
        """Test initialization of the API client."""
        api = ModelsAPI(mock_http_client)
        assert api.http == mock_http_client
    
    def test_get_models_success(self, mock_http_client, model_response):
        """Test successful retrieval of models."""
        # Setup mock
        mock_http_client.get.return_value = model_response
        
        # Create API client and call method
        api = ModelsAPI(mock_http_client)
        models = api.get_models()
        
        # Verify results
        mock_http_client.get.assert_called_once_with("models")
        assert len(models) == 1
        assert isinstance(models[0], Model)
        assert models[0].id == "model1"
        assert models[0].name == "Test Model"
        
        # Verify nested objects
        assert isinstance(models[0].actions[0], Action)
        assert models[0].actions[0].name == "test"
        assert models[0].actions[0].id == "action1"
        
        assert isinstance(models[0].pipe, Pipe)
        assert models[0].pipe.name == "test_pipe"
        
        assert isinstance(models[0].openai, OpenAI)
        assert models[0].openai.name == "test_openai"
        
        assert isinstance(models[0].info, Info)
        assert models[0].info.description == "test"
    
    def test_get_models_error(self, mock_http_client):
        """Test error handling when retrieving models."""
        # Setup mock to raise an exception
        mock_http_client.get.side_effect = Exception("API Error")
        
        # Create API client and call method with exception
        api = ModelsAPI(mock_http_client)
        with pytest.raises(Exception, match="Failed to fetch models"):
            api.get_models()
        
        mock_http_client.get.assert_called_once_with("models")
