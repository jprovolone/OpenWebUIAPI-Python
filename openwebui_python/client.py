"""
Base client for the OpenWebUI Python SDK.

This module provides the base client functionality for interacting with the OpenWebUI API.
"""

import os
import logging
from dotenv import load_dotenv
from .utils.http import HttpClient
from .utils.logging import setup_logging
from .api.models import ModelsAPI
from .api.chat import ChatAPI
from .api.files import FilesAPI
from .api.knowledge import KnowledgeAPI
from .api.users import UsersAPI
from .api.audio import AudioAPI

logger = logging.getLogger('OpenWebUI.client')

class BaseClient:
    """
    Base client for interacting with the OpenWebUI API.
    
    This class provides the core functionality for API authentication and request handling.
    It is used as the foundation for the domain-specific API clients.
    """
    
    def __init__(self, base_url: str = None, api_key: str = None):
        """
        Initialize the OpenWebUI client.
        
        Args:
            base_url: The base URL of the OpenWebUI API. If not provided, it will be loaded
                      from the BASE_URL environment variable.
            api_key: The API key for authentication. If not provided, it will be loaded
                     from the OPENWEBUI_API_KEY environment variable.
                     
        Raises:
            ValueError: If base_url or api_key is not provided and cannot be loaded
                       from environment variables.
        """
        # Load environment variables from .env file if present
        load_dotenv()
        
        # Use provided values or fall back to environment variables
        self.base_url = base_url or os.getenv('BASE_URL')
        self.api_key = api_key or os.getenv('OPENWEBUI_API_KEY')
        
        # Validate required parameters
        if not self.base_url:
            raise ValueError("base_url must be provided")
        if not self.api_key:
            raise ValueError("api_key must be provided or set as OPENWEBUI_API_KEY environment variable")
        
        # Remove trailing slash if present in base_url
        self.base_url = self.base_url.rstrip('/')
        
        # Initialize HTTP client
        self.http = HttpClient(self.base_url, self.api_key)
        logger.info(f"Initialized OpenWebUI client with base URL: {self.base_url}")
        
        # Initialize API clients
        self.models = ModelsAPI(self.http)
        self.chat = ChatAPI(self.http)
        self.files = FilesAPI(self.http)
        self.knowledge = KnowledgeAPI(self.http)
        self.users = UsersAPI(self.http)
        self.audio = AudioAPI(self.http)

class OpenWebUI(BaseClient):
    """
    Main client for the OpenWebUI API.
    
    This class provides backward compatibility with the original client
    by exposing methods from the domain-specific API clients directly.
    """
    
    def __init__(self, base_url: str = None, api_key: str = None):
        """
        Initialize the OpenWebUI client.
        
        Args:
            base_url: The base URL of the OpenWebUI API. If not provided, it will be loaded
                     from the BASE_URL environment variable.
            api_key: The API key for authentication. If not provided, it will be loaded
                     from the OPENWEBUI_API_KEY environment variable.
        """
        super().__init__(base_url, api_key)
        logger.info("Initialized OpenWebUI compatibility client")
    
    #region MODEL METHODS
    def get_models(self):
        """
        Gets all of the available models.
        
        Returns:
            A list of Model objects.
        """
        return self.models.get_models()
    #endregion
    
    #region CHAT METHODS
    def get_chat_completion(self, model_id, prompt):
        """
        Gets a basic chat completion from openwebui provided a model_id and prompt.
        
        Args:
            model_id: The ID of the model to use.
            prompt: The prompt to send to the model.
            
        Returns:
            A ChatCompletion object.
        """
        return self.chat.get_chat_completion(model_id, prompt)
    
    def get_chat_completion_with_messages(self, model_id, messages):
        """
        Get a chat completion using a list of messages.
        
        Args:
            model_id: The ID of the model to use.
            messages: A list of message objects, each with 'role' and 'content'.
            
        Returns:
            A ChatCompletion object.
        """
        return self.chat.get_chat_completion_with_messages(model_id, messages)
    
    def chat_with_file(self, model, query, file_id):
        """
        Chat with or about a specific file. Must upload a file or have a file id first.
        
        Args:
            model: The ID of the model to use.
            query: The query to send about the file.
            file_id: The ID of the file to chat about.
            
        Returns:
            A ChatCompletion object.
        """
        return self.chat.chat_with_file(model, query, file_id)
    #endregion
    
    #region FILE METHODS
    def get_files(self):
        """
        Get all of the files.
        
        Returns:
            A list of OpenWebFile objects.
        """
        return self.files.get_files()
    
    def get_file_by_id(self, id):
        """
        Get a single file by id.
        
        Args:
            id: The ID of the file to retrieve.
            
        Returns:
            An OpenWebFile object.
        """
        return self.files.get_file_by_id(id)
    
    def delete_file_by_id(self, id):
        """
        Delete a single file by id.
        
        Args:
            id: The ID of the file to delete.
            
        Returns:
            A ValidationErrorItem object with success status.
        """
        return self.files.delete_file_by_id(id)
    
    def update_file_content_by_id(self, id, new_content):
        """
        Update file content by id.
        
        Args:
            id: The ID of the file to update.
            new_content: The new content for the file.
            
        Returns:
            A ValidationErrorItem object with success status.
        """
        return self.files.update_file_content_by_id(id, new_content)
    
    def upload_file(self, file_path):
        """
        Upload a file.
        
        Args:
            file_path: The path to the file to upload.
            
        Returns:
            An OpenWebFile object if successful, or a ValidationErrorItem if failed.
        """
        return self.files.upload_file(file_path)
    #endregion
    
    #region KNOWLEDGE METHODS
    def get_knowledge(self):
        """
        Get all knowledge items.
        
        Returns:
            A list of Knowledge objects.
        """
        return self.knowledge.get_knowledge()
    
    def get_knowledge_by_id(self, id):
        """
        Get a single knowledge item by id.
        
        Args:
            id: The ID of the knowledge item to retrieve.
            
        Returns:
            A Knowledge object if successful, or a ValidationErrorItem if failed.
        """
        return self.knowledge.get_knowledge_by_id(id)
    
    def add_remove_file_to_knowledge(self, knowledge_id, file_id, addRemove):
        """
        Add or remove a file to a knowledge item.
        
        Args:
            knowledge_id: The ID of the knowledge item.
            file_id: The ID of the file to add/remove.
            addRemove: True to add, False to remove.
            
        Returns:
            A Knowledge object if successful, or a ValidationErrorItem if failed.
        """
        if addRemove:
            return self.knowledge.add_file_to_knowledge(knowledge_id, file_id)
        else:
            return self.knowledge.remove_file_from_knowledge(knowledge_id, file_id)
    #endregion
    
    #region USER METHODS
    def get_users(self):
        """
        Get all users.
        
        Returns:
            A list of User objects.
        """
        return self.users.get_users()
    #endregion
    
    #region AUDIO METHODS
    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file.
        
        Args:
            audio_file_path: The path to the audio file to transcribe.
            
        Returns:
            A dictionary containing the transcription results.
        """
        return self.audio.transcribe_audio(audio_file_path)
    #endregion
