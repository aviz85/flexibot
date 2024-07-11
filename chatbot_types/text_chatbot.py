# File: chatbot_types/text_chatbot.py

from .base import BaseChatbot
from models.message import Message, Content
from models.thread import Thread
from typing import Dict, Any

class TextChatbot(BaseChatbot):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

    def chat(self, message: Message, thread: Thread) -> Message:
        # Simple echo implementation
        response_text = f"Echo: {message.contents[0].content}"
        return Message(
            thread_id=thread.id,
            role="assistant",
            contents=[Content(type="text", content=response_text)]
        )

    @staticmethod
    def get_default_settings() -> Dict[str, Any]:
        return {
            "max_response_length": 1000,
            "response_prefix": "Bot: "
        }

    @staticmethod
    def validate_settings(settings: Dict[str, Any]) -> bool:
        return (
            isinstance(settings.get("max_response_length"), int) and
            isinstance(settings.get("response_prefix"), str)
        )