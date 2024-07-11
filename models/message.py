
from uuid import uuid4
from datetime import datetime
from typing import List, Dict

class Content:
    def __init__(self, type: str, content: str, metadata: Dict = None):
        self.type = type
        self.content = content
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            "type": self.type,
            "content": self.content,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["type"], data["content"], data.get("metadata"))

class Message:
    def __init__(self, thread_id: str, role: str, contents: List[Content], 
                 id: str = None, created_at: datetime = None, 
                 metadata: Dict = None, visible: bool = True):
        self.id = id or str(uuid4())
        self.thread_id = thread_id
        self.role = role
        self.contents = contents
        self.created_at = created_at or datetime.utcnow()
        self.metadata = metadata or {}
        self.visible = visible

    def to_dict(self):
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "role": self.role,
            "contents": [c.to_dict() for c in self.contents],
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
            "visible": self.visible
        }

    @classmethod
    def from_dict(cls, data):
        contents = [Content.from_dict(c) for c in data["contents"]]
        return cls(
            data["thread_id"],
            data["role"],
            contents,
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            metadata=data.get("metadata"),
            visible=data.get("visible", True)
        )
