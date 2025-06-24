from modules.definitions.serializable import Serializable

import re


class Procedure(Serializable):
    def __init__(self, airport_id: str, procedure_type: str, procedure_id: str):
        self.airport_id: str = airport_id
        self.procedure_type: str = procedure_type
        self.procedure_id: str = procedure_id
        self.draw_names: bool = False
        self.draw_altitudes: bool = False
        self.draw_speeds: bool = False
        self.draw_symbols: bool = False
        self.append_name: str = None
        self.leading_transitions: list[str] = []
        self.suppress_core: bool = False
        self.trailing_transitions: list[str] = []

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
