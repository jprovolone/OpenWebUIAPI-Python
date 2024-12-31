# openwebui_api.py

if __name__ == "__main__":
    from models.chat_completion import *
    from models.model import *
    from models.files import *
    from models.knowledge import *
else:
    from .models.chat_completion import *
    from .models.model import *
    from .models.files import *
    from .models.knowledge import *
import os, json, requests, pprint, logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('OpenWebUI')

class OpenWebUI:
    def __init__(self, base_url: str, api_key: str):
        if not base_url:
            raise ValueError("base_url cannot be empty")
        if not api_key:
            raise ValueError("api_key cannot be empty")
            
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        logger.info(f"Initialized OpenWebUI client with base URL: {base_url}")

    #region MODEL METHODS
    def get_models(self) -> list[Model]:
        '''
        Gets all of the available models
        '''
        logger.info("Fetching available models")
        try:
            response = requests.get(f"{self.base_url}/models", headers=self.headers)
            response.raise_for_status()
            
            data = response.json().get('data', [])
            models = []
            for item in data:
                item['actions'] = [Action(**action) for action in item.get('actions', [])]
                item['pipe'] = Pipe(**item['pipe']) if item.get('pipe') else None
                item['openai'] = OpenAI(**item['openai']) if item.get('openai') else None
                item['info'] = Info(**item['info']) if item.get('info') else None
                models.append(Model(**item))
            
            logger.info(f"Successfully retrieved {len(models)} models")
            return models
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch models: {str(e)}")
            raise Exception(f"Failed to fetch models: {str(e)}")
    #endregion
    
    #region CHAT METHODS
    def get_chat_completion(self, model_id: str, prompt: str) -> ChatCompletion:
        '''
        Gets a basic chat completion from openwebui provided a model_id and prompt.
        '''
        if not model_id:
            raise ValueError("model_id cannot be empty")
        if not prompt:
            raise ValueError("prompt cannot be empty")
            
        logger.info(f"Requesting chat completion for model: {model_id}")
        try:
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            choices = []
            for item in data.get('choices', []):
                item['message'] = Message(**item['message'])
                choices.append(Choice(**item))
            data['choices'] = choices
            
            logger.info("Successfully received chat completion")
            return ChatCompletion(**data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get chat completion: {str(e)}")
            raise Exception(f"Failed to get chat completion: {str(e)}")
        
    def get_chat_completion_with_messages(self, model_id: str, messages) -> ChatCompletion:
        if not model_id:
            raise ValueError("model_id cannot be empty")
        if not messages or not isinstance(messages, list):
            raise ValueError("messages must be a non-empty list")
            
        logger.info(f"Requesting chat completion with messages for model: {model_id}")
        try:
            payload = {
                "model": model_id,
                "messages": messages
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            
            data = response.json()
            choices = []
            for item in data.get('choices', []):
                item['message'] = Message(**item['message'])
                choices.append(Choice(**item))
            data['choices'] = choices
            
            logger.info("Successfully received chat completion with messages")
            return ChatCompletion(**data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get chat completion with messages: {str(e)}")
            raise Exception(f"Failed to get chat completion with messages: {str(e)}")
    
    def chat_with_file(self, model: str, query: str, file_id: str) -> ChatCompletion:
        '''
        Chat with or about a specific file. Must upload a file or have a file id first
        '''
        if not model:
            raise ValueError("model cannot be empty")
        if not query:
            raise ValueError("query cannot be empty")
        if not file_id:
            raise ValueError("file_id cannot be empty")
            
        logger.info(f"Requesting chat completion with file {file_id}")
        try:
            payload = {
                'model': model,
                'messages': [{'role': 'user', 'content': query}],
                'files': [{'type': 'file', 'id': file_id}]
            }
            response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            choices = []
            for item in data.get('choices', []):
                item['message'] = Message(**item['message'])
                choices.append(Choice(**item))
            data['choices'] = choices
            
            logger.info("Successfully received chat completion with file")
            return ChatCompletion(**data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get chat completion with file: {str(e)}")
            raise Exception(f"Failed to get chat completion with file: {str(e)}")
    #endregion

    #region FILE METHODS
    def get_files(self) -> list[OpenWebFile]:
        '''
        Get all of the files!
        '''
        logger.info("Fetching all files")
        try:
            response = requests.get(f"{self.base_url}/v1/files", headers=self.headers)
            response.raise_for_status()
            
            files = []
            data = response.json()
            for item in data:
                item['meta'] = Meta(**item['meta'])
                item['data'] = FileData(**item['data'])
                files.append(OpenWebFile(**item))
            
            logger.info(f"Successfully retrieved {len(files)} files")
            return files
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch files: {str(e)}")
            raise Exception(f"Failed to fetch files: {str(e)}")
    
    def get_file_by_id(self, id: str) -> OpenWebFile:
        '''
        Get a single file by id
        '''
        if not id:
            raise ValueError("id cannot be empty")
            
        logger.info(f"Fetching file with id: {id}")
        try:
            response = requests.get(f"{self.base_url}/v1/files/{id}", headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            data['meta'] = Meta(**data['meta'])
            data['data'] = FileData(**data['data'])
            
            logger.info(f"Successfully retrieved file: {data.get('filename', id)}")
            return OpenWebFile(**data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch file {id}: {str(e)}")
            raise Exception(f"Failed to fetch file {id}: {str(e)}")
        
    def delete_file_by_id(self, id: str) -> ValidationErrorItem:
        '''
        Delete a single file by id
        '''
        if not id:
            raise ValueError("id cannot be empty")
            
        logger.info(f"Deleting file with id: {id}")
        try:
            response = requests.delete(f"{self.base_url}/v1/files/{id}", headers=self.headers)
            data = response.json()
            
            if response.status_code == 200:
                data['success'] = True
                logger.info(f"Successfully deleted file: {id}")
            else:
                data['success'] = False
                data['message'] = data.get('detail', 'Unknown error occurred')
                logger.warning(f"Failed to delete file {id}: {data['message']}")
                
            return ValidationErrorItem(**data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete file {id}: {str(e)}")
            raise Exception(f"Failed to delete file {id}: {str(e)}")
    
    def update_file_content_by_id(self, id: str, new_content: str) -> ValidationErrorItem:
        '''
        Update file content by id
        '''
        if not id:
            raise ValueError("id cannot be empty")
        if new_content is None:  # Allow empty string but not None
            raise ValueError("new_content cannot be None")
            
        logger.info(f"Updating content for file with id: {id}")
        try:
            payload = {
                'content': new_content
            }
            response = requests.post(
                f"{self.base_url}/v1/files/{id}/data/content/update", 
                json=payload, 
                headers=self.headers)
            
            data = response.json()
            
            if response.status_code == 200:
                data['success'] = True
                logger.info(f"Successfully updated file content: {id}")
            else:
                data['success'] = False
                data['message'] = data.get('detail', 'Unknown error occurred')
                logger.warning(f"Failed to update file {id}: {data['message']}")
                
            return ValidationErrorItem(**data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update file {id}: {str(e)}")
            raise Exception(f"Failed to update file {id}: {str(e)}")
        
    def upload_file(self, file_path: str):
        '''
        Upload a file
        '''
        if not file_path:
            raise ValueError("file_path cannot be empty")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        logger.info(f"Uploading file: {file_path}")
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.base_url}/v1/files/", headers=self.headers, files=files)
                
            data = response.json()
            
            if response.status_code == 200:
                data['success'] = True
                data['meta'] = Meta(**data['meta'])
                data['data'] = FileData(**data['data'])
                logger.info(f"Successfully uploaded file: {os.path.basename(file_path)}")
                return OpenWebFile(**data)
            else:
                data['success'] = False
                data['message'] = data.get('detail', 'Unknown error occurred')
                logger.warning(f"Failed to upload file {file_path}: {data['message']}")
                return ValidationErrorItem(**data)
        except Exception as e:
            logger.error(f"Failed to upload file {file_path}: {str(e)}")
            raise Exception(f"Failed to upload file {file_path}: {str(e)}")
    #endregion

    #region KNOWLEDGE METHODS
    def get_knowledge(self) -> list[Knowledge]:
        '''
        Get all knowledge items
        '''
        logger.info("Fetching all knowledge items")
        try:
            response = requests.get(f"{self.base_url}/v1/knowledge", headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            knowledges = []
            for item in data:
                knowledges.append(Knowledge(**item))
            
            logger.info(f"Successfully retrieved {len(knowledges)} knowledge items")
            return knowledges
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch knowledge items: {str(e)}")
            raise Exception(f"Failed to fetch knowledge items: {str(e)}")

    def get_knowledge_by_id(self, id: str):
        '''
        Get a single knowledge item by id
        '''
        if not id:
            raise ValueError("id cannot be empty")
            
        logger.info(f"Fetching knowledge item with id: {id}")
        try:
            response = requests.get(f"{self.base_url}/v1/knowledge/{id}", headers=self.headers)
            data = response.json()
            
            if response.status_code == 200:
                logger.info(f"Successfully retrieved knowledge item: {id}")
                return Knowledge(**data)
            else:
                data['success'] = False
                logger.warning(f"Failed to fetch knowledge item {id}: {data.get('detail', 'Unknown error')}")
                return ValidationErrorItem(**data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch knowledge item {id}: {str(e)}")
            raise Exception(f"Failed to fetch knowledge item {id}: {str(e)}")

    def add_remove_file_to_knowledge(self, knowledge_id: str, file_id: str, addRemove: bool):
        '''
        Add or remove a file to a knowledge item
        '''
        if not knowledge_id:
            raise ValueError("knowledge_id cannot be empty")
        if not file_id:
            raise ValueError("file_id cannot be empty")
            
        action = "Adding" if addRemove else "Removing"
        logger.info(f"{action} file {file_id} to/from knowledge item {knowledge_id}")
        
        try:
            payload = {'file_id': file_id}
            url = f"{self.base_url}/v1/knowledge/{knowledge_id}/file/{'add' if addRemove else 'remove'}"

            response = requests.post(url, json=payload, headers=self.headers)
            data = response.json()
            
            if response.status_code == 200:
                logger.info(f"Successfully {action.lower()}ed file {file_id} {'to' if addRemove else 'from'} knowledge item {knowledge_id}")
                return Knowledge(**data)
            else:
                data['success'] = False
                data['message'] = data.get('detail', 'Unknown error occurred')
                logger.warning(f"Failed to {action.lower()} file: {data['message']}")
                return ValidationErrorItem(**data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to {action.lower()} file: {str(e)}")
            raise Exception(f"Failed to {action.lower()} file: {str(e)}")

    #endregion

    #region USER METHODS
    def get_users(self) -> list[User]:
        '''
        Get all users
        '''
        logger.info("Fetching all users")
        try:
            response = requests.get(f"{self.base_url}/v1/users/", headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            users = []
            for item in data:
                users.append(User(**item))
            
            logger.info(f"Successfully retrieved {len(users)} users")
            return users
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch users: {str(e)}")
            raise Exception(f"Failed to fetch users: {str(e)}")

    #endregion

    #region AUDIO METHODS
    def transcribe_audio(self, audio_file_path: str):
        '''
        Transcribe audio file
        '''
        if not audio_file_path:
            raise ValueError("audio_file_path cannot be empty")
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
        logger.info(f"Transcribing audio file: {audio_file_path}")
        try:
            with open(audio_file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.base_url}/audio/api/v1/transcriptions", headers=self.headers, files=files)
                
            if response.status_code == 200:
                logger.info("Successfully transcribed audio file")
                return response.json()
            else:
                error_msg = f"Failed to transcribe audio: {response.text}"
                logger.error(error_msg)
                return {"error": error_msg}
        except Exception as e:
            logger.error(f"Failed to transcribe audio file: {str(e)}")
            raise Exception(f"Failed to transcribe audio file: {str(e)}")

    #endregion

# Example usage
if __name__ == "__main__":
    api = OpenWebUI(os.getenv('BASE_URL'),os.getenv('OPENWEBUI_API_KEY'))
    
    try:
        #region MODEL EXAMPLES
        # Example getting model and id
        models = api.get_models()
        for model in models:
            print(model.id)
        #endregion
        
        #region CHAT EXAMPLES
        # # Example using chat completion
        # completion = api.get_chat_completion('meta-llama/llama-3.1-405b-instruct:free', 'Repeat this phrase exactly: OpenWebUI is awesome!')
        # pprint.pprint(completion.choices[0].message.content)

        # # Example using chat completion with preloaded messages
        # with open("test.json", "r") as file:
        #     json_data = json.load(file)
        #     completion = api.get_chat_completion_with_messages(
        #         'qwen/qvq-72b-preview',
        #         messages = json_data
        #         )
        #     pprint.pprint(completion)
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
        # users = api.get_users()
        # for user in users:
        #     print(f"User: {user.name} - {user.role} - {user.created_at} - {user.id}")
        #endregion
    
        #region AUDIO EXAMPLES
        # # Example transcribing audio file
        # response = api.transcribe_audio("audio_file_path")
        # pprint.pprint(response)
        #endregion
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        print(f"Error: {str(e)}")
