"""
Tests for the client module.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from openwebui_python import OpenWebUI, BaseClient
from openwebui_python.utils.http import HttpClient

class TestBaseClient:
    """
    Tests for the BaseClient class.
    """
    
    def test_init_with_params(self):
        """Test initialization with explicit parameters."""
        client = BaseClient(base_url="http://test.com", api_key="test-key")
        assert client.base_url == "http://test.com"
        assert client.api_key == "test-key"
        assert isinstance(client.http, HttpClient)
        
        # Test that domains are initialized
        assert client.models is not None
        assert client.chat is not None
        assert client.files is not None
        assert client.knowledge is not None
        assert client.users is not None
        assert client.audio is not None
    
    def test_init_with_trailing_slash(self):
        """Test initialization with trailing slash in base_url."""
        client = BaseClient(base_url="http://test.com/", api_key="test-key")
        assert client.base_url == "http://test.com"
    
    @patch.dict(os.environ, {"BASE_URL": "http://env-test.com", "OPENWEBUI_API_KEY": "env-test-key"})
    def test_init_from_env(self):
        """Test initialization from environment variables."""
        client = BaseClient()
        assert client.base_url == "http://env-test.com"
        assert client.api_key == "env-test-key"
    
    def test_init_validation(self):
        """Test validation of required parameters."""
        # Mock environment to remove any default values
        with patch.dict(os.environ, {"BASE_URL": "", "OPENWEBUI_API_KEY": ""}, clear=True):
            with pytest.raises(ValueError, match="base_url must be provided"):
                BaseClient(base_url="", api_key="test-key")
            
            with pytest.raises(ValueError, match="api_key must be provided"):
                BaseClient(base_url="http://test.com", api_key="")


class TestOpenWebUI:
    """
    Tests for the OpenWebUI class.
    """
    
    def test_init(self):
        """Test initialization and inheritance."""
        client = OpenWebUI(base_url="http://test.com", api_key="test-key")
        assert isinstance(client, BaseClient)
        assert client.base_url == "http://test.com"
        assert client.api_key == "test-key"
    
    def test_compatibility_methods(self, client, mock_http_client, model_response):
        """Test that compatibility methods call the correct API domain methods."""
        # Setup mock
        mock_http_client.get.return_value = model_response
        
        # Test get_models()
        with patch.object(client.models, 'get_models', return_value=["model1"]) as mock_get_models:
            result = client.get_models()
            mock_get_models.assert_called_once()
            assert result == ["model1"]
