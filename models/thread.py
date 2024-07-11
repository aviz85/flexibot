
from uuid import uuid4
from datetime import datetime
from typing import Dict

class Thread:
    def __init__(self, chatbot_id: str, id: str = None, 
                 created_at: datetime = None, metadata: Dict = None, 
                 visible: bool = True):
        self.id = id or str(uuid4())
        self.chatbot_id = chatbot_id
        self.created_at = created_at or datetime.utcnow()
        self.metadata = metadata or {}
        self.visible = visible

    def to_dict(self):
        return {
            "id": self.id,
            "chatbot_id": self.chatbot_id,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
            "visible": self.visible
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["chatbot_id"],
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            metadata=data.get("metadata"),
            visible=data.get("visible", True)
        )
