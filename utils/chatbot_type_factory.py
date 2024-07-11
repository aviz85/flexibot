# File: utils/chatbot_type_factory.py

from typing import Dict, Type, Optional
from chatbot_types.base import BaseChatbot

class ChatbotFactory:
    def __init__(self):
        self.chatbot_types: Dict[str, Type[BaseChatbot]] = {}

    def register(self, chatbot_class: Type[BaseChatbot]):
        self.chatbot_types[chatbot_class.__name__.lower()] = chatbot_class

    def get(self, chatbot_type: str) -> Optional[Type[BaseChatbot]]:
        if chatbot_type is None:
            print("Warning: Attempted to get a chatbot type with None value")
            return None
        chatbot_class = self.chatbot_types.get(chatbot_type.lower())
        if chatbot_class is None:
            print(f"Warning: Unknown chatbot type '{chatbot_type}'")
        return chatbot_class

    def create(self, chatbot_type: str, name: str, **kwargs) -> Optional[BaseChatbot]:
        chatbot_class = self.get(chatbot_type)
        if chatbot_class:
            return chatbot_class(name, **kwargs)
        return None

chatbot_factory = ChatbotFactory()

# Register chatbot types
from chatbot_types.text_chatbot import TextChatbot
from chatbot_types.claude.claude_chatbot import ClaudeChatbot

chatbot_factory.register(TextChatbot)
chatbot_factory.register(ClaudeChatbot)