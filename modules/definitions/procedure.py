from modules.definitions.serializable import Serializable

import re


class Procedure(Serializable):
    def __init__(self, airport_id: str, procedure_type: str, procedure_id: str):
        self.airport_id: str = airport_id
        self.procedure_type: str = procedure_type
        self.procedure_id: str = procedure_id
        self.file_name: str = f"{airport_id}_{procedure_type}_{procedure_id.replace("#","")}"
        self.line_style: str = "solid"
        self.draw_symbols: bool = False
        self.symbol_scale: float = 1.0
        self.draw_altitudes: bool = False
        self.draw_speeds: bool = False
        self.draw_names: bool = False
        self.x_offset: float = 0.0
        self.y_offset: float = 0.0
        self.text_scale: float = 1.0
        self.line_height: float = 1.5

    def _replace_trailing_number(self, string: str) -> str:
        return re.sub(r"\d+$", "#", string)

    def to_dict(self) -> dict:
        return {
            "airport_id": self.airport_id,
            "procedure_id": self.procedure_id,
            "file_name": self.file_name,
            "line_style": self.line_style,
            "draw_symbols": self.draw_symbols,
            "symbol_scale": self.symbol_scale,
            "draw_altitudes": self.draw_altitudes,
            "draw_speeds": self.draw_speeds,
            "draw_names": self.draw_names,
            "x_offset": self.x_offset,
            "y_offset": self.y_offset,
            "text_scale": self.text_scale,
            "line_height": self.line_height,
        }
