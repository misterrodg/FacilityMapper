from modules.ErrorHelper import print_top_level

ERROR_HEADER = "MAP: "
SUPPORTED_TYPES = ["SID", "STAR"]


class Map:
    def __init__(self, mapDict: dict) -> None:
        self.mapType = None
        self.definition = None

        self.validate(mapDict)

    def validate(self, mapDict: dict) -> None:
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
        return
