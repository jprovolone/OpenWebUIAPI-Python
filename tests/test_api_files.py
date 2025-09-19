"""
Tests for the files API module.
"""

import os
import pytest
from unittest.mock import patch, MagicMock, mock_open
from openwebui_python.api.files import FilesAPI
from openwebui_python.models import OpenWebFile, FileData, FileMeta, ValidationErrorItem

class TestFilesAPI:
    """
    Tests for the FilesAPI class.
    """
    
    def test_init(self, mock_http_client):
        """Test initialization of the API client."""
        api = FilesAPI(mock_http_client)
        assert api.http == mock_http_client
    
    def test_get_files_success(self, mock_http_client, file_response):
        """Test successful retrieval of files."""
        # Setup mock to return a list of files
        mock_http_client.get.return_value = [file_response]
        
        # Create API client and call method
        api = FilesAPI(mock_http_client)
        files = api.get_files()
        
        # Verify results
        mock_http_client.get.assert_called_once_with("v1/files")
        assert len(files) == 1
        assert isinstance(files[0], OpenWebFile)
        assert files[0].id == "file1"
        assert files[0].filename == "test.txt"
        
        # Verify nested objects
        assert isinstance(files[0].meta, FileMeta)
        assert files[0].meta.type == "text"
        
        assert isinstance(files[0].data, FileData)
        assert files[0].data.content == "test content"
    
    def test_get_files_error(self, mock_http_client):
        """Test error handling when retrieving files."""
        # Setup mock to raise an exception
        mock_http_client.get.side_effect = Exception("API Error")
        
        # Create API client and call method with exception
        api = FilesAPI(mock_http_client)
        with pytest.raises(Exception, match="Failed to fetch files"):
            api.get_files()
    
    def test_get_file_by_id_success(self, mock_http_client, file_response):
        """Test successful retrieval of a file by ID."""
        # Setup mock
        mock_http_client.get.return_value = file_response
        
        # Create API client and call method
        api = FilesAPI(mock_http_client)
        file = api.get_file_by_id("file1")
        
        # Verify results
        mock_http_client.get.assert_called_once_with("v1/files/file1")
        assert isinstance(file, OpenWebFile)
        assert file.id == "file1"
        assert file.filename == "test.txt"
    
    def test_get_file_by_id_validation(self, mock_http_client):
        """Test validation of required parameters."""
        api = FilesAPI(mock_http_client)
        
        with pytest.raises(ValueError, match="id cannot be empty"):
            api.get_file_by_id("")
    
    def test_delete_file_by_id_success(self, mock_http_client):
        """Test successful deletion of a file by ID."""
        # Setup mock
        mock_response = {"id": "file1", "success": True}
        mock_http_client.delete.return_value = mock_response
        
        # Create API client and call method
        api = FilesAPI(mock_http_client)
        result = api.delete_file_by_id("file1")
        
        # Verify results
        mock_http_client.delete.assert_called_once_with("v1/files/file1")
        assert isinstance(result, ValidationErrorItem)
        assert result.success is True
    
    def test_delete_file_by_id_validation(self, mock_http_client):
        """Test validation of required parameters."""
        api = FilesAPI(mock_http_client)
        
        with pytest.raises(ValueError, match="id cannot be empty"):
            api.delete_file_by_id("")
    
    def test_update_file_content_by_id_success(self, mock_http_client):
        """Test successful update of file content."""
        # Setup mock
        mock_response = {"id": "file1", "success": True}
        mock_http_client.post.return_value = mock_response
        
        # Create API client and call method
        api = FilesAPI(mock_http_client)
        result = api.update_file_content_by_id("file1", "updated content")
        
        # Verify results
        mock_http_client.post.assert_called_once_with(
            "v1/files/file1/data/content/update", 
            json={"content": "updated content"}
        )
        assert isinstance(result, ValidationErrorItem)
        assert result.success is True
    
    def test_update_file_content_by_id_validation(self, mock_http_client):
        """Test validation of required parameters."""
        api = FilesAPI(mock_http_client)
        
        with pytest.raises(ValueError, match="id cannot be empty"):
            api.update_file_content_by_id("", "content")
        
        with pytest.raises(ValueError, match="new_content cannot be None"):
            api.update_file_content_by_id("file1", None)
    
    def test_upload_file_success(self, mock_http_client, file_response):
        """Test successful file upload."""
        # Setup mocks
        file_response['success'] = True
        mock_http_client.post.return_value = file_response
        
        # Mock file operations
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data="file content")):
            
            # Create API client and call method
            api = FilesAPI(mock_http_client)
            result = api.upload_file("test.txt")
            
            # Verify results
            assert mock_http_client.post.call_count == 1
            assert isinstance(result, OpenWebFile)
            assert result.id == "file1"
            assert result.filename == "test.txt"
    
    def test_upload_file_validation(self, mock_http_client):
        """Test validation of required parameters."""
        api = FilesAPI(mock_http_client)
        
        with pytest.raises(ValueError, match="file_path cannot be empty"):
            api.upload_file("")
        
        with patch('os.path.exists', return_value=False):
            with pytest.raises(FileNotFoundError, match="File not found"):
                api.upload_file("nonexistent.txt")
