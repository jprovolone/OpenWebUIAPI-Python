"""
API module for interacting with the models endpoints.
"""

import logging
from typing import List
from ..models import Model, Action
from ..utils.http import HttpClient

logger = logging.getLogger('OpenWebUI.api.models')

class ModelsAPI:
    """
    API client for model-related endpoints.
    """
    
    def __init__(self, http: HttpClient):
        """
        Initialize the models API client.
        
        Args:
            http: The HTTP client for making requests.
        """
        self.http = http
    
    def get_models(self) -> List[Model]:
        """
        Get all available models.
        
        Returns:
            A list of Model objects.
            
        Raises:
            Exception: If the request fails.
        """
        logger.info("Fetching available models")
        
        try:
            response = self.http.get("models")
            
            data = response.get('data', [])
            models = []
            
            for item in data:
                # Create Action objects for each action
                if 'actions' in item and item['actions']:
                    item['actions'] = [Action.from_dict(action) for action in item.get('actions', [])]
                
                # Create nested objects
                if item.get('pipe'):
                    from ..models import Pipe
                    item['pipe'] = Pipe.from_dict(item['pipe'])
                
                if item.get('openai'):
                    from ..models import OpenAI
                    item['openai'] = OpenAI.from_dict(item['openai'])
                
                if item.get('info'):
                    from ..models import Info
                    item['info'] = Info.from_dict(item['info'])
                
                # Use from_dict instead of constructor to handle unknown fields
                models.append(Model.from_dict(item))
            
            logger.info(f"Successfully retrieved {len(models)} models")
            return models
            
        except Exception as e:
            logger.error(f"Failed to fetch models: {str(e)}")
            raise Exception(f"Failed to fetch models: {str(e)}")
