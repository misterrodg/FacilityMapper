from modules.error_helper import print_top_level
from modules.geo_json import GeoJSON, FeatureCollection
from modules.query_handler import query_db
from modules.db import ControlledRecords, select_controlled_points
from modules.airspace import process_controlled

from sqlite3 import Cursor

ERROR_HEADER = "CONTROLLED: "


class Controlled:
    map_type: str
    airport_id: str | None
    controlled: ControlledRecords | None
    file_name: str | None
    db_cursor: Cursor
    is_valid: bool

    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.map_type = "CONTROLLED"
        self.airport_id = None
        self.controlled = None
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
        query_result = query_db(self.db_cursor, controlled_query)
        controlled_records = ControlledRecords()
        controlled_records.from_db_records(query_result)
        self.controlled = controlled_records
        return

    def _build_query_string(self) -> str:
        airport_id = f"'{self.airport_id}'"
        result = select_controlled_points(airport_id)
        return result

    def _to_file(self) -> None:
        if self.controlled.check_for_multiple_classes():
            airspace_classes = self.controlled.get_segmented_by_airspace_class()
            for a_class in airspace_classes:
                airspace_class_id = a_class[0].airspace_class
                geo_json = GeoJSON(f"{self.file_name}_{airspace_class_id}")
                controlled_records = ControlledRecords()
                controlled_records.from_list(a_class)
                feature_collection = process_controlled(controlled_records)
                geo_json.add_feature_collection(feature_collection)
                geo_json.to_file()
        else:
            geo_json = GeoJSON(self.file_name)
            feature_collection = process_controlled(self.controlled)
            geo_json.add_feature_collection(feature_collection)
            geo_json.to_file()
        return
