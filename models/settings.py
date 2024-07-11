# File: models/settings.py

from typing import Any, Dict, Optional

class Settings:
    def __init__(self, general: Dict[str, Any] = None, type_specific: Dict[str, Any] = None):
        self._general = general or {}
        self._type_specific = type_specific or {}

    def get(self, key: str, default: Any = None) -> Any:
        return self._type_specific.get(key) or self._general.get(key) or default

    def set_general(self, key: str, value: Any):
        self._general[key] = value

    def set_type_specific(self, key: str, value: Any):
        self._type_specific[key] = value

    def update(self, general: Optional[Dict[str, Any]] = None, type_specific: Optional[Dict[str, Any]] = None):
        if general:
            self._general.update(general)
        if type_specific:
            self._type_specific.update(type_specific)

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        return {
            "general": self._general,
            "type_specific": self._type_specific
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Dict[str, Any]]) -> 'Settings':
        return cls(general=data.get("general", {}), type_specific=data.get("type_specific", {}))

    @property
    def general(self) -> Dict[str, Any]:
        return self._general

    @property
    def type_specific(self) -> Dict[str, Any]:
        return self._type_specific