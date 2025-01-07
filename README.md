# OpenWebUI API Python Client

An unofficial python client for interacting with OpenWebUI's API, providing easy access to language models and chat completions.

## Features

- **Model Management**
  - Get available models with detailed information
  - Support for multiple model types (OpenAI, Ollama)
  - Model metadata and configuration access
  - Access control settings

- **Chat Capabilities**
  - Create chat completions using specified models
  - Support for chat with file attachments
  - Collection-based chat interactions
  - Structured message handling

- **File Operations**
  - Upload and manage files
  - File metadata handling
  - File content updates
  - Validation and error handling

- **Knowledge Management**
  - List and retrieve knowledge collections
  - Add/remove files to knowledge bases
  - User management and access control

- **Type Safety**
  - Structured data classes for better code organization
  - Validation error handling
  - Strong typing for API responses

## Installation

1. Clone the repository
2. Install dependencies 
```
pip install requirements -r requirements.txt
```
3. Set up your environment variables below

## Environment Setup

1. Copy the ```.envexample``` file to a new file:
```
cp .envexample .env
```
2. Set the correct values:
```
BASE_URL=http://your-openwebui-instance:port/api # ‼️ Be sure to include the /api in the BASE_URL!
OPENWEBUI_API_KEY=your_api_key_here
```
---
## Usage

### Get all models
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Get available models
models = client.get_models()
for model in models:
    print(model.id)
```

### Chat Completion
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Create a chat completion
response = client.get_chat_completion(
    model_id="llama3.2:latest", # Use model id here, not the name
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
        ]
    )
print(response.choices[0].message.content)
```

### Chat Completion (with files)
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Create a chat completion
completion = client.chat_with_file('llama3.2:latest', "What is this document?", "SOME_FILE_ID")
print(completion.choices[0].message.content)
```

### List files
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# List files
files = client.get_files()
for file in files:
    print(f"{file.id} - {file.filename}")
```

### Get single file by id
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Get a single file
single_file = client.get_file_by_id("SOME_FILE_ID")
print(single_file.data.content)
```

### Delete a file
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Delete a file
response = client.delete_file_by_id("SOME_FILE_ID")
print(f"{response.success} - {response.message}")
```

### Update file content
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Update file content
response = client.update_file_content_by_id("SOME_FILE_ID", "SOME NEW CONTENT")
print(f"{response.success} - {response.message}")
```

### Upload a new file
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Upload a file
new_file = client.upload_file("SOME_FILE_PATH")
if new_file.success:
    print(f"Success - {new_file.id}")
else:
    print(f"Failed - {new_file.message}")
```

### List all knowlege
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

response = client.get_knowledge()
for knowledge in response:
    print(f"""
    Found {knowledge.name} {knowledge.id}:
    Description: {knowledge.description}
    Files: {len(knowledge.files)} files
    """)
```

### Get knowledge by id
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

knowledge = client.get_knowledge_by_id("KNOWLEDGE_ID")
print(f"""
Found {knowledge.name} {knowledge.id}:
Description: {knowledge.description}
Files: {len(knowledge.files)} files
""")
```

### Add or remove file to knowledge
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Add file
knowledge = client.add_remove_file_to_knowledge("some_knowledge_id", "some_file_id")
if isinstance(knowledge, ValidationErrorItem):
    print(knowledge.message)
else:
    print(f"Added file {new_file.id} to knowledge {knowledge.id}", True)

# Remove file
knowledge = client.add_remove_file_to_knowledge("some_knowledge_id", "some_file_id", False)
if isinstance(knowledge, ValidationErrorItem):
    print(knowledge.message)
else:
    print(f"Added file {new_file.id} to knowledge {knowledge.id}")
```

### List users
```python
from openwebui_python import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# List users
users = client.get_users()
for user in users:
    print(f"User: {user.name} - {user.role} - {user.created_at} - {user.id}")
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [COPYING](COPYING) file for details.

The GNU GPL v3 is a strong copyleft license that requires any distributed modifications or derivative works to also be licensed under the GPL v3. This ensures that the software remains free and open source.

Key points of the license:
- You can use, modify, and distribute the software freely
- Any modifications or derivative works must also be licensed under GPL v3
- The source code must be made available when distributing the software
- No warranty is provided with the software
