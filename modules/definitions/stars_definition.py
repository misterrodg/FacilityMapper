from modules.definitions.serializable import Serializable
from typing import Optional, Literal


class STARSDefinition(Serializable):
    def __init__(self, map_name: str, map_id: int):
        self.name: str = map_name
        self.map_id: int = map_id
        self.short_name: str = map_name.split(" ")[-1]
        self.brightness_category: Optional[Literal["A", "B"]] = "A"
        self.tdm_only: bool = False
        self.always_visible: bool = False
        self.note: str = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "map_id": self.map_id,
            "short_name": self.short_name,
            "brightness_category": self.brightness_category,
            "tdm_only": self.tdm_only,
            "always_visible": self.always_visible,
            "note": self.note,
        }
