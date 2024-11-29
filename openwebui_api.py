# openwebui_api.py

from models import Model, ChatCompletion, ChatWithFile, ChatWithCollection, Choice, Message
from models import Action, Pipe, OpenAI, Info
import os, json, requests, pprint
from dotenv import load_dotenv

load_dotenv()

class OpenWebUI:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    # methods
    def get_models(self) -> list[Model]:
        '''
        Gets all of the available models
        '''
        response = requests.get(f"{self.base_url}/models", headers=self.headers)
        if response.status_code == 200:
            data = response.json().get('data', [])
            models = []
            for item in data:
                item['actions'] = [Action(**action) for action in item.get('actions', [])]
                item['pipe'] = Pipe(**item['pipe']) if item.get('pipe') else None
                item['openai'] = OpenAI(**item['openai']) if item.get('openai') else None
                item['info'] = Info(**item['info']) if item.get('info') else None
                models.append(Model(**item))
            return models

    def get_chat_completion(self, model_id: str, prompt: str) -> ChatCompletion:
        '''
        Gets a basic chat completion from openwebui provided a model_id and prompt.
        '''
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            choices = []
            for item in data.get('choices', []):
                item['message'] = Message(**item['message'])
                choices.append(Choice(**item))
            data['choices'] = choices
            return ChatCompletion(**data)
        else:
            raise Exception(f"Failed to get chat completion: {response.status_code}")
        

# Example usage
if __name__ == "__main__":
    api = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))
    
    try:
        # Example getting model and id
        models = api.get_models()
        for model in models:
            print(model)
            break
        
        # Example using chat completion
        completion = api.get_chat_completion('llama3.2:latest', 'Repeat this phrase exactly: OpenWebUI is awesome!')
        pprint.pprint(completion.choices[0].message.content)
        

    except Exception as e:
        print(e)