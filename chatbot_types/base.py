from abc import ABC, abstractmethod
from typing import Dict, Any
from models.chatbot import Chatbot
from models.message import Message
from models.thread import Thread

class ChatbotType(ABC):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @abstractmethod
    def chat(self, chatbot: Chatbot, message: Message, thread: Thread) -> Message:
        pass

    @staticmethod
    @abstractmethod
    def get_default_settings() -> Dict[str, Any]:
        pass

    @staticmethod
    @abstractmethod
    def validate_settings(settings: Dict[str, Any]) -> bool:
        pass

    def apply_settings(self, chatbot: Chatbot) -> None:
        type_specific_settings = self.get_default_settings()
        type_specific_settings.update(chatbot.settings.to_dict().get("type_specific", {}))
        if self.validate_settings(type_specific_settings):
            chatbot.settings.update(type_specific=type_specific_settings)
        else:
            raise ValueError("Invalid type-specific settings")