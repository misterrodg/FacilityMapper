from modules.error_helper import print_top_level
from modules.map import Map
from modules.map_list import MapList

from os.path import isfile, getsize
from sqlite3 import Cursor

import json

ERROR_HEADER = "MANIFEST: "


class Manifest:
    def __init__(
        self, db_cursor: Cursor, manifest_path: str, map_list: MapList = None
    ) -> None:
        self.maps = None
        self.db_cursor = db_cursor
        self.map_list = map_list
        self.is_valid = False

        manifest_dict = self.get_manifest(manifest_path)
        self._validate(manifest_dict)

        if self.is_valid:
            self.process()

    def get_manifest(self, manifest_path: str) -> dict:
        result = {}
        try:
            if isfile(manifest_path) and getsize(manifest_path) > 0:
                with open(manifest_path, "r") as json_file:
                    result = json.load(json_file)

            else:
                print(
                    f"{ERROR_HEADER}Cannot find manifest json data at {manifest_path}."
                )
                print(f"{ERROR_HEADER}Follow the README to create a manifest.")
        except json.JSONDecodeError:
            print("Failed to decode JSON from the file.")
        return result

    def _validate(self, manifest_dict: dict) -> None:
        if not manifest_dict:
            print(f"{ERROR_HEADER}Manifest contains no data.")
            return

        maps = manifest_dict.get("maps")

        if maps is None:
            print(f"{ERROR_HEADER}Missing `maps` in:\n{print_top_level(manifest_dict)}")
            return

        if not isinstance(maps, list):
            print(
                f"{ERROR_HEADER}Incorrect format for `maps`. Should be list, but received {type(maps)}.\n{print_top_level(manifest_dict)}"
            )
            return

        self.maps = maps
        self.is_valid = True
        return

    def process(self) -> None:
        for map in self.maps:
            Map(self.db_cursor, map, self.map_list)
        return
