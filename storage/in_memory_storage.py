from typing import List, Dict, Optional
from models.chatbot import Chatbot
from models.message import Message
from models.thread import Thread

class InMemoryStorage:
    def __init__(self):
        self.chatbots: Dict[str, Chatbot] = {}
        self.threads: Dict[str, Thread] = {}
        self.messages: Dict[str, Message] = {}

    def save_chatbot(self, chatbot: Chatbot) -> None:
        self.chatbots[chatbot.id] = chatbot

    def get_chatbot(self, chatbot_id: str) -> Optional[Chatbot]:
        return self.chatbots.get(chatbot_id)

    def get_chatbots(self, query: Optional[Dict] = None) -> List[Chatbot]:
        if query is None:
            return list(self.chatbots.values())
        
        filtered_chatbots = []
        for chatbot in self.chatbots.values():
            match = True
            for key, value in query.items():
                if getattr(chatbot, key, None) != value:
                    match = False
                    break
            if match:
                filtered_chatbots.append(chatbot)
        return filtered_chatbots

    def save_thread(self, thread: Thread) -> None:
        self.threads[thread.id] = thread

    def get_thread(self, thread_id: str) -> Optional[Thread]:
        return self.threads.get(thread_id)

    def get_threads(self, query: Optional[Dict] = None) -> List[Thread]:
        if query is None:
            return list(self.threads.values())
        
        filtered_threads = []
        for thread in self.threads.values():
            match = True
            for key, value in query.items():
                if getattr(thread, key, None) != value:
                    match = False
                    break
            if match:
                filtered_threads.append(thread)
        return filtered_threads

    def save_message(self, message: Message) -> None:
        self.messages[message.id] = message

    def get_message(self, message_id: str) -> Optional[Message]:
        return self.messages.get(message_id)

    def get_messages(self, query: Optional[Dict] = None) -> List[Message]:
        if query is None:
            return list(self.messages.values())
        
        filtered_messages = []
        for message in self.messages.values():
            match = True
            for key, value in query.items():
                if getattr(message, key, None) != value:
                    match = False
                    break
            if match:
                filtered_messages.append(message)
        return filtered_messages