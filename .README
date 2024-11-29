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
BASE_URL=http://your-openwebui-instance:port
OPENWEBUI_API_KEY=your_api_key_here
```
---
## Usage

```python
from openwebui_client import OpenWebUIClient

# Initialize the client
client = OpenWebUIClient()

# Get available models
models = client.get_models()
for model in models:
    print(model.id)

# Create a chat completion
response = client.create_chat_completion(
    model="llama3.2:latest", # Use model id here, not the name
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
        ]
    )
print(response.choices[0].message.content)
```
