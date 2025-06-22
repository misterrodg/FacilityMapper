from modules.centerlines import Centerlines
from modules.composite import Composite
from modules.controlled import Controlled
from modules.eram_procedure import ERAMProcedure
from modules.error_helper import print_top_level
from modules.label import Label
from modules.labels import Labels
from modules.map_list import MapList
from modules.restrictive import Restrictive
from modules.runways import Runways
from modules.stars_definition import STARSDefinition
from modules.stars_procedure import STARSProcedure
from modules.vector_sid import VectorSID

from sqlite3 import Cursor

ERROR_HEADER = "MAP: "
CENTERLINES = "CENTERLINES"
COMPOSITE_TYPE = "COMPOSITE"
CONTROLLED_TYPE = "CONTROLLED"
ERAM_PROCEDURE = "ERAM PROCEDURE"
LABEL_TYPE = "LABEL"
LABELS_TYPE = "LABELS"
PLACEHOLDER_TYPE = "PLACEHOLDER"
RESTRICTIVE_TYPE = "RESTRICTIVE"
RUNWAYS_TYPE = "RUNWAYS"
STARS_PROCEDURE_TYPE = "STARS PROCEDURE"
VECTOR_SID_TYPE = "VECTORSID"
SUPPORTED_TYPES = [
    CENTERLINES,
    CONTROLLED_TYPE,
    COMPOSITE_TYPE,
    ERAM_PROCEDURE,
    LABEL_TYPE,
    LABELS_TYPE,
    PLACEHOLDER_TYPE,
    RESTRICTIVE_TYPE,
    RUNWAYS_TYPE,
    STARS_PROCEDURE_TYPE,
    VECTOR_SID_TYPE,
]


class Map:
    def __init__(
        self, db_cursor: Cursor, map_dict: dict, map_list: MapList = None
    ) -> None:
        self.map_type: str = None
        self.definition: dict = None
        self.stars_definition: dict = None
        self.db_cursor: Cursor = db_cursor
        self.map_list: MapList = map_list
        self.is_valid: bool = False

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

        stars_definition = map_dict.get("stars_definition")

        self.map_type = map_type
        self.definition = definition
        self.stars_definition = stars_definition
        self.is_valid = True
        return

    def process(self) -> None:
        if self.map_type == CENTERLINES:
            Centerlines(self.db_cursor, self.definition)
        if self.map_type == ERAM_PROCEDURE:
            ERAMProcedure(self.db_cursor, self.definition)
        if self.map_type == STARS_PROCEDURE_TYPE:
            STARSProcedure(self.db_cursor, self.definition)
        if self.map_type == VECTOR_SID_TYPE:
            VectorSID(self.db_cursor, self.definition)
        if self.map_type == RUNWAYS_TYPE:
            Runways(self.db_cursor, self.definition)
        if self.map_type == LABEL_TYPE:
            Label(self.definition)
        if self.map_type == LABELS_TYPE:
            Labels(self.definition)
        if self.map_type == COMPOSITE_TYPE:
            Composite(self.definition)
        if self.map_type == CONTROLLED_TYPE:
            Controlled(self.db_cursor, self.definition)
        if self.map_type == RESTRICTIVE_TYPE:
            Restrictive(self.db_cursor, self.definition)
        if self.map_type == PLACEHOLDER_TYPE:
            pass

        if self.map_list is not None and self.stars_definition is not None:
            stars_definition = STARSDefinition(self.stars_definition)
            self.map_list.write_line(stars_definition)
