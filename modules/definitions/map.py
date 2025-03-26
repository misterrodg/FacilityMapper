from modules.definitions.serializable import Serializable
from modules.definitions.stars_definition import STARSDefinition

from enum import Enum


class MapType(Enum):
    CENTERLINES = "CENTERLINES"
    COMPOSITE_TYPE = "COMPOSITE"
    CONTROLLED_TYPE = "CONTROLLED"
    IAP_TYPE = "IAP"
    LABEL_TYPE = "LABEL"
    LABELS_TYPE = "LABELS"
    RESTRICTIVE_TYPE = "RESTRICTIVE"
    RUNWAYS_TYPE = "RUNWAYS"
    SID_TYPE = "SID"
    STAR_TYPE = "STAR"
    VECTOR_SID_TYPE = "VECTOR" + SID_TYPE


class Map(Serializable):
    def __init__(self, map_type: MapType):
        self.map_type: MapType = map_type
        self.definition: Serializable = None
        self.stars_definition: Serializable = None

    def add_definition(self, definition_object: Serializable) -> None:
        self.definition = definition_object

    def add_stars_definition(self, stars_definition_object: Serializable) -> None:
        self.stars_definition = stars_definition_object

    def to_dict(self) -> dict:
        definition_dict = self.definition.to_dict() if self.definition else {}
        stars_definition_dict = (
            self.stars_definition.to_dict() if self.stars_definition else {}
        )

        return {
            "map_type": self.map_type.value,
            "definition": definition_dict,
            "stars_definition": stars_definition_dict,
        }
