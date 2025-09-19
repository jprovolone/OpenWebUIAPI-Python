# OpenWebUI Python SDK

A Python client library for interacting with the OpenWebUI API.

## Installation

```bash
pip install openwebui-python
```

## Quick Start

```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(
    base_url="https://your-openwebui-instance.com",
    api_key="your-api-key"
)

# Get available models
models = client.get_models()
for model in models:
    print(f"Model: {model.name} ({model.id})")

# Get a chat completion
completion = client.get_chat_completion(
    model_id="meta-llama/llama-3.1-405b-instruct:free",
    prompt="What is the capital of France?"
)
print(completion.choices[0].message.content)
```

## Environment Variables

You can use environment variables to avoid hardcoding your API credentials:

```python
# Load API credentials from environment variables
# BASE_URL and OPENWEBUI_API_KEY
client = OpenWebUI()
```

You can also use a `.env` file in your project directory:

```
BASE_URL=https://your-openwebui-instance.com
OPENWEBUI_API_KEY=your-api-key
```

## Architecture Overview

The SDK has been professionally designed with a modular, maintainable architecture:

### Client Structure

```
openwebui_python/
├── __init__.py                 # Package exports
├── client.py                   # Base client and OpenWebUI client
├── api/                        # Domain-specific API modules
│   ├── __init__.py
│   ├── models.py               # Model listing and operations
│   ├── chat.py                 # Chat completion endpoints
│   ├── files.py                # File operations
│   ├── knowledge.py            # Knowledge base operations
│   ├── users.py                # User operations
│   └── audio.py                # Audio transcription
├── models/                     # Data models
│   ├── __init__.py
│   ├── base.py                 # Base model with future-proofing
│   ├── chat.py                 # Chat-related models
│   ├── file.py                 # File-related models
│   ├── knowledge.py            # Knowledge-related models
│   ├── model.py                # AI model-related models
│   ├── user.py                 # User-related models
│   └── error.py                # Error models and exceptions
└── utils/                      # Utility modules
    ├── __init__.py
    ├── http.py                 # HTTP client
    └── logging.py              # Logging setup
```

### Client Classes

- `BaseClient`: Core client with authentication and domain-specific API clients
- `OpenWebUI`: Backward-compatible client that provides direct access to all API methods

### Domain-specific API Modules

Each API domain has its own dedicated module:

- `ModelsAPI`: For interacting with models
- `ChatAPI`: For chat completions
- `FilesAPI`: For file operations
- `KnowledgeAPI`: For knowledge base operations
- `UsersAPI`: For user management
- `AudioAPI`: For audio transcription

You can access these domain-specific clients through the main client:

```python
# Using domain-specific clients
models = client.models.get_models()
chat_completion = client.chat.get_chat_completion(model_id, prompt)
```

### Data Models

All API responses are converted to typed data models for better code completion and type safety:

- Models: `Model`, `Action`, `Pipe`, etc.
- Chat: `ChatCompletion`, `Message`, `Choice`
- Files: `OpenWebFile`, `FileData`, `FileMeta`
- Knowledge: `Knowledge`
- Users: `User`

### Future-Proof Design

The SDK is designed to handle future API changes without breaking:

- All models extend `BaseModel` which automatically stores unknown fields
- When the API adds new fields, the SDK will preserve them in the `extra_fields` property
- All models have a `from_dict` method to handle new fields from API responses
- Models can be serialized back to dictionaries with `to_dict`, including unknown fields

```python
# Example of handling future API changes
data = api_client.get_some_data()  # API returns unknown fields
model = SomeModel.from_dict(data)  # Unknown fields are stored

# Access known fields normally
print(model.id)
print(model.name)

# Access unknown fields through extra_fields
print(model.extra_fields["new_api_field"])

# Serialize back to dict with all fields intact
complete_data = model.to_dict()
```

## Examples

### Chat Completions

```python
# Basic chat completion
completion = client.get_chat_completion(
    model_id="meta-llama/llama-3.1-405b-instruct:free",
    prompt="What is the capital of France?"
)
print(completion.choices[0].message.content)

# Chat completion with messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
completion = client.get_chat_completion_with_messages(
    model_id="meta-llama/llama-3.1-405b-instruct:free",
    messages=messages
)
print(completion.choices[0].message.content)
```

### File Operations

```python
# Upload a file
new_file = client.upload_file("path/to/file.txt")
print(f"Uploaded file: {new_file.id}")

# Get all files
files = client.get_files()
for file in files:
    print(f"{file.id} - {file.filename}")

# Get a specific file
file = client.get_file_by_id("file_id")
print(file.data.content)

# Update file content
response = client.update_file_content_by_id("file_id", "New content")
print(f"Update success: {response.success}")

# Delete a file
response = client.delete_file_by_id("file_id")
print(f"Delete success: {response.success}")
```

### Knowledge Base Operations

```python
# Get all knowledge items
knowledge_items = client.get_knowledge()
for item in knowledge_items:
    print(f"{item.id} - {item.name}")

# Get a specific knowledge item
knowledge = client.get_knowledge_by_id("knowledge_id")
print(f"Knowledge: {knowledge.name}")

# Add a file to a knowledge item
result = client.add_remove_file_to_knowledge("knowledge_id", "file_id", True)
print(f"Added file to knowledge: {result.id}")

# Chat with a file
completion = client.chat_with_file(
    model="meta-llama/llama-3.1-405b-instruct:free",
    query="What is this document about?",
    file_id="file_id"
)
print(completion.choices[0].message.content)
```

### Audio Transcription

```python
# Transcribe an audio file
transcription = client.transcribe_audio("path/to/audio.mp3")
print(transcription)
```

## Advanced Usage

### Using the Logger

```python
from openwebui_python.utils.logging import setup_logging

# Set up logging with custom level and format
logger = setup_logging(
    level="DEBUG",
    format_string="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    log_file="openwebui.log"
)
```

### Direct Domain API Usage

```python
# Initialize a base client
from openwebui_python import BaseClient
client = BaseClient(base_url="https://your-openwebui-instance.com", api_key="your-api-key")

# Use domain-specific APIs directly
models = client.models.get_models()
files = client.files.get_files()
knowledge = client.knowledge.get_knowledge()
```

### Using Model Classes Directly

```python
from openwebui_python.models import Model, Knowledge, OpenWebFile
from openwebui_python.models.base import BaseModel

# Create a model from dictionary data
data = {"id": "123", "name": "Test", "unknown_field": "value"}
model = Model.from_dict(data)

# Access extra fields
print(model.extra_fields["unknown_field"])  # "value"

# Convert back to dictionary
data_dict = model.to_dict()  # Includes all fields, even unknown ones
```

## Testing

The SDK includes comprehensive tests to ensure reliability:

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run all tests
pytest tests/

# Generate coverage report
pytest --cov=openwebui_python tests/
```

## License

This project is licensed under [LICENSE].
