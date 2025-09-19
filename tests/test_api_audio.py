"""
Tests for the audio API module.
"""

import os
import pytest
from unittest.mock import patch, MagicMock, mock_open
from openwebui_python.api.audio import AudioAPI

class TestAudioAPI:
    """
    Tests for the AudioAPI class.
    """
    
    def test_init(self, mock_http_client):
        """Test initialization of the API client."""
        api = AudioAPI(mock_http_client)
        assert api.http == mock_http_client
    
    def test_transcribe_audio_success(self, mock_http_client, audio_transcription_response):
        """Test successful transcription of audio file."""
        # Setup mock
        mock_http_client.post.return_value = audio_transcription_response
        
        # Mock file operations
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data="audio content")):
            
            # Create API client and call method
            api = AudioAPI(mock_http_client)
            result = api.transcribe_audio("test.mp3")
            
            # Verify results
            assert mock_http_client.post.call_count == 1
            assert mock_http_client.post.call_args[0][0] == "audio/api/v1/transcriptions"
            assert "files" in mock_http_client.post.call_args[1]
            assert result == audio_transcription_response
            assert result["text"] == "transcribed text"
    
    def test_transcribe_audio_validation(self, mock_http_client):
        """Test validation of required parameters."""
        api = AudioAPI(mock_http_client)
        
        with pytest.raises(ValueError, match="audio_file_path cannot be empty"):
            api.transcribe_audio("")
        
        with patch('os.path.exists', return_value=False):
            with pytest.raises(FileNotFoundError, match="Audio file not found"):
                api.transcribe_audio("nonexistent.mp3")
    
    def test_transcribe_audio_error(self, mock_http_client):
        """Test error handling when transcribing audio."""
        # Setup mock to raise an exception
        mock_http_client.post.side_effect = Exception("API Error")
        
        # Mock file operations
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data="audio content")):
            
            # Create API client and call method with exception
            api = AudioAPI(mock_http_client)
            with pytest.raises(Exception, match="Failed to transcribe audio file"):
                api.transcribe_audio("test.mp3")
