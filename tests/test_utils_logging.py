"""
Tests for the logging utility module.
"""

import pytest
import logging
import sys
from unittest.mock import patch, MagicMock, call
from openwebui_python.utils.logging import setup_logging

class TestLogging:
    """
    Tests for the logging utility functions.
    """
    
    def test_setup_logging_default(self):
        """Test setup_logging with default parameters."""
        with patch('logging.StreamHandler') as mock_stream_handler, \
             patch('logging.FileHandler') as mock_file_handler, \
             patch('logging.getLogger') as mock_get_logger:
            
            # Setup mocks
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            mock_stream_instance = MagicMock()
            mock_stream_handler.return_value = mock_stream_instance
            
            # Call function
            result = setup_logging()
            
            # Verify results
            mock_get_logger.assert_called_once_with('OpenWebUI')
            mock_logger.setLevel.assert_called_once_with(logging.INFO)
            mock_stream_handler.assert_called_once_with(sys.stdout)
            mock_stream_instance.setLevel.assert_called_once_with(logging.INFO)
            assert mock_file_handler.call_count == 0  # No file handler by default
            assert result == mock_logger
    
    def test_setup_logging_custom_level(self):
        """Test setup_logging with custom level."""
        with patch('logging.StreamHandler') as mock_stream_handler, \
             patch('logging.getLogger') as mock_get_logger:
            
            # Setup mocks
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            mock_stream_instance = MagicMock()
            mock_stream_handler.return_value = mock_stream_instance
            
            # Call function
            result = setup_logging(level=logging.DEBUG)
            
            # Verify results
            mock_logger.setLevel.assert_called_once_with(logging.DEBUG)
            mock_stream_instance.setLevel.assert_called_once_with(logging.DEBUG)
    
    def test_setup_logging_custom_format(self):
        """Test setup_logging with custom format string."""
        with patch('logging.StreamHandler') as mock_stream_handler, \
             patch('logging.Formatter') as mock_formatter, \
             patch('logging.getLogger') as mock_get_logger:
            
            # Setup mocks
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            mock_stream_instance = MagicMock()
            mock_stream_handler.return_value = mock_stream_instance
            mock_formatter_instance = MagicMock()
            mock_formatter.return_value = mock_formatter_instance
            
            # Call function
            custom_format = '%(levelname)s - %(message)s'
            result = setup_logging(format_string=custom_format)
            
            # Verify results
            mock_formatter.assert_called_once_with(custom_format)
            mock_stream_instance.setFormatter.assert_called_once_with(mock_formatter_instance)
    
    def test_setup_logging_with_file(self):
        """Test setup_logging with log file."""
        with patch('logging.StreamHandler') as mock_stream_handler, \
             patch('logging.FileHandler') as mock_file_handler, \
             patch('logging.getLogger') as mock_get_logger:
            
            # Setup mocks
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            mock_stream_instance = MagicMock()
            mock_stream_handler.return_value = mock_stream_instance
            mock_file_instance = MagicMock()
            mock_file_handler.return_value = mock_file_instance
            
            # Call function
            result = setup_logging(log_file='test.log')
            
            # Verify results
            mock_file_handler.assert_called_once_with('test.log')
            mock_file_instance.setLevel.assert_called_once_with(logging.INFO)
            assert mock_logger.addHandler.call_count == 2  # Both stream and file handlers
            mock_logger.addHandler.assert_has_calls([
                call(mock_stream_instance),
                call(mock_file_instance)
            ])
    
    def test_setup_logging_removes_existing_handlers(self):
        """Test that setup_logging removes existing handlers."""
        with patch('logging.StreamHandler') as mock_stream_handler, \
             patch('logging.getLogger') as mock_get_logger:
            
            # Setup mocks
            mock_logger = MagicMock()
            mock_existing_handler = MagicMock()
            mock_logger.handlers = [mock_existing_handler]
            mock_get_logger.return_value = mock_logger
            
            # Call function
            result = setup_logging()
            
            # Verify results
            mock_logger.removeHandler.assert_called_once_with(mock_existing_handler)
