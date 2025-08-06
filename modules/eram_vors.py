from modules.db import select_vors_by_ids, VORRecords
from modules.definitions import (
    SymbolProperties,
    TextProperties,
    vNASProperties,
)
from modules.eram_draw import get_symbol_feature, get_text_feature
from modules.error_helper import print_top_level
from modules.geo_json import (
    Coordinate,
    Feature,
    FeatureCollection,
    GeoJSON,
    Point,
    Properties,
)
from modules.query_handler import query_db
from modules.v_nas import SymbolStyle

from sqlite3 import Cursor

ERROR_HEADER = "ERAM VORs: "


class ERAMVOR:
    map_type: str
    vor_ids: list
    draw_symbols: bool
    draw_text: bool
    symbol_defaults: SymbolProperties
    text_defaults: TextProperties
    vor_records: VORRecords
    file_name: str
    db_cursor: Cursor
    is_valid: bool

    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.map_type = "VORS"
        self.vor_ids = []
        self.draw_symbols = True
        self.draw_text = False
        self.symbol_defaults = None
        self.text_defaults = None
        self.vor_records = None
        self.file_name = None
        self.db_cursor = db_cursor
        self.is_valid = False

        self._validate(definition_dict)

        if self.is_valid:
            self._process()
            self._to_file()

    def _validate(self, definition_dict: dict) -> None:
        draw_symbols = definition_dict.get("draw_symbols", True)
        draw_text = definition_dict.get("draw_text", False)
        vor_ids = definition_dict.get("vor_ids")
        if vor_ids is None:
            print(
                f"{ERROR_HEADER}Missing `vor_ids` in:\n{print_top_level(definition_dict)}."
            )
            return

        symbol_defaults = definition_dict.get("symbol_defaults")
        if draw_symbols and not symbol_defaults:
            print(f"{ERROR_HEADER}draw_symbols specified without symbol_defaults.")
            return
        if symbol_defaults:
            symbol_defaults = SymbolProperties(symbol_defaults, True)

        text_defaults = definition_dict.get("text_defaults")
        if draw_text and not text_defaults:
            print(f"{ERROR_HEADER}draw_text specified without text_defaults.")
            return
        if text_defaults:
            text_defaults = TextProperties(text_defaults, True)

        file_name = definition_dict.get("file_name")
        if file_name is None:
            print(
                f"{ERROR_HEADER}Missing `file_name` in:\n{print_top_level(definition_dict)}."
            )
            return

        self.vor_ids = vor_ids
        self.draw_symbols = draw_symbols
        self.draw_text = draw_text
        self.symbol_defaults = symbol_defaults
        self.text_defaults = text_defaults

        self.file_name = file_name
        self.is_valid = True
        return

    def _process(self) -> None:
        query_string = select_vors_by_ids(self.vor_ids)
        query_result = query_db(self.db_cursor, query_string)
        self.vor_records = VORRecords(query_result)
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

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        if self.symbol_defaults:
            feature = self._process_defaults(self.symbol_defaults)
            feature_collection.add_feature(feature)

        if self.text_defaults:
            feature = self._process_defaults(self.text_defaults)
            feature_collection.add_feature(feature)

        records = self.vor_records.get_records()
        for record in records:
            lat = record.dme_lat if not record.lat else record.lat
            lon = record.dme_lon if not record.lon else record.lon
            if lat and lon:
                record_symbol = SymbolStyle.from_type("VHF", record.nav_class)
                symbol_type = None
                if self.symbol_defaults.style != record_symbol.value:
                    symbol_type = record_symbol
                if self.draw_symbols:
                    feature = get_symbol_feature(lat, lon, symbol_type)
                    feature_collection.add_feature(feature)
                if self.draw_text:
                    vhf_id = record.dme_id if not record.vhf_id else record.vhf_id
                    feature = get_text_feature(lat, lon, [vhf_id])
                    feature_collection.add_feature(feature)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
