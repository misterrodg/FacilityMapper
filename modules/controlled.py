from modules.airspace_handler import get_line_strings
from modules.airspace_queries import select_controlled_points
from modules.error_helper import print_top_level
from modules.geo_json import GeoJSON, FeatureCollection
from modules.query_handler import query_db

from sqlite3 import Cursor

ERROR_HEADER = "CONTROLLED: "


class Controlled:
    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.map_type = "CONTROLLED"
        self.airport_id = None
        self.controlled = list[dict]
        self.file_name = None
        self.db_cursor = db_cursor
        self.is_valid = False

        self._validate(definition_dict)

        if self.is_valid:
            self._process()
            self._to_file()

    def _validate(self, definition_dict: dict) -> None:
        airport_id = definition_dict.get("airport_id")
        if airport_id is None:
            print(
                f"{ERROR_HEADER}Missing `airport_id` in:\n{print_top_level(definition_dict)}."
            )
            return

        file_name = definition_dict.get("file_name")
        if file_name is None:
            file_name = f"{self.map_type}_{airport_id}"

        self.airport_id = airport_id
        self.file_name = file_name
        self.is_valid = True
        return

    def _process(self) -> None:
        controlled_query = self._build_query_string()
        self.controlled = query_db(self.db_cursor, controlled_query)
        return

    def _build_query_string(self) -> str:
        airport_id = f"'{self.airport_id}'"
        result = select_controlled_points(airport_id)
        return result

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        feature_collection = get_line_strings(self.controlled)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
