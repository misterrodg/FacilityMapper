from modules.draw import ARC_MIN
from modules.error_helper import print_top_level
from modules.geo_json import (
    FeatureCollection,
    GeoJSON,
)
from modules.procedure import LineOptions, SymbolOptions, TextOptions
from modules.procedure_base import ProcedureBase
from modules.v_nas import LINE_STYLES, LINE_STYLE_NONE, LINE_STYLE_SOLID

from sqlite3 import Cursor

ERROR_HEADER = "STARS Procedure: "


class STARSProcedure(ProcedureBase):
    line_type: str
    x_offset: float
    y_offset: float
    symbol_scale: float
    text_scale: float
    line_height: float
    draw_missed: bool
    vector_length: float
    is_valid: bool

    def __init__(self, db_cursor: Cursor, definition_dict: dict[str, object]):
        super().__init__(db_cursor, definition_dict)
        self.line_type = ""
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.symbol_scale = 1.0
        self.text_scale = 1.0
        self.line_height = 1.5 * self.text_scale
        self.draw_missed = False
        self.vector_length = 2.5
        self.is_valid = False

        self._validate(definition_dict)

        if self.base_valid and self.is_valid:
            self._process()
            line_options = LineOptions(
                self.symbol_scale, self.line_type, self.vector_length
            )
            symbol_options = SymbolOptions(True, self.symbol_scale)
            text_options = TextOptions(
                self.draw_names,
                self.draw_altitudes,
                self.draw_speeds,
                True,
                self.x_offset,
                self.y_offset,
                self.text_scale,
                self.line_height,
            )
            self._to_file(line_options, symbol_options, text_options)

    def _validate(self, definition_dict: dict[str, object]) -> None:
        line_type = definition_dict.get("line_type", LINE_STYLE_SOLID)
        if not isinstance(line_type, str):
            print(
                f"{ERROR_HEADER}Invalid `line_type` in:\n{print_top_level(definition_dict)}."
            )
            return
        if line_type not in LINE_STYLES:
            print(f"{ERROR_HEADER}line_type '{line_type}' not recognized.")
            print(f"{ERROR_HEADER}Supported types are {", ".join(LINE_STYLES)}.")
            return

        x_offset = definition_dict.get("x_offset", 0)
        if not isinstance(x_offset, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `x_offset` in:\n{print_top_level(definition_dict)}."
            )
            return

        y_offset = definition_dict.get("y_offset", 0)
        if not isinstance(y_offset, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `y_offset` in:\n{print_top_level(definition_dict)}."
            )
            return

        symbol_scale = definition_dict.get("symbol_scale", 1.0)
        if not isinstance(symbol_scale, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `symbol_scale` in:\n{print_top_level(definition_dict)}."
            )
            return

        text_scale = definition_dict.get("text_scale", 1.0)
        if not isinstance(text_scale, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `text_scale` in:\n{print_top_level(definition_dict)}."
            )
            return

        line_height = definition_dict.get("line_height", 1.5 * text_scale)
        if not isinstance(line_height, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `line_height` in:\n{print_top_level(definition_dict)}."
            )
            return

        draw_missed = definition_dict.get("draw_missed", False)
        if not isinstance(draw_missed, bool):
            draw_missed = False

        vector_length = definition_dict.get("vector_length", 2.5)
        if not isinstance(vector_length, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `vector_length` in:\n{print_top_level(definition_dict)}."
            )
            return

        self.line_type = line_type
        self.x_offset = float(x_offset) * ARC_MIN
        self.y_offset = float(y_offset) * ARC_MIN
        self.symbol_scale = float(symbol_scale)
        self.text_scale = float(text_scale)
        self.line_height = float(line_height)
        self.draw_missed = draw_missed
        self.vector_length = float(vector_length)

        self.is_valid = True
        return

    def _to_file(
        self,
        line_options: LineOptions | None = None,
        symbol_options: SymbolOptions | None = None,
        text_options: TextOptions | None = None,
    ) -> None:
        feature_collection = FeatureCollection()

        if self.line_type != LINE_STYLE_NONE:
            feature = self._draw_lines(line_options)
            feature_collection.add_feature(feature)

        if self.draw_symbols:
            features = self._draw_symbols(symbol_options)
            feature_collection.add_features(features)

        if self.draw_names or self.draw_altitudes or self.draw_speeds:
            features = self._draw_text(text_options)
            feature_collection.add_features(features)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
