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
from modules.procedure.procedure_options import SymbolOptions, TextOptions
from modules.query_handler import query_db

from sqlite3 import Cursor

ERROR_HEADER = "VECTORSID: "


class VectorSID:
    map_type: str
    airport_id: str
    procedure_id: str
    draw_names: bool
    draw_symbols: bool
    x_offset: float
    y_offset: float
    symbol_scale: float
    text_scale: float
    line_height: float
    leading: JoinedProcedureRecords
    trailing: JoinedProcedureRecords
    file_name: str
    db_cursor: Cursor
    is_valid: bool

    def __init__(self, db_cursor: Cursor, definition_dict: dict[str, object]):
        self.map_type = "VECTORSID"
        self.airport_id = ""
        self.procedure_id = ""
        self.draw_names = False
        self.draw_symbols = False
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.symbol_scale = 1.0
        self.text_scale = 1.0
        self.line_height = 1.5 * self.text_scale
        self.leading = JoinedProcedureRecords([])
        self.trailing = JoinedProcedureRecords([])
        self.file_name = ""
        self.db_cursor = db_cursor
        self.is_valid = False

        self._validate(definition_dict)

        if self.is_valid:
            self._process()
            self._to_file()

    def _validate(self, definition_dict: dict[str, object]) -> None:
        airport_id = definition_dict.get("airport_id")
        if not isinstance(airport_id, str):
            print(
                f"{ERROR_HEADER}Invalid `airport_id` in:\n{print_top_level(definition_dict)}."
            )
            return

        procedure_id = definition_dict.get("procedure_id")
        if not isinstance(procedure_id, str):
            print(
                f"{ERROR_HEADER}Invalid `procedure_id` in:\n{print_top_level(definition_dict)}."
            )
            return

        draw_names = definition_dict.get("draw_names", True)
        if not isinstance(draw_names, bool):
            draw_names = True

        draw_symbols = definition_dict.get("draw_symbols", True)
        if not isinstance(draw_symbols, bool):
            draw_symbols = True

        x_offset = definition_dict.get("x_offset", 0)
        if not isinstance(x_offset, (int, float)):
            x_offset = 0.0

        y_offset = definition_dict.get("y_offset", 0)
        if not isinstance(y_offset, (int, float)):
            y_offset = 0.0

        symbol_scale = definition_dict.get("symbol_scale", 1.0)
        if not isinstance(symbol_scale, (int, float)):
            symbol_scale = 1.0

        text_scale = definition_dict.get("text_scale", 1.0)
        if not isinstance(text_scale, (int, float)):
            text_scale = 1.0

        line_height = definition_dict.get("line_height", 1.5 * text_scale)
        if not isinstance(line_height, (int, float)):
            line_height = 1.5 * text_scale

        file_name = definition_dict.get("file_name")
        if not isinstance(file_name, str):
            file_name = f"{airport_id}_{self.map_type}_{procedure_id}"

        self.airport_id = airport_id
        self.procedure_id = procedure_id
        self.draw_symbols = draw_symbols
        self.draw_names = draw_names
        self.x_offset = float(x_offset) * ARC_MIN
        self.y_offset = float(y_offset) * ARC_MIN
        self.symbol_scale = float(symbol_scale)
        self.text_scale = float(text_scale)
        self.line_height = float(line_height)
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
                joined_procedure_records_list, SymbolOptions(True, self.symbol_scale)
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
                TextOptions(
                    self.draw_names,
                    False,
                    False,
                    True,
                    self.x_offset,
                    self.y_offset,
                    self.text_scale,
                    self.line_height,
                ),
            )
            result.extend(features)

        return result
