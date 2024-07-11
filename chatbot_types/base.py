# File: chatbot_types/base.py

from abc import ABC
from datetime import datetime
from typing import Dict, Any, Optional, List
from models.message import Message
from models.thread import Thread
from models.settings import Settings
from uuid import uuid4

class BaseChatbot(ABC):
    def __init__(self, name: str, id: Optional[str] = None,
                 settings: Optional[Settings] = None, 
                 created_at: Optional[datetime] = None):
        self.id = id or str(uuid4())
        self.name = name
        self.settings = settings or Settings()
        self.created_at = created_at or datetime.utcnow()

    def chat(self, message: Message, thread: Thread) -> Message:
        # Default implementation
        return Message(
            thread_id=thread.id,
            role="assistant",
            contents=[Content(type="text", content="This is a default response.")]
        )

    @staticmethod
    def get_default_settings() -> Dict[str, Any]:
        # Default implementation
        return {
            "response_length": 100,
            "language": "en"
        }

    @staticmethod
    def validate_settings(settings: Dict[str, Any]) -> bool:
        # Default implementation
        return (
            isinstance(settings.get("response_length"), int) and
            isinstance(settings.get("language"), str)
        )

    def apply_settings(self) -> None:
        type_specific_settings = self.get_default_settings()
        type_specific_settings.update(self.settings.to_dict().get("type_specific", {}))
        if self.validate_settings(type_specific_settings):
            self.settings.update(type_specific=type_specific_settings)
        else:
            raise ValueError("Invalid type-specific settings")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "settings": self.settings.to_dict(),
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseChatbot':
        settings = Settings.from_dict(data.get("settings", {}))
        return cls(
            name=data["name"],
            id=data["id"],
            settings=settings,
            created_at=datetime.fromisoformat(data["created_at"])
        )