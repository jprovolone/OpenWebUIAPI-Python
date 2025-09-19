"""
HTTP utilities for making requests to the OpenWebUI API.
"""

import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger('OpenWebUI.http')

class HttpClient:
    """
    A client for making HTTP requests to the OpenWebUI API.
    """
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the HTTP client.
        
        Args:
            base_url: The base URL of the OpenWebUI API.
            api_key: The API key for authentication.
        """
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        logger.debug(f"Initialized HTTP client with base URL: {base_url}")
        
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the API.
        
        Args:
            endpoint: The API endpoint to request.
            params: Optional query parameters.
            
        Returns:
            The response JSON.
            
        Raises:
            Exception: If the request fails.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"Making GET request to {url}")
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"GET request to {url} failed: {str(e)}")
            raise Exception(f"Request failed: {str(e)}")
    
    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a POST request to the API.
        
        Args:
            endpoint: The API endpoint to request.
            json: Optional JSON payload.
            files: Optional files to upload.
            
        Returns:
            The response JSON.
            
        Raises:
            Exception: If the request fails.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"Making POST request to {url}")
        try:
            response = requests.post(url, headers=self.headers, json=json, files=files)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"POST request to {url} failed: {str(e)}")
            raise Exception(f"Request failed: {str(e)}")
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Make a DELETE request to the API.
        
        Args:
            endpoint: The API endpoint to request.
            
        Returns:
            The response JSON.
            
        Raises:
            Exception: If the request fails.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"Making DELETE request to {url}")
        try:
            response = requests.delete(url, headers=self.headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"DELETE request to {url} failed: {str(e)}")
            raise Exception(f"Request failed: {str(e)}")
