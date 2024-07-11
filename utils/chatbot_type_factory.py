from typing import Dict, Optional
from chatbot_types.base import ChatbotType

class ChatbotTypeFactory:
    def __init__(self):
        self.chatbot_types: Dict[str, ChatbotType] = {}

    def register(self, chatbot_type: ChatbotType):
        self.chatbot_types[chatbot_type.id] = chatbot_type

    def get(self, chatbot_type_id: str) -> Optional[ChatbotType]:
        return self.chatbot_types.get(chatbot_type_id)

chatbot_type_factory = ChatbotTypeFactory()