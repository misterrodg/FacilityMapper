from modules.error_helper import print_top_level
from modules.geo_json import GeoJSON, FeatureCollection
from modules.query_handler import query_db
from modules.db import RestrictiveRecords, select_restrictive_points
from modules.airspace import process_restrictive

from sqlite3 import Cursor

ERROR_HEADER = "RESTRICTIVE: "


class Restrictive:
    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.map_type: str = "RESTRICTIVE"
        self.restrictive_id: str = None
        self.restrictive: RestrictiveRecords = None
        self.file_name: str = None
        self.db_cursor: Cursor = db_cursor
        self.is_valid: bool = False

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
        query_result = query_db(self.db_cursor, restrictive_query)
        restrictive_records = RestrictiveRecords(query_result)
        self.restrictive = restrictive_records
        return

    def _build_query_string(self) -> str:
        restrictive_id = f"'{self.restrictive_id}'"
        result = select_restrictive_points(restrictive_id)
        return result

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        feature_collection = process_restrictive(self.restrictive)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
