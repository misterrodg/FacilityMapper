from modules.definitions.serializable import Serializable
from typing import Literal


class STARSDefinition(Serializable):
    name: str
    map_id: int
    short_name: str
    brightness_category: Literal["A", "B"]
    tdm_only: bool
    always_visible: bool
    note: str | None

    def __init__(self, map_name: str, map_id: int):
        self.name = map_name
        self.map_id = map_id
        self.short_name = map_name.split(" ")[-1]
        self.brightness_category = "A"
        self.tdm_only = False
        self.always_visible = False
        self.note = None

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
