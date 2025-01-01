import pytest
import os
from unittest.mock import patch, MagicMock
from openwebui_python import OpenWebUI
from openwebui_python.models.chat_completion import ChatCompletion, Choice, Message
from openwebui_python.models.model import Model, Action, Pipe, OpenAI, Info
from openwebui_python.models.files import OpenWebFile, Meta, FileData, ValidationErrorItem
from openwebui_python.models.knowledge import Knowledge

@pytest.fixture
def api():
    return OpenWebUI(base_url="http://test.com", api_key="test-key")

def test_init():
    # Test successful initialization
    api = OpenWebUI("http://test.com", "test-key")
    assert api.base_url == "http://test.com"
    assert api.headers["Authorization"] == "Bearer test-key"

    # Test initialization with trailing slash
    api = OpenWebUI("http://test.com/", "test-key")
    assert api.base_url == "http://test.com"

    # Test validation errors
    with pytest.raises(ValueError, match="base_url cannot be empty"):
        OpenWebUI("", "test-key")
    with pytest.raises(ValueError, match="api_key cannot be empty"):
        OpenWebUI("http://test.com", "")

class TestModelMethods:
    @patch('requests.get')
    def test_get_models_success(self, mock_get, api):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [{
                "id": "model1",
                "name": "Test Model",
                "actions": [{"name": "test"}],
                "pipe": {"name": "test_pipe"},
                "openai": {"name": "test_openai"},
                "info": {"description": "test"}
            }]
        }
        mock_get.return_value = mock_response
        mock_response.raise_for_status = MagicMock()

        models = api.get_models()
        assert len(models) == 1
        assert isinstance(models[0], Model)
        assert models[0].id == "model1"
        assert isinstance(models[0].actions[0], Action)
        assert isinstance(models[0].pipe, Pipe)
        assert isinstance(models[0].openai, OpenAI)
        assert isinstance(models[0].info, Info)

    @patch('requests.get')
    def test_get_models_error(self, mock_get, api):
        mock_get.side_effect = Exception("API Error")
        with pytest.raises(Exception, match="Failed to fetch models"):
            api.get_models()

class TestChatMethods:
    @patch('requests.post')
    def test_get_chat_completion_success(self, mock_post, api):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {"role": "assistant", "content": "Test response"},
                "index": 0,
                "finish_reason": "stop"
            }]
        }
        mock_post.return_value = mock_response
        mock_response.raise_for_status = MagicMock()

        completion = api.get_chat_completion("model1", "test prompt")
        assert isinstance(completion, ChatCompletion)
        assert isinstance(completion.choices[0], Choice)
        assert isinstance(completion.choices[0].message, Message)
        assert completion.choices[0].message.content == "Test response"

    def test_get_chat_completion_validation(self, api):
        with pytest.raises(ValueError, match="model_id cannot be empty"):
            api.get_chat_completion("", "test")
        with pytest.raises(ValueError, match="prompt cannot be empty"):
            api.get_chat_completion("model1", "")

    @patch('requests.post')
    def test_get_chat_completion_with_messages_success(self, mock_post, api):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {"role": "assistant", "content": "Test response"},
                "index": 0,
                "finish_reason": "stop"
            }]
        }
        mock_post.return_value = mock_response
        mock_response.raise_for_status = MagicMock()

        messages = [{"role": "user", "content": "test"}]
        completion = api.get_chat_completion_with_messages("model1", messages)
        assert isinstance(completion, ChatCompletion)
        assert completion.choices[0].message.content == "Test response"

    def test_get_chat_completion_with_messages_validation(self, api):
        with pytest.raises(ValueError, match="model_id cannot be empty"):
            api.get_chat_completion_with_messages("", [])
        with pytest.raises(ValueError, match="messages must be a non-empty list"):
            api.get_chat_completion_with_messages("model1", None)
        with pytest.raises(ValueError, match="messages must be a non-empty list"):
            api.get_chat_completion_with_messages("model1", "not a list")

class TestFileMethods:
    @patch('requests.get')
    def test_get_files_success(self, mock_get, api):
        mock_response = MagicMock()
        mock_response.json.return_value = [{
            "id": "file1",
            "filename": "test.txt",
            "meta": {"type": "text"},
            "data": {"content": "test content"}
        }]
        mock_get.return_value = mock_response
        mock_response.raise_for_status = MagicMock()

        files = api.get_files()
        assert len(files) == 1
        assert isinstance(files[0], OpenWebFile)
        assert isinstance(files[0].meta, Meta)
        assert isinstance(files[0].data, FileData)
        assert files[0].id == "file1"

    @patch('requests.get')
    def test_get_file_by_id_success(self, mock_get, api):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "file1",
            "filename": "test.txt",
            "meta": {"type": "text"},
            "data": {"content": "test content"}
        }
        mock_get.return_value = mock_response
        mock_response.raise_for_status = MagicMock()

        file = api.get_file_by_id("file1")
        assert isinstance(file, OpenWebFile)
        assert file.id == "file1"

    def test_get_file_by_id_validation(self, api):
        with pytest.raises(ValueError, match="id cannot be empty"):
            api.get_file_by_id("")

    @patch('requests.delete')
    def test_delete_file_by_id_success(self, mock_delete, api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_delete.return_value = mock_response

        result = api.delete_file_by_id("file1")
        assert isinstance(result, ValidationErrorItem)
        assert result.success is True

    @patch('requests.post')
    def test_update_file_content_success(self, mock_post, api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        result = api.update_file_content_by_id("file1", "new content")
        assert isinstance(result, ValidationErrorItem)
        assert result.success is True

    def test_update_file_content_validation(self, api):
        with pytest.raises(ValueError, match="id cannot be empty"):
            api.update_file_content_by_id("", "content")
        with pytest.raises(ValueError, match="new_content cannot be None"):
            api.update_file_content_by_id("file1", None)

class TestKnowledgeMethods:
    @patch('requests.get')
    def test_get_knowledge_success(self, mock_get, api):
        mock_response = MagicMock()
        mock_response.json.return_value = [{
            "id": "knowledge1",
            "name": "Test Knowledge",
            "description": "Test description",
            "files": []
        }]
        mock_get.return_value = mock_response
        mock_response.raise_for_status = MagicMock()

        knowledge_items = api.get_knowledge()
        assert len(knowledge_items) == 1
        assert isinstance(knowledge_items[0], Knowledge)
        assert knowledge_items[0].id == "knowledge1"

    @patch('requests.get')
    def test_get_knowledge_by_id_success(self, mock_get, api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "knowledge1",
            "name": "Test Knowledge",
            "description": "Test description",
            "files": []
        }
        mock_get.return_value = mock_response

        knowledge = api.get_knowledge_by_id("knowledge1")
        assert isinstance(knowledge, Knowledge)
        assert knowledge.id == "knowledge1"

    def test_get_knowledge_by_id_validation(self, api):
        with pytest.raises(ValueError, match="id cannot be empty"):
            api.get_knowledge_by_id("")

    @patch('requests.post')
    def test_add_remove_file_to_knowledge_success(self, mock_post, api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "knowledge1",
            "name": "Test Knowledge",
            "files": ["file1"]
        }
        mock_post.return_value = mock_response

        # Test adding file
        result = api.add_remove_file_to_knowledge("knowledge1", "file1", True)
        assert isinstance(result, Knowledge)
        assert "file1" in result.files

        # Test removing file
        result = api.add_remove_file_to_knowledge("knowledge1", "file1", False)
        assert isinstance(result, Knowledge)

    def test_add_remove_file_to_knowledge_validation(self, api):
        with pytest.raises(ValueError, match="knowledge_id cannot be empty"):
            api.add_remove_file_to_knowledge("", "file1", True)
        with pytest.raises(ValueError, match="file_id cannot be empty"):
            api.add_remove_file_to_knowledge("knowledge1", "", True)

class TestUserMethods:
    @patch('requests.get')
    def test_get_users_success(self, mock_get, api):
        mock_response = MagicMock()
        mock_response.json.return_value = [{
            "id": "user1",
            "name": "Test User",
            "role": "admin",
            "created_at": "2024-01-01"
        }]
        mock_get.return_value = mock_response
        mock_response.raise_for_status = MagicMock()

        users = api.get_users()
        assert len(users) == 1
        assert users[0].id == "user1"
        assert users[0].name == "Test User"

class TestAudioMethods:
    @patch('requests.post')
    def test_transcribe_audio_success(self, mock_post, api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"text": "transcribed text"}
        mock_post.return_value = mock_response

        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', MagicMock()):
                result = api.transcribe_audio("test.mp3")
                assert result == {"text": "transcribed text"}

    def test_transcribe_audio_validation(self, api):
        with pytest.raises(ValueError, match="audio_file_path cannot be empty"):
            api.transcribe_audio("")
        with pytest.raises(FileNotFoundError):
            api.transcribe_audio("nonexistent.mp3")
