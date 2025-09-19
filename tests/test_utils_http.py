"""
Tests for the HTTP utility module.
"""

import pytest
from unittest.mock import patch, MagicMock
import requests
from openwebui_python.utils.http import HttpClient

class TestHttpClient:
    """
    Tests for the HttpClient class.
    """
    
    def test_init(self):
        """Test initialization of the HTTP client."""
        client = HttpClient("http://test.com", "test-key")
        assert client.base_url == "http://test.com"
        assert client.headers["Authorization"] == "Bearer test-key"
        assert client.headers["Accept"] == "application/json"
    
    def test_init_with_trailing_slash(self):
        """Test initialization with trailing slash in base_url."""
        client = HttpClient("http://test.com/", "test-key")
        assert client.base_url == "http://test.com"
    
    @patch('requests.get')
    def test_get_success(self, mock_get):
        """Test successful GET request."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response
        mock_response.raise_for_status = MagicMock()
        
        # Create client and call method
        client = HttpClient("http://test.com", "test-key")
        result = client.get("endpoint")
        
        # Verify results
        mock_get.assert_called_once_with(
            "http://test.com/endpoint",
            headers=client.headers,
            params=None
        )
        assert result == {"data": "test"}
    
    @patch('requests.get')
    def test_get_with_params(self, mock_get):
        """Test GET request with query parameters."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response
        mock_response.raise_for_status = MagicMock()
        
        # Create client and call method
        client = HttpClient("http://test.com", "test-key")
        result = client.get("endpoint", params={"key": "value"})
        
        # Verify results
        mock_get.assert_called_once_with(
            "http://test.com/endpoint",
            headers=client.headers,
            params={"key": "value"}
        )
        assert result == {"data": "test"}
    
    @patch('requests.get')
    def test_get_error(self, mock_get):
        """Test error handling in GET request."""
        # Setup mock to raise an exception
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        # Create client and call method with exception
        client = HttpClient("http://test.com", "test-key")
        with pytest.raises(Exception, match="Request failed"):
            client.get("endpoint")
    
    @patch('requests.post')
    def test_post_with_json(self, mock_post):
        """Test POST request with JSON payload."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_post.return_value = mock_response
        
        # Create client and call method
        client = HttpClient("http://test.com", "test-key")
        result = client.post("endpoint", json={"key": "value"})
        
        # Verify results
        mock_post.assert_called_once_with(
            "http://test.com/endpoint",
            headers=client.headers,
            json={"key": "value"},
            files=None
        )
        assert result == {"data": "test"}
    
    @patch('requests.post')
    def test_post_with_files(self, mock_post):
        """Test POST request with files."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_post.return_value = mock_response
        
        # Create client and call method
        client = HttpClient("http://test.com", "test-key")
        files = {"file": "test_file"}
        result = client.post("endpoint", files=files)
        
        # Verify results
        mock_post.assert_called_once_with(
            "http://test.com/endpoint",
            headers=client.headers,
            json=None,
            files=files
        )
        assert result == {"data": "test"}
    
    @patch('requests.post')
    def test_post_error(self, mock_post):
        """Test error handling in POST request."""
        # Setup mock to raise an exception
        mock_post.side_effect = requests.exceptions.RequestException("API Error")
        
        # Create client and call method with exception
        client = HttpClient("http://test.com", "test-key")
        with pytest.raises(Exception, match="Request failed"):
            client.post("endpoint", json={"key": "value"})
    
    @patch('requests.delete')
    def test_delete_success(self, mock_delete):
        """Test successful DELETE request."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_delete.return_value = mock_response
        
        # Create client and call method
        client = HttpClient("http://test.com", "test-key")
        result = client.delete("endpoint")
        
        # Verify results
        mock_delete.assert_called_once_with(
            "http://test.com/endpoint",
            headers=client.headers
        )
        assert result == {"data": "test"}
    
    @patch('requests.delete')
    def test_delete_error(self, mock_delete):
        """Test error handling in DELETE request."""
        # Setup mock to raise an exception
        mock_delete.side_effect = requests.exceptions.RequestException("API Error")
        
        # Create client and call method with exception
        client = HttpClient("http://test.com", "test-key")
        with pytest.raises(Exception, match="Request failed"):
            client.delete("endpoint")
    
    def test_url_handling(self):
        """Test URL handling with and without leading slashes."""
        client = HttpClient("http://test.com", "test-key")
        
        with patch('requests.get') as mock_get:
            # Setup mock
            mock_response = MagicMock()
            mock_response.json.return_value = {"data": "test"}
            mock_get.return_value = mock_response
            mock_response.raise_for_status = MagicMock()
            
            # Test with and without leading slash
            client.get("endpoint")
            client.get("/endpoint")
            
            # Verify both calls use the same URL
            assert mock_get.call_args_list[0][0][0] == "http://test.com/endpoint"
            assert mock_get.call_args_list[1][0][0] == "http://test.com/endpoint"
