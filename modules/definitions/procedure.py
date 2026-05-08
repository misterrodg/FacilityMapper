from modules.definitions.serializable import Serializable

import re

PROCEDURE_TYPES = ["SID", "STAR", "IAP"]
LEADING = "leading"
CORE = "core"
TRAILING = "trailing"
PROCEDURE_SEGMENTS = [LEADING, CORE, TRAILING]


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

    def __init__(self, airport_id: str, procedure_type: str, procedure_id: str) -> None:
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
            f"{procedure_type}_{airport_id}_{self.procedure_id.replace("#","")}"
        )

    def _replace_trailing_number(self) -> None:
        if self.procedure_type != "IAP":
            self.procedure_id = re.sub(r"\d+$", "#", self.procedure_id)

    @staticmethod
    def validate(d: dict) -> tuple[dict | None, list[str]]:
        airport_id = d.get("airport_id")
        if not isinstance(airport_id, str):
            return None, ["Missing or invalid `airport_id`"]

        procedure_type = d.get("procedure_type")
        if not isinstance(procedure_type, str):
            return None, ["Missing or invalid `procedure_type`"]
        if procedure_type not in PROCEDURE_TYPES:
            return None, [
                f"`procedure_type` '{procedure_type}' not recognized. "
                f"Supported types are {', '.join(PROCEDURE_TYPES)}."
            ]

        procedure_id = d.get("procedure_id")
        if not isinstance(procedure_id, str):
            return None, ["Missing or invalid `procedure_id`"]

        draw_names = d.get("draw_names", False)
        if not isinstance(draw_names, bool):
            draw_names = False

        draw_altitudes = d.get("draw_altitudes", False)
        if not isinstance(draw_altitudes, bool):
            draw_altitudes = False

        draw_speeds = d.get("draw_speeds", False)
        if not isinstance(draw_speeds, bool):
            draw_speeds = False

        draw_symbols = d.get("draw_symbols", False)
        if not isinstance(draw_symbols, bool):
            draw_symbols = False

        append_name = d.get("append_name")
        if not isinstance(append_name, str) or append_name not in PROCEDURE_SEGMENTS:
            append_name = ""

        leading_transitions = d.get("leading_transitions", [])
        if not isinstance(leading_transitions, list):
            leading_transitions = []
        elif not all(isinstance(item, str) for item in leading_transitions):
            return None, ["Invalid `leading_transitions`: all items must be strings"]

        suppress_core = d.get("suppress_core", False)
        if not isinstance(suppress_core, bool):
            suppress_core = False

        trailing_transitions = d.get("trailing_transitions", [])
        if not isinstance(trailing_transitions, list):
            trailing_transitions = []
        elif not all(isinstance(item, str) for item in trailing_transitions):
            return None, ["Invalid `trailing_transitions`: all items must be strings"]

        file_name = d.get("file_name")
        if not isinstance(file_name, str):
            file_name = None

        return {
            "airport_id": airport_id,
            "procedure_type": procedure_type,
            "procedure_id": procedure_id,
            "draw_names": draw_names,
            "draw_altitudes": draw_altitudes,
            "draw_speeds": draw_speeds,
            "draw_symbols": draw_symbols,
            "append_name": append_name,
            "leading_transitions": leading_transitions,
            "suppress_core": suppress_core,
            "trailing_transitions": trailing_transitions,
            "file_name": file_name,
        }, []

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
