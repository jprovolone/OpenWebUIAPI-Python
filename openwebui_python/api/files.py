"""
API module for interacting with the files endpoints.
"""

import os
import logging
from typing import List, Optional
from ..models import OpenWebFile, FileData, FileMeta, ValidationErrorItem
from ..utils.http import HttpClient

logger = logging.getLogger('OpenWebUI.api.files')

class FilesAPI:
    """
    API client for file-related endpoints.
    """
    
    def __init__(self, http: HttpClient):
        """
        Initialize the files API client.
        
        Args:
            http: The HTTP client for making requests.
        """
        self.http = http
    
    def get_files(self) -> List[OpenWebFile]:
        """
        Get all files.
        
        Returns:
            A list of OpenWebFile objects.
            
        Raises:
            Exception: If the request fails.
        """
        logger.info("Fetching all files")
        
        try:
            response = self.http.get("v1/files")
            
            files = []
            for item in response:
                # Process nested objects using from_dict for future-proofing
                if item.get('meta'):
                    item['meta'] = FileMeta.from_dict(item['meta'])
                if item.get('data'):
                    item['data'] = FileData.from_dict(item['data'])
                
                files.append(OpenWebFile.from_dict(item))
            
            logger.info(f"Successfully retrieved {len(files)} files")
            return files
            
        except Exception as e:
            logger.error(f"Failed to fetch files: {str(e)}")
            raise Exception(f"Failed to fetch files: {str(e)}")
    
    def get_file_by_id(self, id: str) -> OpenWebFile:
        """
        Get a single file by ID.
        
        Args:
            id: The ID of the file to retrieve.
            
        Returns:
            An OpenWebFile object.
            
        Raises:
            ValueError: If id is empty.
            Exception: If the request fails.
        """
        if not id:
            raise ValueError("id cannot be empty")
            
        logger.info(f"Fetching file with id: {id}")
        
        try:
            response = self.http.get(f"v1/files/{id}")
            
            # Process nested objects using from_dict for future-proofing
            if response.get('meta'):
                response['meta'] = FileMeta.from_dict(response['meta'])
            if response.get('data'):
                response['data'] = FileData.from_dict(response['data'])
            
            logger.info(f"Successfully retrieved file: {response.get('filename', id)}")
            return OpenWebFile.from_dict(response)
            
        except Exception as e:
            logger.error(f"Failed to fetch file {id}: {str(e)}")
            raise Exception(f"Failed to fetch file {id}: {str(e)}")
    
    def delete_file_by_id(self, id: str) -> ValidationErrorItem:
        """
        Delete a file by ID.
        
        Args:
            id: The ID of the file to delete.
            
        Returns:
            A ValidationErrorItem object with success status.
            
        Raises:
            ValueError: If id is empty.
            Exception: If the request fails.
        """
        if not id:
            raise ValueError("id cannot be empty")
            
        logger.info(f"Deleting file with id: {id}")
        
        try:
            response = self.http.delete(f"v1/files/{id}")
            
            if 'success' not in response:
                response['success'] = True if 'id' in response else False
                
            if not response.get('success'):
                response['message'] = response.get('detail', 'Unknown error occurred')
                logger.warning(f"Failed to delete file {id}: {response['message']}")
            else:
                logger.info(f"Successfully deleted file: {id}")
                
            return ValidationErrorItem.from_dict(response)
            
        except Exception as e:
            logger.error(f"Failed to delete file {id}: {str(e)}")
            raise Exception(f"Failed to delete file {id}: {str(e)}")
    
    def update_file_content_by_id(self, id: str, new_content: str) -> ValidationErrorItem:
        """
        Update file content by ID.
        
        Args:
            id: The ID of the file to update.
            new_content: The new content for the file.
            
        Returns:
            A ValidationErrorItem object with success status.
            
        Raises:
            ValueError: If id is empty or new_content is None.
            Exception: If the request fails.
        """
        if not id:
            raise ValueError("id cannot be empty")
        if new_content is None:  # Allow empty string but not None
            raise ValueError("new_content cannot be None")
            
        logger.info(f"Updating content for file with id: {id}")
        
        try:
            payload = {
                'content': new_content
            }
            
            response = self.http.post(f"v1/files/{id}/data/content/update", json=payload)
            
            if 'success' not in response:
                response['success'] = True if 'id' in response else False
                
            if not response.get('success'):
                response['message'] = response.get('detail', 'Unknown error occurred')
                logger.warning(f"Failed to update file {id}: {response['message']}")
            else:
                logger.info(f"Successfully updated file content: {id}")
                
            return ValidationErrorItem.from_dict(response)
            
        except Exception as e:
            logger.error(f"Failed to update file {id}: {str(e)}")
            raise Exception(f"Failed to update file {id}: {str(e)}")
    
    def upload_file(self, file_path: str) -> OpenWebFile:
        """
        Upload a file.
        
        Args:
            file_path: The path to the file to upload.
            
        Returns:
            An OpenWebFile object if successful, or a ValidationErrorItem if failed.
            
        Raises:
            ValueError: If file_path is empty.
            FileNotFoundError: If the file does not exist.
            Exception: If the request fails.
        """
        if not file_path:
            raise ValueError("file_path cannot be empty")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        logger.info(f"Uploading file: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = self.http.post("v1/files/", files=files)
            
            if 'success' not in response:
                response['success'] = True if 'id' in response else False
                
            if response.get('success'):
                # Process nested objects using from_dict for future-proofing
                if response.get('meta'):
                    response['meta'] = FileMeta.from_dict(response['meta'])
                if response.get('data'):
                    response['data'] = FileData.from_dict(response['data'])
                
                logger.info(f"Successfully uploaded file: {os.path.basename(file_path)}")
                return OpenWebFile.from_dict(response)
            else:
                response['message'] = response.get('detail', 'Unknown error occurred')
                logger.warning(f"Failed to upload file {file_path}: {response['message']}")
                return ValidationErrorItem.from_dict(response)
                
        except Exception as e:
            logger.error(f"Failed to upload file {file_path}: {str(e)}")
            raise Exception(f"Failed to upload file {file_path}: {str(e)}")
