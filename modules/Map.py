from modules.ErrorHelper import print_top_level
from modules.Label import Label
from modules.SIDSTAR import SIDSTAR

from sqlite3 import Cursor

ERROR_HEADER = "MAP: "
LABEL_TYPE = "LABEL"
SID_TYPE = "SID"
STAR_TYPE = "STAR"
SUPPORTED_TYPES = [LABEL_TYPE, SID_TYPE, STAR_TYPE]


class Map:
    def __init__(self, db_cursor: Cursor, map_dict: dict) -> None:
        self.map_type = None
        self.definition = None
        self.db_cursor = db_cursor
        self.is_valid = False

        self._validate(map_dict)

        if self.is_valid:
            self.process()

    def _validate(self, map_dict: dict) -> None:
        map_type = map_dict.get("map_type")
        if map_type is None:
            print(f"{ERROR_HEADER}Missing `map_type` in:\n{print_top_level(map_dict)}")
            return

        if map_type not in SUPPORTED_TYPES:
            print(f"{ERROR_HEADER}map_type '{map_type}' not recognized.")
            print(f"{ERROR_HEADER}Supported types are {", ".join(SUPPORTED_TYPES)}.")
            return

        definition = map_dict.get("definition")
        if definition is None:
            print(
                f"{ERROR_HEADER}Missing `definition` in:\n{print_top_level(map_dict)}"
            )
            return

        self.map_type = map_type
        self.definition = definition
        self.is_valid = True
        return

    def process(self) -> None:
        if self.map_type == SID_TYPE or self.map_type == STAR_TYPE:
            SIDSTAR(self.db_cursor, self.map_type, self.definition)
        if self.map_type == LABEL_TYPE:
            Label(self.definition)
