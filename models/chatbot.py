from uuid import uuid4
from datetime import datetime
from typing import Optional, Dict, Any
from .settings import Settings

class Chatbot:
    def __init__(self, name: str, chatbot_type_id: str, 
                 general_settings: Dict[str, Any] = None, 
                 type_specific_settings: Dict[str, Any] = None,
                 id: Optional[str] = None, created_at: Optional[datetime] = None):
        self.id = id or str(uuid4())
        self.name = name
        self.chatbot_type_id = chatbot_type_id
        self.settings = Settings(general=general_settings, type_specific=type_specific_settings)
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "chatbot_type_id": self.chatbot_type_id,
            "settings": self.settings.to_dict(),
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chatbot':
        settings = data.get("settings", {})
        return cls(
            name=data["name"],
            chatbot_type_id=data["chatbot_type_id"],
            general_settings=settings.get("general"),
            type_specific_settings=settings.get("type_specific"),
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"])
        )