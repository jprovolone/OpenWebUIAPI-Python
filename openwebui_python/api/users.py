"""
API module for interacting with the users endpoints.
"""

import logging
from typing import List
from ..models import User
from ..utils.http import HttpClient

logger = logging.getLogger('OpenWebUI.api.users')

class UsersAPI:
    """
    API client for user-related endpoints.
    """
    
    def __init__(self, http: HttpClient):
        """
        Initialize the users API client.
        
        Args:
            http: The HTTP client for making requests.
        """
        self.http = http
    
    def get_users(self) -> List[User]:
        """
        Get all users.
        
        Returns:
            A list of User objects.
            
        Raises:
            Exception: If the request fails.
        """
        logger.info("Fetching all users")
        
        try:
            response = self.http.get("v1/users/")
            
            users = []
            for item in response:
                users.append(User(**item))
            
            logger.info(f"Successfully retrieved {len(users)} users")
            return users
            
        except Exception as e:
            logger.error(f"Failed to fetch users: {str(e)}")
            raise Exception(f"Failed to fetch users: {str(e)}")
