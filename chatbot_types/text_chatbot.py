from .base import ChatbotType
from models.chatbot import Chatbot
from models.message import Message, Content
from models.thread import Thread
from typing import Dict, Any

class TextChatbotType(ChatbotType):
    def __init__(self):
        super().__init__("text", "Text Chatbot")

    def chat(self, chatbot: Chatbot, message: Message, thread: Thread) -> Message:
        # In a real implementation, this might involve more complex logic or external API calls
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