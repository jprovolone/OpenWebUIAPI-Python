"""
API module for interacting with the audio endpoints.
"""

import os
import logging
from typing import Dict, Any
from ..utils.http import HttpClient

logger = logging.getLogger('OpenWebUI.api.audio')

class AudioAPI:
    """
    API client for audio-related endpoints.
    """
    
    def __init__(self, http: HttpClient):
        """
        Initialize the audio API client.
        
        Args:
            http: The HTTP client for making requests.
        """
        self.http = http
    
    def transcribe_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe an audio file.
        
        Args:
            audio_file_path: The path to the audio file to transcribe.
            
        Returns:
            A dictionary containing the transcription results.
            
        Raises:
            ValueError: If audio_file_path is empty.
            FileNotFoundError: If the audio file does not exist.
            Exception: If the request fails.
        """
        if not audio_file_path:
            raise ValueError("audio_file_path cannot be empty")
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
        logger.info(f"Transcribing audio file: {audio_file_path}")
        
        try:
            with open(audio_file_path, 'rb') as f:
                files = {'file': f}
                response = self.http.post("audio/api/v1/transcriptions", files=files)
                
            logger.info("Successfully transcribed audio file")
            return response
            
        except Exception as e:
            logger.error(f"Failed to transcribe audio file: {str(e)}")
            raise Exception(f"Failed to transcribe audio file: {str(e)}")
