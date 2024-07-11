# File: chatbot_types/conversational_chatbot.py

from .base import BaseChatbot
from abc import abstractmethod
from typing import List, Dict, Any
from models.message import Message
from models.thread import Thread

class ConversationalChatbot(BaseChatbot):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

    @abstractmethod
    def process_conversation(self, input_text: str, conversation_history: List[Dict[str, str]]) -> str:
        pass

    def chat(self, message: Message, thread: Thread) -> Message:
        conversation_history = self._get_conversation_history(thread)
        response_text = self.process_conversation(message.contents[0].content, conversation_history)
        
        return Message(
            thread_id=thread.id,
            role="assistant",
            contents=[{"type": "text", "content": response_text}]
        )

    def _get_conversation_history(self, thread: Thread) -> List[Dict[str, str]]:
        # This method should be implemented to retrieve and format the conversation history
        # from the storage based on the thread
        # For now, we'll return an empty list as a placeholder
        return []

    @staticmethod
    def get_default_settings() -> Dict[str, Any]:
        return {
            "max_history_length": 10,
            "response_length": 100
        }

    @staticmethod
    def validate_settings(settings: Dict[str, Any]) -> bool:
        return (
            isinstance(settings.get("max_history_length"), int) and
            isinstance(settings.get("response_length"), int) and
            settings.get("max_history_length", 0) > 0 and
            settings.get("response_length", 0) > 0
        )