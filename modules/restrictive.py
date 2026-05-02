from modules.error_helper import print_top_level
from modules.geo_json import GeoJSON, FeatureCollection
from modules.query_handler import query_db
from modules.db import RestrictiveRecords, select_restrictive_points
from modules.airspace import process_restrictive

from sqlite3 import Cursor

ERROR_HEADER = "RESTRICTIVE: "


class Restrictive:
    map_type: str
    restrictive_id: str
    region: str | None
    restrictive: RestrictiveRecords
    file_name: str
    db_cursor: Cursor
    is_valid: bool

    def __init__(self, db_cursor: Cursor, definition_dict: dict[str, object]):
        self.map_type = "RESTRICTIVE"
        self.restrictive_id = ""
        self.region = ""
        self.restrictive = RestrictiveRecords()
        self.file_name = ""
        self.db_cursor = db_cursor
        self.is_valid = False

        self._validate(definition_dict)

        if self.is_valid:
            self._process()
            self._to_file()

    def _validate(self, definition_dict: dict[str, object]) -> None:
        restrictive_id = definition_dict.get("restrictive_id")
        if not isinstance(restrictive_id, str):
            print(
                f"{ERROR_HEADER}Invalid `restrictive_id` in:\n{print_top_level(definition_dict)}."
            )
            return

        file_name = definition_dict.get("file_name")
        if not isinstance(file_name, str):
            file_name = f"{self.map_type}_{restrictive_id}"

        region = definition_dict.get("region")
        if not isinstance(region, str):
            region = None

        self.region = region
        self.restrictive_id = restrictive_id
        self.file_name = file_name
        self.is_valid = True
        return

    def _process(self) -> None:
        restrictive_query = self._build_query_string()
        query_result = query_db(self.db_cursor, restrictive_query)
        restrictive_records = RestrictiveRecords()
        restrictive_records.from_db_records(query_result)
        self.restrictive = restrictive_records
        return

    def _build_query_string(self) -> str:
        restrictive_id = f"'{self.restrictive_id}'"
        region = None
        if self.region is not None:
            region = f"'{self.region}'"
        result = select_restrictive_points(restrictive_id, region)
        return result

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        feature_collection = process_restrictive(self.restrictive)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
