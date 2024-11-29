# OpenWebUI API Python Client

A Python client for interacting with OpenWebUI's API, providing easy access to language models and chat completions.

## Features

- Get available models with detailed information
- Create chat completions using specified models
- Structured data classes for type safety and better code organization

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
from openwebui_client import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Get available models
models = client.get_models()
for model in models:
    print(model.id)
```

### Chat Completion
```python
from openwebui_client import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Create a chat completion
response = client.create_chat_completion(
    model="llama3.2:latest", # Use model id here, not the name
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
        ]
    )
print(response.choices[0].message.content)
```

### Chat Completion
```python
from openwebui_client import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Create a chat completion
response = client.create_chat_completion(
    model="llama3.2:latest", # Use model id here, not the name
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
        ]
    )
print(response.choices[0].message.content)
```

### Chat Completion (with files)
```python
from openwebui_client import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Create a chat completion
completion = client.chat_with_file('llama3.2:latest', "What is this document?", "SOME_FILE_ID")
print(completion.choices[0].message.content)
```

### List files
```python
from openwebui_client import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# List files
files = client.get_files()
for file in files:
    print(f"{file.id} - {file.filename}")
```

### Get single file by id
```python
from openwebui_client import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Get a single file
single_file = client.get_file_by_id("SOME_FILE_ID")
print(single_file.data.content)
```

### Delete a file
```python
from openwebui_client import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Delete a file
response = client.delete_file_by_id("SOME_FILE_ID")
print(f"{response.success} - {response.message}")
```

### Update file content
```python
from openwebui_client import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Update file content
response = client.update_file_content_by_id("SOME_FILE_ID", "SOME NEW CONTENT")
print(f"{response.success} - {response.message}")
```

### Upload a new file
```python
from openwebui_client import OpenWebUI

# Initialize the client
client = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))

# Upload a file
new_file = client.upload_file("SOME_FILE_PATH")
if new_file.success:
    print(f"Success - {new_file.id}")
else:
    print(f"Failed - {new_file.message}")
```