from modules.ErrorHelper import print_top_level
from modules.Map import Map

from os.path import isfile, getsize
from sqlite3 import Cursor

import json

ERROR_HEADER = "MANIFEST: "


class Manifest:
    def __init__(self, dbCursor: Cursor, manifestPath: str) -> None:
        self.maps = None
        self.dbCursor = dbCursor

        manifestDict = self.getManifest(manifestPath)
        self.validate(manifestDict)
        self.process()

    def getManifest(self, manifestPath: str) -> dict:
        result = {}
        try:
            if isfile(manifestPath) and getsize(manifestPath) > 0:
                with open(manifestPath, "r") as jsonFile:
                    result = json.load(jsonFile)

            else:
                print(
                    f"{ERROR_HEADER}Cannot find manifest json data at {manifestPath}."
                )
                print(f"{ERROR_HEADER}Follow the README to create a manifest.")
        except json.JSONDecodeError:
            print("Failed to decode JSON from the file.")

        return result

    def validate(self, manifestDict: dict) -> None:
        if not manifestDict:
            print(f"{ERROR_HEADER}Manifest contains no data.")
            return

        maps = manifestDict.get("maps")

        if maps is None:
            print(f"{ERROR_HEADER}Missing `maps` in:\n{print_top_level(manifestDict)}")
            return

        if not isinstance(maps, list):
            print(
                f"{ERROR_HEADER}Incorrect format for `maps`. Should be list, but received {type(maps)}.\n{print_top_level(manifestDict)}"
            )
            return

        self.maps = maps
        return

    def process(self) -> None:
        for map in self.maps:
            Map(self.dbCursor, map)
