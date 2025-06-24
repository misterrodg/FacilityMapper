from modules.definitions.serializable import Serializable

from enum import Enum


class MapType(Enum):
    CENTERLINES = "CENTERLINES"
    COMPOSITE_TYPE = "COMPOSITE"
    CONTROLLED_TYPE = "CONTROLLED"
    ERAM_PROCEDURE_TYPE = "ERAM PROCEDURE"
    LABEL_TYPE = "LABEL"
    LABELS_TYPE = "LABELS"
    RESTRICTIVE_TYPE = "RESTRICTIVE"
    RUNWAYS_TYPE = "RUNWAYS"
    STARS_PROCEDURE_TYPE = "STARS PROCEDURE"
    VECTOR_SID_TYPE = "VECTORSID"


class Map(Serializable):
    map_type: MapType
    definition: Serializable | None
    stars_definition: Serializable | None

    def __init__(self, map_type: MapType):
        self.map_type = map_type
        self.definition = None
        self.stars_definition = None

    def add_definition(self, definition_object: Serializable) -> None:
        self.definition = definition_object

    def add_stars_definition(self, stars_definition_object: Serializable) -> None:
        self.stars_definition = stars_definition_object

    def to_dict(self, is_eram_mode: bool = False) -> dict:
        definition_dict = self.definition.to_dict() if self.definition else {}
        stars_definition_dict = (
            self.stars_definition.to_dict() if self.stars_definition else {}
        )

        if is_eram_mode:
            return {
                "map_type": self.map_type.value,
                "definition": definition_dict,
            }

        return {
            "map_type": self.map_type.value,
            "definition": definition_dict,
            "stars_definition": stars_definition_dict,
        }
