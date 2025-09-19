"""
Tests for the chat API module.
"""

import pytest
from unittest.mock import patch, MagicMock
from openwebui_python.api.chat import ChatAPI
from openwebui_python.models import ChatCompletion, Message, Choice

class TestChatAPI:
    """
    Tests for the ChatAPI class.
    """
    
    def test_init(self, mock_http_client):
        """Test initialization of the API client."""
        api = ChatAPI(mock_http_client)
        assert api.http == mock_http_client
    
    def test_get_chat_completion_success(self, mock_http_client, chat_completion_response):
        """Test successful retrieval of chat completion."""
        # Setup mock
        mock_http_client.post.return_value = chat_completion_response
        
        # Create API client and call method
        api = ChatAPI(mock_http_client)
        completion = api.get_chat_completion("model1", "test prompt")
        
        # Verify results
        mock_http_client.post.assert_called_once_with(
            "chat/completions", 
            json={
                "model": "model1",
                "messages": [{"role": "user", "content": "test prompt"}]
            }
        )
        
        assert isinstance(completion, ChatCompletion)
        assert completion.id == "chat1"
        assert completion.model == "model1"
        
        # Verify nested objects
        assert isinstance(completion.choices[0], Choice)
        assert isinstance(completion.choices[0].message, Message)
        assert completion.choices[0].message.content == "Test response"
        assert completion.choices[0].message.role == "assistant"
    
    def test_get_chat_completion_validation(self, mock_http_client):
        """Test validation of required parameters."""
        api = ChatAPI(mock_http_client)
        
        with pytest.raises(ValueError, match="model_id cannot be empty"):
            api.get_chat_completion("", "test prompt")
        
        with pytest.raises(ValueError, match="prompt cannot be empty"):
            api.get_chat_completion("model1", "")
    
    def test_get_chat_completion_error(self, mock_http_client):
        """Test error handling when retrieving chat completion."""
        # Setup mock to raise an exception
        mock_http_client.post.side_effect = Exception("API Error")
        
        # Create API client and call method with exception
        api = ChatAPI(mock_http_client)
        with pytest.raises(Exception, match="Failed to get chat completion"):
            api.get_chat_completion("model1", "test prompt")
    
    def test_get_chat_completion_with_messages_success(self, mock_http_client, chat_completion_response):
        """Test successful retrieval of chat completion with messages."""
        # Setup mock
        mock_http_client.post.return_value = chat_completion_response
        
        # Create API client and call method
        api = ChatAPI(mock_http_client)
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "test prompt"}
        ]
        completion = api.get_chat_completion_with_messages("model1", messages)
        
        # Verify results
        mock_http_client.post.assert_called_once_with(
            "chat/completions", 
            json={
                "model": "model1",
                "messages": messages
            }
        )
        
        assert isinstance(completion, ChatCompletion)
        assert completion.id == "chat1"
        assert completion.model == "model1"
    
    def test_get_chat_completion_with_messages_validation(self, mock_http_client):
        """Test validation of required parameters."""
        api = ChatAPI(mock_http_client)
        
        with pytest.raises(ValueError, match="model_id cannot be empty"):
            api.get_chat_completion_with_messages("", [{"role": "user", "content": "test"}])
        
        with pytest.raises(ValueError, match="messages must be a non-empty list"):
            api.get_chat_completion_with_messages("model1", None)
        
        with pytest.raises(ValueError, match="messages must be a non-empty list"):
            api.get_chat_completion_with_messages("model1", "not a list")
        
        with pytest.raises(ValueError, match="messages must be a non-empty list"):
            api.get_chat_completion_with_messages("model1", [])
    
    def test_chat_with_file_success(self, mock_http_client, chat_completion_response):
        """Test successful chat with file."""
        # Setup mock
        mock_http_client.post.return_value = chat_completion_response
        
        # Create API client and call method
        api = ChatAPI(mock_http_client)
        completion = api.chat_with_file("model1", "What's in this file?", "file1")
        
        # Verify results
        mock_http_client.post.assert_called_once_with(
            "chat/completions", 
            json={
                "model": "model1",
                "messages": [{"role": "user", "content": "What's in this file?"}],
                "files": [{"type": "file", "id": "file1"}]
            }
        )
        
        assert isinstance(completion, ChatCompletion)
        assert completion.id == "chat1"
    
    def test_chat_with_file_validation(self, mock_http_client):
        """Test validation of required parameters."""
        api = ChatAPI(mock_http_client)
        
        with pytest.raises(ValueError, match="model cannot be empty"):
            api.chat_with_file("", "query", "file1")
        
        with pytest.raises(ValueError, match="query cannot be empty"):
            api.chat_with_file("model1", "", "file1")
        
        with pytest.raises(ValueError, match="file_id cannot be empty"):
            api.chat_with_file("model1", "query", "")
