from modules.definitions.serializable import Serializable

import re


class Procedure(Serializable):
    airport_id: str
    procedure_type: str
    procedure_id: str
    draw_names: bool
    draw_altitudes: bool
    draw_speeds: bool
    draw_symbols: bool
    append_name: str | None
    leading_transitions: list[str]
    suppress_core: bool
    trailing_transitions: list[str]

    def __init__(self, airport_id: str, procedure_type: str, procedure_id: str):
        self.airport_id = airport_id
        self.procedure_type = procedure_type
        self.procedure_id = procedure_id
        self.draw_names = False
        self.draw_altitudes = False
        self.draw_speeds = False
        self.draw_symbols = False
        self.append_name = None
        self.leading_transitions = []
        self.suppress_core = False
        self.trailing_transitions = []

        self._replace_trailing_number()

        self.file_name: str = (
            f"{airport_id}_{procedure_type}_{self.procedure_id.replace("#","")}"
        )

    def _replace_trailing_number(self) -> str:
        if self.procedure_type != "IAP":
            return re.sub(r"\d+$", "#", self.procedure_id)
        return self.procedure_id

    def to_dict(self) -> dict:
        return {
            "airport_id": self.airport_id,
            "procedure_type": self.procedure_type,
            "procedure_id": self.procedure_id,
            "file_name": self.file_name,
            "leading_transitions": self.leading_transitions,
            "suppress_core": self.suppress_core,
            "trailing_transitions": self.trailing_transitions,
            "draw_names": self.draw_names,
            "draw_altitudes": self.draw_altitudes,
            "draw_speeds": self.draw_speeds,
            "draw_symbols": self.draw_symbols,
            "append_name": self.append_name,
        }
