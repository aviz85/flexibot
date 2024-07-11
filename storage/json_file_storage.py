import json
import os
from typing import List, Dict, Optional
from models.chatbot import Chatbot
from models.message import Message
from models.thread import Thread

class JSONFileStorage:
    def __init__(self, data_folder: str = 'data'):
        self.data_folder = data_folder
        self.ensure_data_folder_exists()

    def ensure_data_folder_exists(self):
        os.makedirs(self.data_folder, exist_ok=True)
        for subfolder in ['chatbots', 'threads', 'messages']:
            os.makedirs(os.path.join(self.data_folder, subfolder), exist_ok=True)

    def save_chatbot(self, chatbot: Chatbot) -> None:
        file_path = os.path.join(self.data_folder, 'chatbots', f"{chatbot.id}.json")
        with open(file_path, 'w') as f:
            json.dump(chatbot.to_dict(), f)

    def get_chatbot(self, chatbot_id: str) -> Optional[Chatbot]:
        file_path = os.path.join(self.data_folder, 'chatbots', f"{chatbot_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return Chatbot.from_dict(json.load(f))
        return None

    def get_chatbots(self, query: Optional[Dict] = None) -> List[Chatbot]:
        chatbots = []
        chatbots_folder = os.path.join(self.data_folder, 'chatbots')
        for filename in os.listdir(chatbots_folder):
            if filename.endswith('.json'):
                with open(os.path.join(chatbots_folder, filename), 'r') as f:
                    chatbot = Chatbot.from_dict(json.load(f))
                    if query is None or all(getattr(chatbot, k) == v for k, v in query.items()):
                        chatbots.append(chatbot)
        return chatbots

    def delete_chatbot(self, chatbot_id: str) -> None:
        file_path = os.path.join(self.data_folder, 'chatbots', f"{chatbot_id}.json")
        if os.path.exists(file_path):
            os.remove(file_path)

    def save_thread(self, thread: Thread) -> None:
        file_path = os.path.join(self.data_folder, 'threads', f"{thread.id}.json")
        with open(file_path, 'w') as f:
            json.dump(thread.to_dict(), f)

    def get_thread(self, thread_id: str) -> Optional[Thread]:
        file_path = os.path.join(self.data_folder, 'threads', f"{thread_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return Thread.from_dict(json.load(f))
        return None

    def get_threads(self, query: Optional[Dict] = None) -> List[Thread]:
        threads = []
        threads_folder = os.path.join(self.data_folder, 'threads')
        for filename in os.listdir(threads_folder):
            if filename.endswith('.json'):
                with open(os.path.join(threads_folder, filename), 'r') as f:
                    thread = Thread.from_dict(json.load(f))
                    if query is None or all(getattr(thread, k) == v for k, v in query.items()):
                        threads.append(thread)
        return threads

    def save_message(self, message: Message) -> None:
        file_path = os.path.join(self.data_folder, 'messages', f"{message.id}.json")
        with open(file_path, 'w') as f:
            json.dump(message.to_dict(), f)

    def get_message(self, message_id: str) -> Optional[Message]:
        file_path = os.path.join(self.data_folder, 'messages', f"{message_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return Message.from_dict(json.load(f))
        return None

    def get_messages(self, query: Optional[Dict] = None) -> List[Message]:
        messages = []
        messages_folder = os.path.join(self.data_folder, 'messages')
        for filename in os.listdir(messages_folder):
            if filename.endswith('.json'):
                with open(os.path.join(messages_folder, filename), 'r') as f:
                    message = Message.from_dict(json.load(f))
                    if query is None or all(getattr(message, k) == v for k, v in query.items()):
                        messages.append(message)
        return messages