from modules.db.joined_procedure_records import (
    JoinedProcedureRecords,
    select_joined_procedure_points,
)
from modules.draw import ARC_MIN
from modules.error_helper import print_top_level
from modules.geo_json import (
    Feature,
    FeatureCollection,
    GeoJSON,
)
from modules.procedure import (
    get_symbol_features,
    get_text_features,
)
from modules.query_handler import query_db

from sqlite3 import Cursor

ERROR_HEADER = "VECTORSID: "


class VectorSID:
    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.map_type: str = "VECTORSID"
        self.airport_id: str = None
        self.procedure_id: str = None
        self.draw_names: bool = False
        self.draw_symbols: bool = False
        self.x_offset: float = None
        self.y_offset: float = None
        self.symbol_scale: float = None
        self.text_scale: float = None
        self.line_height: float = None
        self.file_name: str = None
        self.db_cursor: Cursor = db_cursor
        self.is_valid: bool = False

        self.leading: JoinedProcedureRecords = None
        self.trailing: JoinedProcedureRecords = None

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

        procedure_id = definition_dict.get("procedure_id")
        if procedure_id is None:
            print(
                f"{ERROR_HEADER}Missing `procedure_id` in:\n{print_top_level(definition_dict)}."
            )
            return

        draw_names = definition_dict.get("draw_names", True)
        draw_symbols = definition_dict.get("draw_symbols", True)
        x_offset = definition_dict.get("x_offset", 0) * ARC_MIN
        y_offset = definition_dict.get("y_offset", 0) * ARC_MIN
        symbol_scale = definition_dict.get("symbol_scale", 1.0)
        text_scale = definition_dict.get("text_scale", 1.0)
        line_height = definition_dict.get("line_height", 1.5 * text_scale)

        file_name = definition_dict.get("file_name")
        if file_name is None:
            file_name = f"{airport_id}_{self.map_type}_{procedure_id}"

        self.airport_id = airport_id
        self.procedure_id = procedure_id
        self.draw_symbols = draw_symbols
        self.draw_names = draw_names
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.symbol_scale = symbol_scale
        self.text_scale = text_scale
        self.line_height = line_height
        self.file_name = file_name
        self.is_valid = True
        return

    def _process(self) -> None:
        self.leading = self._retrieve_records("T")
        self.trailing = self._retrieve_records("V")
        return

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        if self.draw_names:
            features = self._draw_text()
            feature_collection.add_features(features)

        if self.draw_symbols:
            features = self._draw_symbols()
            feature_collection.add_features(features)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return

    def _retrieve_records(self, procedure_type: str) -> JoinedProcedureRecords:
        query_string = select_joined_procedure_points(
            self.airport_id,
            "D",
            self.procedure_id,
            transitions=["ALL"],
            procedure_types=[procedure_type],
        )
        query_result = query_db(self.db_cursor, query_string)
        result = JoinedProcedureRecords(query_result)
        return result

    def _draw_symbols(self) -> list[Feature]:
        result = []
        joined_procedure_records_list = []

        if self.leading:
            joined_procedure_records_list.append(self.leading)

        if self.trailing:
            joined_procedure_records_list.append(self.trailing)

        if joined_procedure_records_list:
            features = get_symbol_features(
                joined_procedure_records_list, True, self.symbol_scale
            )
            result.extend(features)

        return result

    def _draw_text(self) -> list[Feature]:
        result = []
        joined_procedure_records_list = []

        if self.leading:
            joined_procedure_records_list.append(self.leading)

        if self.trailing:
            joined_procedure_records_list.append(self.trailing)

        if joined_procedure_records_list:
            features = get_text_features(
                joined_procedure_records_list,
                self.draw_names,
                False,
                False,
                True,
                self.x_offset,
                self.y_offset,
                self.text_scale,
                self.line_height,
            )
            result.extend(features)

        return result
