from modules.error_helper import print_top_level
from modules.geo_json import FeatureCollection, GeoJSON
from modules.query_handler import query_db
from modules.db import select_runways_by_airport_id, RunwayRecords
from modules.runway import get_line_strings, RunwayPair, RunwayPairs

from sqlite3 import Cursor

ERROR_HEADER = "RUNWAYS: "


class Runways:
    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.map_type: str = "RUNWAYS"
        self.airport_ids: list = []
        self.airport_runways: list[list[RunwayPair]] = []
        self.file_name: str = None
        self.db_cursor: Cursor = db_cursor
        self.is_valid: bool = False

        self._validate(definition_dict)

        if self.is_valid:
            self._process()
            self._to_file()

    def _validate(self, definition_dict: dict) -> None:
        airport_ids = definition_dict.get("airport_ids")
        if airport_ids is None:
            print(
                f"{ERROR_HEADER}Missing `airport_ids` in:\n{print_top_level(definition_dict)}."
            )
            return

        file_name = definition_dict.get("file_name")
        if file_name is None:
            print(
                f"{ERROR_HEADER}Missing `file_name` in:\n{print_top_level(definition_dict)}."
            )
            return

        self.airport_ids = airport_ids
        self.file_name = file_name
        self.is_valid = True
        return

    def _process(self) -> None:
        for airport_id in self.airport_ids:
            runways_query = self._build_query_string(airport_id)
            query_result = query_db(self.db_cursor, runways_query)
            runway_records = RunwayRecords(query_result)
            paired_runways = RunwayPairs(runway_records)
            self.airport_runways.append(paired_runways.get_runway_pairs())
        return

    def _build_query_string(self, airport_id: str) -> str:
        airport_id = f"'{airport_id}'"
        result = select_runways_by_airport_id(airport_id)
        return result

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        feature = get_line_strings(self.airport_runways)
        feature_collection.add_feature(feature)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
