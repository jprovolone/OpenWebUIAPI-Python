"""
API module for interacting with the chat endpoints.
"""

import logging
from typing import List, Dict, Any, Optional
from ..models import ChatCompletion, Message, Choice
from ..utils.http import HttpClient

logger = logging.getLogger('OpenWebUI.api.chat')

class ChatAPI:
    """
    API client for chat-related endpoints.
    """
    
    def __init__(self, http: HttpClient):
        """
        Initialize the chat API client.
        
        Args:
            http: The HTTP client for making requests.
        """
        self.http = http
    
    def get_chat_completion(self, model_id: str, prompt: str) -> ChatCompletion:
        """
        Get a basic chat completion from the API.
        
        Args:
            model_id: The ID of the model to use.
            prompt: The prompt to send to the model.
            
        Returns:
            A ChatCompletion object.
            
        Raises:
            ValueError: If model_id or prompt is empty.
            Exception: If the request fails.
        """
        if not model_id:
            raise ValueError("model_id cannot be empty")
        if not prompt:
            raise ValueError("prompt cannot be empty")
            
        logger.info(f"Requesting chat completion for model: {model_id}")
        
        try:
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = self.http.post("chat/completions", json=payload)
            
            # Process response data
            data = response
            choices = []
            for item in data.get('choices', []):
                # Use from_dict to handle unknown fields
                if 'message' in item:
                    item['message'] = Message.from_dict(item['message'])
                choices.append(Choice.from_dict(item))
            data['choices'] = choices
            
            logger.info("Successfully received chat completion")
            return ChatCompletion.from_dict(data)
            
        except Exception as e:
            logger.error(f"Failed to get chat completion: {str(e)}")
            raise Exception(f"Failed to get chat completion: {str(e)}")
    
    def get_chat_completion_with_messages(self, model_id: str, messages: List[Dict[str, Any]]) -> ChatCompletion:
        """
        Get a chat completion using a list of messages.
        
        Args:
            model_id: The ID of the model to use.
            messages: A list of message objects, each with 'role' and 'content'.
            
        Returns:
            A ChatCompletion object.
            
        Raises:
            ValueError: If model_id is empty or messages is not a valid list.
            Exception: If the request fails.
        """
        if not model_id:
            raise ValueError("model_id cannot be empty")
        if not messages or not isinstance(messages, list):
            raise ValueError("messages must be a non-empty list")
            
        logger.info(f"Requesting chat completion with messages for model: {model_id}")
        
        try:
            payload = {
                "model": model_id,
                "messages": messages
            }
            
            response = self.http.post("chat/completions", json=payload)
            
            # Process response data
            data = response
            choices = []
            for item in data.get('choices', []):
                # Use from_dict to handle unknown fields
                if 'message' in item:
                    item['message'] = Message.from_dict(item['message'])
                choices.append(Choice.from_dict(item))
            data['choices'] = choices
            
            logger.info("Successfully received chat completion with messages")
            return ChatCompletion.from_dict(data)
            
        except Exception as e:
            logger.error(f"Failed to get chat completion with messages: {str(e)}")
            raise Exception(f"Failed to get chat completion with messages: {str(e)}")
    
    def chat_with_file(self, model: str, query: str, file_id: str) -> ChatCompletion:
        """
        Chat with or about a specific file.
        
        Args:
            model: The ID of the model to use.
            query: The query to send about the file.
            file_id: The ID of the file to chat about.
            
        Returns:
            A ChatCompletion object.
            
        Raises:
            ValueError: If any required parameter is empty.
            Exception: If the request fails.
        """
        if not model:
            raise ValueError("model cannot be empty")
        if not query:
            raise ValueError("query cannot be empty")
        if not file_id:
            raise ValueError("file_id cannot be empty")
            
        logger.info(f"Requesting chat completion with file {file_id}")
        
        try:
            payload = {
                'model': model,
                'messages': [{'role': 'user', 'content': query}],
                'files': [{'type': 'file', 'id': file_id}]
            }
            
            response = self.http.post("chat/completions", json=payload)
            
            # Process response data
            data = response
            choices = []
            for item in data.get('choices', []):
                # Use from_dict to handle unknown fields
                if 'message' in item:
                    item['message'] = Message.from_dict(item['message'])
                choices.append(Choice.from_dict(item))
            data['choices'] = choices
            
            logger.info("Successfully received chat completion with file")
            return ChatCompletion.from_dict(data)
            
        except Exception as e:
            logger.error(f"Failed to get chat completion with file: {str(e)}")
            raise Exception(f"Failed to get chat completion with file: {str(e)}")
