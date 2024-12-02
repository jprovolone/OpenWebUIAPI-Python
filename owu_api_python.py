# openwebui_api.py

from models.chat_completion import *
from models.model import *
from models.files import *
from models.knowledge import *
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

    #region MODEL METHODS
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
    #endregion
    
    #region CHAT METHODS
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
        
    def get_chat_completion(self, model_id: str, messages) -> ChatCompletion:
        '''
        Gets a basic chat completion from openwebui provided a model_id and a set of messages.
        '''
        payload = {
            "model": model_id,
            "messages": messages
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
    
    def chat_with_file(self, model, query, file_id) -> ChatCompletion:
        '''
        Chat with or about a specific file. Must upload a file or have a file id first
        '''
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': query}],
            'files': [{'type': 'file', 'id': file_id}]
        }
        response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload)
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
    #endregion

    #region FILE METHODS
    def get_files(self) -> list[OpenWebFile]:
        '''
        Get all of the files!
        '''
        response = requests.get(f"{self.base_url}/v1/files", headers=self.headers)
        if response.status_code == 200:
            files = []
            data = response.json()
            for item in data:
                item['meta'] = Meta(**item['meta'])
                item['data'] = FileData(**item['data'])
                files.append(OpenWebFile(**item))
            return files
    
    def get_file_by_id(self, id) -> OpenWebFile:
        '''
        Get a single file by id
        '''
        response = requests.get(f"{self.base_url}/v1/files/{id}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            data['meta'] = Meta(**data['meta'])
            data['data'] = FileData(**data['data'])
            return OpenWebFile(**data)
        
    def delete_file_by_id(self, id) -> ValidationErrorItem:
        '''
        Delete a single file by id
        '''
        response = requests.delete(f"{self.base_url}/v1/files/{id}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            data['success'] = True
            return ValidationErrorItem(**data)
        else:
            data = response.json()
            data['success'] = False
            data['message'] = data['detail']
            return ValidationErrorItem(**data)
    
    def update_file_content_by_id(self, id, new_content):
        '''
        Update file content by id
        '''
        payload = {
            'content': new_content
        }
        response = requests.post(
            f"{self.base_url}/v1/files/{id}/data/content/update", 
            json=payload, 
            headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            
            data['success'] = True
            return ValidationErrorItem(**data)
        else:
            data = response.json()
            data['success'] = False
            data['message'] = data['detail']
            return ValidationErrorItem(**data)
        
    def upload_file(self, file_path):
        '''
        Upload a file
        '''
        files = {'file': open(file_path, 'rb')}
        response = requests.post(f"{self.base_url}/v1/files/", headers=self.headers, files=files)
        data = response.json()
        if response.status_code == 200:
            data['success'] = True
            data['meta'] = Meta(**data['meta'])
            data['data'] = FileData(**data['data'])
            return OpenWebFile(**data)
        else:
            data['success'] = False
            data['message'] = data['detail']
            return ValidationErrorItem(**data)
    #endregion

    #region KNOWLEDGE METHODS
    def get_knowledge(self) -> list[Knowledge]:
        '''
        Get all knowledge items
        '''
        response = requests.get(f"{self.base_url}/v1/knowledge", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            knowledges = []
            for item in data:
                knowledges.append(Knowledge(**item))
            return knowledges

    def get_knowledge_by_id(self, id):
        '''
        Get a single knowledge item by id
        '''
        response = requests.get(f"{self.base_url}/v1/knowledge/{id}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return Knowledge(**data)
        else:
            data = response.json()
            data['success'] = False
            return ValidationErrorItem(**data)

    def add_remove_file_to_knowledge(self, knowledge_id, file_id, addRemove):
        '''
        Add or remove a file to a knowledge item
        '''
        payload = {'file_id': file_id}
        if addRemove:
            url = f"{self.base_url}/v1/knowledge/{knowledge_id}/file/add"
        else:
            url = f"{self.base_url}/v1/knowledge/{knowledge_id}/file/remove"

        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return Knowledge(**data)
        else:
            data = response.json()
            data['success'] = False
            data['message'] = data['detail']
            return ValidationErrorItem(**data)

    #endregion

    #region USER METHODS
    def get_users(self) -> list[User]:
        '''
        Get all users
        '''
        response = requests.get(f"{self.base_url}/v1/users/", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            users = []
            for item in data:
                users.append(User(**item))
            return users

    #endregion

    #region AUDIO METHODS
    def transcribe_audio(self, audio_file_path: str):
        '''
        Transcribe audio file
        '''
        files = {'file': open(audio_file_path, 'rb')}
        response = requests.post(f"{self.base_url}/audio/api/v1/transcriptions", headers=self.headers, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()


    #endregion

# Example usage
if __name__ == "__main__":
    api = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))
    
    try:
        #region MODEL EXAMPLES
        # # Example getting model and id
        # models = api.get_models()
        # for model in models:
        #     print(model)
        #     break
        #endregion
        
        #region CHAT EXAMPLES
        # # Example using chat completion
        # completion = api.get_chat_completion('llama3.2:latest', 'Repeat this phrase exactly: OpenWebUI is awesome!')
        # pprint.pprint(completion.choices[0].message.content)

        # # Example using chat completion with preloaded messages
        # with open("file_with_preloaded_messages.json", "r") as file:
        #     json_data = json.load(file)
        #     completion = api.get_chat_completion(
        #         'gpt-4o',
        #         messages = json_data
        #         )
        #     pprint.pprint(completion.choices[0].message.content)

        # # Example chat with file
        # completion = api.chat_with_file('llama3.2:latest', "What is this document?", "05094421-5b5a-43da-9c56-ddc054945fac")
        # print(completion.choices[0].message.content)
        #endregion
        
        #region FILES EXAMPLES
        # # Example getting all files
        # files = api.get_files()
        # for file in files:
        #     print(f"{file.id} - {file.filename}")

        # # Example getting a single file by id
        # single_file = api.get_file_by_id("c9b052bb-8ca7-438b-94ac-d5adab8af51e")
        # print(single_file.data.content)

        # # Example deleting a single file by id
        # response = api.delete_file_by_id("a521753e-9223-47f7-a9d6-deae48a9f0df")
        # print(f"{response.success} - {response.message}")

        # # Example bulk deleting files by their id
        # file_ids = ['26055075-59cf-414f-a5c0-53587d89149b',
        #     '3603de45-b378-4329-b2d3-83b654a0d912',
        #     '276d7f34-7033-4bb6-aa38-c836a68a3f95',
        #     '40575bb6-7de7-4afc-bb66-d63633781422',
        #     'ef64320e-8887-4e2f-a5e5-96afdd2cf809']
        # for i in file_ids:
        #     response = api.delete_file_by_id(i)
        #     print(f"{response.success} - {response.message}")

        # # Example updating file content by id
        # response = api.update_file_content_by_id("4ec052e0-5470-49b6-af5d-8239268d7a", "SOME NEW CONTENT")
        # print(f"{response.success} - {response.message}")

        # # Example uploading a file
        # new_file = api.upload_file("some_file_path")
        # if new_file.success:
        #     print(f"Success - {new_file.id}")
        # else:
        #     print(f"Failed - {new_file.message}")
        
        #endregion

        #region KNOWLEDGE EXAMPLES
        # # Example getting knowledge
        # response = api.get_knowledge()
        # for knowledge in response:
        #     print(f"""
        #     Found {knowledge.name} {knowledge.id}:
        #     Description: {knowledge.description}
        #     Files: {len(knowledge.files)} files
        #     """)

        # # Example getting a single knowledge item by id
        # knowledge = api.get_knowledge_by_id("dd659ea6-57be-422f-9db9-e6ff265bf7cb")
        # if isinstance(knowledge, ValidationErrorItem):
        #     print(knowledge.detail)
        # else:
        #     print(f"""
        #     Retrieved {knowledge.name} {knowledge.id}:
        #     Description: {knowledge.description}
        #     Files: {len(knowledge.files)} files
        #     """)

        # # Example adding file to knowledge
        # knowledge = api.add_remove_file_to_knowledge("dd659ea6-57be-422f-9db9-e6ff265bf7cb", new_file.id, True)
        # if isinstance(knowledge, ValidationErrorItem):
        #     print(knowledge.message)
        # else:
        #     print(f"Added file {new_file.id} to knowledge {knowledge.id}")

        #endregion

        #region USER EXAMPLES
        users = api.get_users()
        for user in users:
            print(f"User: {user.name} - {user.role} - {user.created_at} - {user.id}")
        #endregion
    
        #region AUDIO EXAMPLES
        # # Example transcribing audio file
        # response = api.transcribe_audio("audio_file_path")
        # pprint.pprint(response)
        #endregion
    except Exception as e:
        print(e)