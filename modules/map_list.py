from modules.dir_paths import VIDMAP_DIR
from modules.stars_definition import STARSDefinition, DEFINITION_HEADER

MAP_LIST_NAME = "map_list.txt"


class MapList:
    def __init__(self):
        self.map_id = 0
        self.lines: list[str] = []

        self.lines.append(DEFINITION_HEADER)

    def write_line(self, stars_definition: STARSDefinition) -> None:
        map_id = self.map_id
        if stars_definition.map_id is not None:
            map_id = stars_definition.map_id
        line = f"{map_id},{stars_definition.to_line()}"
        self.lines.append(line)
        self.map_id += 1

    def write(self) -> None:
        map_list_file = f"{VIDMAP_DIR}/{MAP_LIST_NAME}"
        with open(map_list_file, "w") as list_file:
            list_file.writelines(self.lines)
