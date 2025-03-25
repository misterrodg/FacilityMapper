from modules.centerline import CenterlineRunway
from modules.error_helper import print_top_level
from modules.geo_json import Feature, FeatureCollection, GeoJSON, MultiLineString

from sqlite3 import Cursor

ERROR_HEADER = "CENTERLINES: "


class Centerlines:
    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.map_type = "CENTERLINES"
        self.airport_id = None
        self.centerline_list = None
        self.multi_line_strings: list[MultiLineString] = []
        self.file_name = None
        self.db_cursor = db_cursor
        self.is_valid = False

        self._validate(definition_dict)

        if self.is_valid:
            self._to_file()

    def _validate(self, definition_dict: dict) -> None:
        airport_id = definition_dict.get("airport_id")
        if airport_id is None:
            print(
                f"{ERROR_HEADER}Missing `airport_id` in:\n{print_top_level(definition_dict)}."
            )
            return

        centerline_list = definition_dict.get("centerlines")
        if centerline_list is None:
            print(
                f"{ERROR_HEADER}Missing `centerlines` in:\n{print_top_level(definition_dict)}."
            )
            return

        file_name = definition_dict.get("file_name")
        if file_name is None:
            print(
                f"{ERROR_HEADER}Missing `file_name` in:\n{print_top_level(definition_dict)}."
            )
            return

        self.airport_id = airport_id
        self.centerline_list = centerline_list
        self.file_name = file_name
        self.is_valid = True
        return

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        feature = Feature()
        multi_line_string = MultiLineString()

        for runway in self.centerline_list:
            centerline_runway = CenterlineRunway(
                self.db_cursor, self.airport_id, runway
            )
            if centerline_runway.is_valid:
                line_strings = centerline_runway.get_line_strings()
                if line_strings is not None:
                    multi_line_string.add_line_strings(line_strings)

        feature.add_multi_line_string(multi_line_string)
        feature_collection.add_feature(feature)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
