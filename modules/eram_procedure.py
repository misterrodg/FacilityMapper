from modules.definitions import (
    LineProperties,
    SymbolProperties,
    TextProperties,
    vNASProperties,
)
from modules.geo_json import (
    Coordinate,
    Feature,
    FeatureCollection,
    GeoJSON,
    Point,
    Properties,
)
from modules.procedure import LineOptions
from modules.procedure_base import ProcedureBase

from sqlite3 import Cursor

ERROR_HEADER = "ERAM Procedure: "


class ERAMProcedure(ProcedureBase):
    draw_lines: bool
    suppress_core: bool
    truncation: float
    line_defaults: LineProperties
    symbol_defaults: SymbolProperties
    text_defaults: TextProperties

    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        super().__init__(db_cursor, definition_dict)
        self.draw_lines = True
        self.suppress_core = False
        self.truncation = None
        self.line_defaults = None
        self.symbol_defaults = None
        self.text_defaults = None

        self._validate(definition_dict)

        if self.base_valid and self.is_valid:
            self._process()
            line_options = LineOptions(self.truncation)
            self._to_file(line_options)

    def _validate(self, definition_dict: dict) -> None:
        draw_lines = definition_dict.get("draw_lines", True)
        truncation = definition_dict.get("truncation", 0.0)

        line_defaults = definition_dict.get("line_defaults")
        if draw_lines and not line_defaults:
            print(f"{ERROR_HEADER}line draw specified without line_defaults.")
            return
        if line_defaults:
            line_defaults = LineProperties(line_defaults, True)

        symbol_defaults = definition_dict.get("symbol_defaults")
        if self.draw_symbols and not symbol_defaults:
            print(f"{ERROR_HEADER}draw_symbols specified without symbol_defaults.")
            return
        if symbol_defaults:
            symbol_defaults = SymbolProperties(symbol_defaults, True)

        text_defaults = definition_dict.get("text_defaults")
        if (
            self.draw_names or self.draw_altitudes or self.draw_speeds
        ) and not text_defaults:
            print(f"{ERROR_HEADER}text draw specified without text_defaults.")
            return
        if text_defaults:
            text_defaults = TextProperties(text_defaults, True)

        self.draw_lines = draw_lines
        self.truncation = truncation

        self.line_defaults = line_defaults
        self.symbol_defaults = symbol_defaults
        self.text_defaults = text_defaults
        return

    def _process_defaults(self, defaults: vNASProperties) -> Feature:
        result = Feature()
        default_point = Point()
        default_point.set_coordinate(Coordinate(0, 0))
        properties = Properties()
        properties.from_dict(defaults.to_dict())
        result.add_point(default_point)
        result.add_properties(properties)
        return result

    def _to_file(self, line_options: LineOptions = None) -> None:
        feature_collection = FeatureCollection()

        if self.line_defaults:
            feature = self._process_defaults(self.line_defaults)
            feature_collection.add_feature(feature)

        if self.symbol_defaults:
            feature = self._process_defaults(self.symbol_defaults)
            feature_collection.add_feature(feature)

        if self.text_defaults:
            feature = self._process_defaults(self.text_defaults)
            feature_collection.add_feature(feature)

        if self.draw_lines:
            feature = self._draw_lines(line_options)
            feature_collection.add_feature(feature)

        if self.draw_names or self.draw_altitudes or self.draw_speeds:
            features = self._draw_text()
            feature_collection.add_features(features)

        if self.draw_symbols:
            features = self._draw_symbols()
            feature_collection.add_features(features)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
