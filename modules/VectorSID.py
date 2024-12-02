from modules.DrawHelper import ARC_MIN
from modules.ErrorHelper import print_top_level
from modules.GeoJSON import FeatureCollection, GeoJSON
from modules.QueryHandler import query_db
from modules.QueryHelper import translate_wildcard
from modules.VectorSIDQueries import select_procedure_points
from modules.SymbolHandler import get_symbol_features
from modules.TextHandler import get_text_features

from sqlite3 import Cursor

ERROR_HEADER = "VECTORSID: "


class VectorSID:
    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.map_type = "VECTORSID"
        self.airport_id = None
        self.procedure_id = None
        self.draw_symbols = False
        self.symbol_scale = None
        self.draw_names = False
        self.x_offset = None
        self.y_offset = None
        self.text_scale = None
        self.line_height = None
        self.core: list[dict] = []
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

        procedure_id = definition_dict.get("procedure_id")
        if procedure_id is None:
            print(
                f"{ERROR_HEADER}Missing `procedure_id` in:\n{print_top_level(definition_dict)}."
            )
            return

        draw_symbols = definition_dict.get("draw_symbols", True)
        symbol_scale = definition_dict.get("symbol_scale", 1.0)
        draw_names = definition_dict.get("draw_names", True)
        x_offset = definition_dict.get("x_offset", 0) * ARC_MIN
        y_offset = definition_dict.get("y_offset", 0) * ARC_MIN
        text_scale = definition_dict.get("text_scale", 1.0)
        line_height = definition_dict.get("line_height", 1.5 * text_scale)
        file_name = definition_dict.get("file_name")
        if file_name is None:
            file_name = f"{airport_id}_{self.map_type}_{procedure_id}"

        self.airport_id = airport_id
        self.procedure_id = procedure_id
        self.draw_symbols = draw_symbols
        self.symbol_scale = symbol_scale
        self.draw_names = draw_names
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.text_scale = text_scale
        self.line_height = line_height
        self.file_name = file_name
        self.is_valid = True
        return

    def _process(self) -> None:
        core_query = self._build_query_string()
        self.core = query_db(self.db_cursor, core_query)

    def _build_query_string(self) -> str:
        fac_id = f"'{self.airport_id}'"
        procedure_id = f"'{translate_wildcard(self.procedure_id)}'"
        result = select_procedure_points(fac_id, procedure_id)
        return result

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        if self.draw_names:
            feature_list = get_text_features(
                self.core,
                self.x_offset,
                self.y_offset,
                self.text_scale,
                self.line_height,
            )
            feature_collection.add_features(feature_list)

        if self.draw_symbols:
            feature_list = get_symbol_features(
                self.core,
                self.symbol_scale,
            )
            feature_collection.add_features(feature_list)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
