"""
Tests for the users API module.
"""

import pytest
from unittest.mock import patch, MagicMock
from openwebui_python.api.users import UsersAPI
from openwebui_python.models import User

class TestUsersAPI:
    """
    Tests for the UsersAPI class.
    """
    
    def test_init(self, mock_http_client):
        """Test initialization of the API client."""
        api = UsersAPI(mock_http_client)
        assert api.http == mock_http_client
    
    def test_get_users_success(self, mock_http_client, user_response):
        """Test successful retrieval of users."""
        # Setup mock to return a list of users
        mock_http_client.get.return_value = [user_response]
        
        # Create API client and call method
        api = UsersAPI(mock_http_client)
        users = api.get_users()
        
        # Verify results
        mock_http_client.get.assert_called_once_with("v1/users/")
        assert len(users) == 1
        assert isinstance(users[0], User)
        assert users[0].id == "user1"
        assert users[0].name == "Test User"
        assert users[0].role == "admin"
    
    def test_get_users_error(self, mock_http_client):
        """Test error handling when retrieving users."""
        # Setup mock to raise an exception
        mock_http_client.get.side_effect = Exception("API Error")
        
        # Create API client and call method with exception
        api = UsersAPI(mock_http_client)
        with pytest.raises(Exception, match="Failed to fetch users"):
            api.get_users()
