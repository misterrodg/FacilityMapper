from modules.dir_paths import VIDMAP_DIR
from modules.stars_definition import STARSDefinition, DEFINITION_HEADER

MAP_LIST_NAME = "map_list.txt"


class MapList:
    def __init__(self):
        self.map_id: int = 0
        self.stars_definitions: list[STARSDefinition] = []

    def write_line(self, stars_definition: STARSDefinition) -> None:
        map_id = self.map_id
        if stars_definition.map_id is None:
            stars_definition.map_id = map_id
        else:
            self.map_id = stars_definition.map_id
        self.stars_definitions.append(stars_definition)
        self.map_id += 1

    def write(self) -> None:
        map_list_file = f"{VIDMAP_DIR}/{MAP_LIST_NAME}"
        with open(map_list_file, "w") as list_file:
            result = []
            result.append(DEFINITION_HEADER)

            self.stars_definitions.sort(key=lambda definition: definition.map_id)

            for definition in self.stars_definitions:
                result.append(definition.to_line())

            list_file.writelines(result)
