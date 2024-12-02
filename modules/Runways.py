from modules.ErrorHelper import print_top_level
from modules.GeoJSON import FeatureCollection, GeoJSON
from modules.QueryHandler import query_db
from modules.RunwayHandler import get_line_strings
from modules.RunwayHelper import inverse_runway
from modules.RunwayQueries import select_runways_by_airport_id

from sqlite3 import Cursor

ERROR_HEADER = "RUNWAYS: "


class Runways:
    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.map_type = "RUNWAYS"
        self.airport_ids = []
        self.airport_runways: list[list[dict]] = []
        self.file_name = None
        self.db_cursor = db_cursor
        self.is_valid = False

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
            runways_rows = query_db(self.db_cursor, runways_query)
            paired_runways = self._pair_runways(runways_rows)
            self.airport_runways.append(paired_runways)
        return

    def _find_runway_in_list(self, runway_list: list[dict], runway_id: str) -> dict:
        result = next((r for r in runway_list if r.get("runway_id") == runway_id), None)
        return result

    def _pair_runways(self, db_rows: list[dict]) -> list[dict]:
        result = []
        runway_end_count = len(db_rows)
        runway_count = int(runway_end_count / 2)
        runway_bases = db_rows[:runway_count]
        runway_reciprocals = db_rows[runway_count:]
        for base in runway_bases:
            pair_dict = {}
            runway_id = base.get("runway_id")
            reciprocal_id = inverse_runway(runway_id)
            reciprocal = self._find_runway_in_list(runway_reciprocals, reciprocal_id)
            pair_dict["airport_id"] = base["airport_id"]
            pair_dict["base_id"] = base["runway_id"]
            pair_dict["base_lat"] = base["lat"]
            pair_dict["base_lon"] = base["lon"]
            pair_dict["base_displaced"] = base["displaced_threshold"]
            pair_dict["reciprocal_id"] = reciprocal["runway_id"]
            pair_dict["reciprocal_lat"] = reciprocal["lat"]
            pair_dict["reciprocal_lon"] = reciprocal["lon"]
            pair_dict["reciprocal_displaced"] = reciprocal["displaced_threshold"]
            result.append(pair_dict)
        return result

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
