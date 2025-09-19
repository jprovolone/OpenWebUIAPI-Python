"""
Tests for the knowledge API module.
"""

import pytest
from unittest.mock import patch, MagicMock
from openwebui_python.api.knowledge import KnowledgeAPI
from openwebui_python.models import Knowledge, ValidationErrorItem

class TestKnowledgeAPI:
    """
    Tests for the KnowledgeAPI class.
    """
    
    def test_init(self, mock_http_client):
        """Test initialization of the API client."""
        api = KnowledgeAPI(mock_http_client)
        assert api.http == mock_http_client
    
    def test_get_knowledge_success(self, mock_http_client, knowledge_response):
        """Test successful retrieval of knowledge items."""
        # Setup mock to return a list of knowledge items
        mock_http_client.get.return_value = [knowledge_response]
        
        # Create API client and call method
        api = KnowledgeAPI(mock_http_client)
        knowledge_items = api.get_knowledge()
        
        # Verify results
        mock_http_client.get.assert_called_once_with("v1/knowledge")
        assert len(knowledge_items) == 1
        assert isinstance(knowledge_items[0], Knowledge)
        assert knowledge_items[0].id == "knowledge1"
        assert knowledge_items[0].name == "Test Knowledge"
        assert knowledge_items[0].description == "Test description"
    
    def test_get_knowledge_error(self, mock_http_client):
        """Test error handling when retrieving knowledge items."""
        # Setup mock to raise an exception
        mock_http_client.get.side_effect = Exception("API Error")
        
        # Create API client and call method with exception
        api = KnowledgeAPI(mock_http_client)
        with pytest.raises(Exception, match="Failed to fetch knowledge items"):
            api.get_knowledge()
    
    def test_get_knowledge_by_id_success(self, mock_http_client, knowledge_response):
        """Test successful retrieval of a knowledge item by ID."""
        # Setup mock
        mock_http_client.get.return_value = knowledge_response
        
        # Create API client and call method
        api = KnowledgeAPI(mock_http_client)
        knowledge = api.get_knowledge_by_id("knowledge1")
        
        # Verify results
        mock_http_client.get.assert_called_once_with("v1/knowledge/knowledge1")
        assert isinstance(knowledge, Knowledge)
        assert knowledge.id == "knowledge1"
        assert knowledge.name == "Test Knowledge"
    
    def test_get_knowledge_by_id_failure(self, mock_http_client):
        """Test handling of failed retrieval of a knowledge item."""
        # Setup mock to return an error response
        mock_http_client.get.return_value = {"detail": "Knowledge not found"}
        
        # Create API client and call method
        api = KnowledgeAPI(mock_http_client)
        result = api.get_knowledge_by_id("nonexistent")
        
        # Verify results
        assert isinstance(result, ValidationErrorItem)
        assert result.success is False
        assert result.detail == "Knowledge not found"
    
    def test_get_knowledge_by_id_validation(self, mock_http_client):
        """Test validation of required parameters."""
        api = KnowledgeAPI(mock_http_client)
        
        with pytest.raises(ValueError, match="id cannot be empty"):
            api.get_knowledge_by_id("")
    
    def test_add_file_to_knowledge_success(self, mock_http_client, knowledge_response):
        """Test successful addition of a file to a knowledge item."""
        # Setup mock
        mock_http_client.post.return_value = knowledge_response
        
        # Create API client and call method
        api = KnowledgeAPI(mock_http_client)
        result = api.add_file_to_knowledge("knowledge1", "file1")
        
        # Verify results
        mock_http_client.post.assert_called_once_with(
            "v1/knowledge/knowledge1/file/add", 
            json={"file_id": "file1"}
        )
        assert isinstance(result, Knowledge)
        assert result.id == "knowledge1"
    
    def test_remove_file_from_knowledge_success(self, mock_http_client, knowledge_response):
        """Test successful removal of a file from a knowledge item."""
        # Setup mock
        mock_http_client.post.return_value = knowledge_response
        
        # Create API client and call method
        api = KnowledgeAPI(mock_http_client)
        result = api.remove_file_from_knowledge("knowledge1", "file1")
        
        # Verify results
        mock_http_client.post.assert_called_once_with(
            "v1/knowledge/knowledge1/file/remove", 
            json={"file_id": "file1"}
        )
        assert isinstance(result, Knowledge)
        assert result.id == "knowledge1"
    
    def test_add_remove_file_validation(self, mock_http_client):
        """Test validation of required parameters for add/remove file methods."""
        api = KnowledgeAPI(mock_http_client)
        
        with pytest.raises(ValueError, match="knowledge_id cannot be empty"):
            api._add_remove_file_to_knowledge("", "file1", True)
        
        with pytest.raises(ValueError, match="file_id cannot be empty"):
            api._add_remove_file_to_knowledge("knowledge1", "", True)
    
    def test_add_remove_file_error(self, mock_http_client):
        """Test error handling when adding/removing a file to/from a knowledge item."""
        # Setup mock to raise an exception
        mock_http_client.post.side_effect = Exception("API Error")
        
        # Create API client and call method with exception
        api = KnowledgeAPI(mock_http_client)
        with pytest.raises(Exception, match="Failed to add file"):
            api.add_file_to_knowledge("knowledge1", "file1")
