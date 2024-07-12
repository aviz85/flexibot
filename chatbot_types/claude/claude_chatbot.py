# File: chatbot_types/claude/claude_chatbot.py

from ..conversational_chatbot import ConversationalChatbot
from typing import List, Dict, Any
from models.message import Message, Content
from models.thread import Thread
from .anthropic_api_client import AnthropicAPIClient

class ClaudeChatbot(ConversationalChatbot):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self.anthropic_client = AnthropicAPIClient()

    def chat(self, message: Message, thread: Thread) -> Message:
        conversation_history = self._get_conversation_history(thread)
        response_text = self.process_conversation(message.contents[0].content, conversation_history)
        
        return Message(
            thread_id=thread.id,
            role="assistant",
            contents=[Content(type="text", content=response_text)]
        )

    def process_conversation(self, input_text: str, conversation_history: List[Dict[str, str]]) -> str:
        messages = conversation_history + [{"role": "user", "content": input_text}]

        api_response = self.anthropic_client.call_anthropic_api(
            messages=messages,
            system_prompt=self.settings.get("system_prompt")
        )
        # Extract the response text from the API response
        response_text = api_response['content'][0]['text']
        
        return response_text
        
    def _get_conversation_history(self, thread: Thread) -> List[Dict[str, str]]:
        # This method should be implemented to retrieve and format the conversation history
        # from the storage based on the thread
        # For now, we'll return an empty list as a placeholder
        # In a real implementation, you would fetch messages from the storage and format them
        return []

    @staticmethod
    def get_default_settings() -> Dict[str, Any]:
        default_settings = ConversationalChatbot.get_default_settings()
        default_settings.update({
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "system_prompt": "You are a helpful AI assistant."
        })
        return default_settings

    @staticmethod
    def validate_settings(settings: Dict[str, Any]) -> bool:
        base_valid = ConversationalChatbot.validate_settings(settings)
        claude_valid = (
            isinstance(settings.get("model"), str) and
            isinstance(settings.get("max_tokens"), int) and
            isinstance(settings.get("temperature"), (int, float)) and
            0 <= settings.get("temperature", 0) <= 1 and
            isinstance(settings.get("system_prompt"), str)
        )
        return base_valid and claude_valid

    def apply_settings(self) -> None:
        super().apply_settings()
        # You might want to update the AnthropicAPIClient with new settings here
        # For example, updating the API key if it's in the settings
        api_key = self.settings.get("api_key")
        if api_key:
            self.anthropic_client.update_api_key(api_key)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['type'] = 'claudechatbot'  # Add a type identifier
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClaudeChatbot':
        chatbot = super().from_dict(data)
        # If there's any Claude-specific data to restore, do it here
        return chatbot