from modules.definitions.serializable import Serializable
from typing import Optional, Literal


class Centerline(Serializable):
    def __init__(self, runway_id: str):
        self.runway_id: str = runway_id
        self.length: float = 10.0
        self.crossbar_scale: float = 0.5
        self.selected_iap: str = None
        self.selected_transition: str = None
        self.selected_loc: Optional[Literal[1, 2]] = None
        self.selected_distances: list = []

    def to_dict(self) -> dict:
        return {
            "runway_id": self.runway_id,
            "length": self.length,
            "crossbar_scale": self.crossbar_scale,
            "selected_iap": self.selected_iap,
            "selected_transition": self.selected_transition,
            "selected_loc": self.selected_loc,
            "selected_distances": self.selected_distances,
        }
