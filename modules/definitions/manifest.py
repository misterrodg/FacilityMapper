from modules.definitions.map import Map
from modules.dir_paths import MANIFEST_DIR

import json


class Manifest:
    def __init__(self):
        self.maps: list[Map] = []

    def add_map(self, map) -> None:
        self.maps.append(map)

    def to_file(self, file_name: str, is_eram_mode: bool = False) -> None:
        map_dicts = []
        for map in self.maps:
            map_dicts.append(map.to_dict(is_eram_mode))

        result = {"maps": map_dicts}

        with open(f"{MANIFEST_DIR}/{file_name}.json", "w") as json_file:
            json.dump(result, json_file, indent=2)
