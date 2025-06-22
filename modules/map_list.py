from modules.dir_paths import VIDMAP_DIR
from modules.stars_definition import STARSDefinition

import json


class MapList:
    def __init__(self, facility_id: str):
        self.map_id: int = 0
        self.stars_definitions: list[STARSDefinition] = []
        self.file_name = f"map_list_{facility_id}.json"

    def write_line(self, stars_definition: STARSDefinition) -> None:
        map_id = self.map_id
        if stars_definition.map_id is None:
            stars_definition.map_id = map_id
        else:
            self.map_id = stars_definition.map_id
        self.stars_definitions.append(stars_definition)
        self.map_id += 1

    def write(self) -> None:
        map_list_file = f"{VIDMAP_DIR}/{self.file_name}"
        with open(map_list_file, "w") as ml:
            result = []

            self.stars_definitions.sort(key=lambda definition: definition.map_id)

            for definition in self.stars_definitions:
                result.append(definition.to_dict())

            json.dump(result, ml, indent=2)
