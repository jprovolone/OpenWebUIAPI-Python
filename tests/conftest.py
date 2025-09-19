"""
Shared fixtures and configurations for testing the OpenWebUI Python SDK.
"""

import pytest
from unittest.mock import MagicMock, patch
from openwebui_python import OpenWebUI, BaseClient
from openwebui_python.utils.http import HttpClient

@pytest.fixture
def mock_http_client():
    """
    Create a mock HTTP client for testing API interactions.
    """
    client = MagicMock(spec=HttpClient)
    return client

@pytest.fixture
def base_client(mock_http_client):
    """
    Create a BaseClient instance with a mocked HTTP client.
    """
    with patch('openwebui_python.client.HttpClient', return_value=mock_http_client):
        client = BaseClient(base_url="http://test.com", api_key="test-key")
        client.http = mock_http_client
        return client

@pytest.fixture
def client(base_client, mock_http_client):
    """
    Create an OpenWebUI client instance with a mocked HTTP client.
    
    This fixture provides a client instance with all API domains properly mocked.
    """
    with patch('openwebui_python.client.HttpClient', return_value=mock_http_client):
        client = OpenWebUI(base_url="http://test.com", api_key="test-key")
        client.http = mock_http_client
        return client

@pytest.fixture
def model_response():
    """
    Fixture for a standard model response from the API.
    """
    return {
        "data": [{
            "id": "model1",
            "name": "Test Model",
            "actions": [{"name": "test", "id": "action1", "description": "Test action"}],
            "pipe": {"name": "test_pipe", "type": "test"},
            "openai": {"name": "test_openai", "id": "openai1"},
            "info": {"description": "test", "id": "info1"}
        }]
    }

@pytest.fixture
def chat_completion_response():
    """
    Fixture for a standard chat completion response from the API.
    """
    return {
        "id": "chat1",
        "object": "chat.completion",
        "created": 1625097807,
        "model": "model1",
        "choices": [{
            "message": {"role": "assistant", "content": "Test response"},
            "index": 0,
            "finish_reason": "stop"
        }]
    }

@pytest.fixture
def file_response():
    """
    Fixture for a standard file response from the API.
    """
    return {
        "id": "file1",
        "filename": "test.txt",
        "meta": {"type": "text", "size": 100},
        "data": {"content": "test content"}
    }

@pytest.fixture
def knowledge_response():
    """
    Fixture for a standard knowledge response from the API.
    """
    return {
        "id": "knowledge1",
        "name": "Test Knowledge",
        "description": "Test description",
        "files": []
    }

@pytest.fixture
def user_response():
    """
    Fixture for a standard user response from the API.
    """
    return {
        "id": "user1",
        "name": "Test User",
        "role": "admin",
        "created_at": 1625097807
    }

@pytest.fixture
def audio_transcription_response():
    """
    Fixture for a standard audio transcription response from the API.
    """
    return {
        "text": "transcribed text"
    }
