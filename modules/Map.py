from modules.ErrorHelper import print_top_level
from modules.Label import Label
from modules.SIDSTAR import SIDSTAR

from sqlite3 import Cursor

ERROR_HEADER = "MAP: "
SUPPORTED_TYPES = ["LABEL", "SID", "STAR"]


class Map:
    def __init__(self, dbCursor: Cursor, mapDict: dict) -> None:
        self.mapType = None
        self.definition = None
        self.dbCursor = dbCursor
        self.isValid = False

        self._validate(mapDict)

        if self.isValid:
            self.process()

    def _validate(self, mapDict: dict) -> None:
        mapType = mapDict.get("map_type")
        if mapType is None:
            print(f"{ERROR_HEADER}Missing `map_type` in:\n{print_top_level(mapDict)}")
            return

        if mapType not in SUPPORTED_TYPES:
            print(f"{ERROR_HEADER}map_type '{mapType}' not recognized.")
            print(f"{ERROR_HEADER}Supported types are {", ".join(SUPPORTED_TYPES)}.")
            return

        definition = mapDict.get("definition")
        if definition is None:
            print(f"{ERROR_HEADER}Missing `definition` in:\n{print_top_level(mapDict)}")
            return

        self.mapType = mapType
        self.definition = definition
        self.isValid = True
        return

    def process(self) -> None:
        if self.mapType == "SID" or self.mapType == "STAR":
            SIDSTAR(self.dbCursor, self.mapType, self.definition)
        if self.mapType == "LABEL":
            Label(self.definition)
