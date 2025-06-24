from modules.definitions.serializable import Serializable
from typing import Literal


class Centerline(Serializable):
    runway_id: str
    length: float
    crossbar_scale: float
    selected_iap: str | None
    selected_transition: str | None
    selected_loc: Literal[1, 2] | None
    selected_distances: list

    def __init__(self, runway_id: str):
        self.runway_id = runway_id
        self.length = 10.0
        self.crossbar_scale = 0.5
        self.selected_iap = None
        self.selected_transition = None
        self.selected_loc = None
        self.selected_distances = []

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
