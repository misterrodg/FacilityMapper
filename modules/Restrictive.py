from modules.AirspaceHandler import get_line_strings
from modules.AirspaceQueries import select_restrictive_points
from modules.ErrorHelper import print_top_level
from modules.GeoJSON import GeoJSON, FeatureCollection
from modules.QueryHandler import query_db

from sqlite3 import Cursor

ERROR_HEADER = "RESTRICTIVE: "


class Restrictive:
    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.map_type = "RESTRICTIVE"
        self.restrictive_id = None
        self.restrictive = list[dict]
        self.file_name = None
        self.db_cursor = db_cursor
        self.is_valid = False

        self._validate(definition_dict)

        if self.is_valid:
            self._process()
            self._to_file()

    def _validate(self, definition_dict: dict) -> None:
        restrictive_id = definition_dict.get("restrictive_id")
        if restrictive_id is None:
            print(
                f"{ERROR_HEADER}Missing `restrictive_id` in:\n{print_top_level(definition_dict)}."
            )
            return

        file_name = definition_dict.get("file_name")
        if file_name is None:
            file_name = f"{self.map_type}_{restrictive_id}"

        self.restrictive_id = restrictive_id
        self.file_name = file_name
        self.is_valid = True
        return

    def _process(self) -> None:
        restrictive_query = self._build_query_string()
        self.restrictive = query_db(self.db_cursor, restrictive_query)
        return

    def _build_query_string(self) -> str:
        restrictive_id = f"'{self.restrictive_id}'"
        result = select_restrictive_points(restrictive_id)
        return result

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        feature_collection = get_line_strings(self.restrictive)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
