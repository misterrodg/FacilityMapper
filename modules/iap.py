from modules.draw_helper import ARC_MIN
from modules.error_helper import print_top_level
from modules.geo_json import FeatureCollection, GeoJSON
from modules.iap_queries import select_procedure_points
from modules.line_handler import get_line_strings
from modules.query_handler import query_db
from modules.symbol_handler import get_symbol_features
from modules.text_handler import get_text_features
from modules.v_nas import LINE_STYLES

from sqlite3 import Cursor

import re

ERROR_HEADER = "IAP: "


class IAP:
    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.map_type: str = "IAP"
        self.airport_id: str = None
        self.procedure_id: str = None
        self.line_style: str = None
        self.draw_symbols: bool = False
        self.symbol_scale: float = None
        self.draw_altitudes: bool = False
        self.draw_speeds: bool = False
        self.draw_names: bool = False
        self.x_offset: float = None
        self.y_offset: float = None
        self.text_scale: float = None
        self.line_height: float = None
        self.core: list[dict] = []
        self.transition_ids: list[str] = []
        self.transitions: list[dict] = []
        self.draw_missed: bool = False
        self.file_name: str = None
        self.db_cursor: Cursor = db_cursor
        self.is_valid: bool = False

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

        line_style = definition_dict.get("line_type", "solid")
        if line_style not in LINE_STYLES:
            print(f"{ERROR_HEADER}line_type '{line_style}' not recognized.")
            print(f"{ERROR_HEADER}Supported types are {", ".join(LINE_STYLES)}.")
            return

        draw_symbols = definition_dict.get("draw_symbols", False)
        symbol_scale = definition_dict.get("symbol_scale", 1.0)
        draw_altitudes = definition_dict.get("draw_altitudes", False)
        draw_speeds = definition_dict.get("draw_speeds", False)
        draw_names = definition_dict.get("draw_names", False)
        x_offset = definition_dict.get("x_offset", 0) * ARC_MIN
        y_offset = definition_dict.get("y_offset", 0) * ARC_MIN
        text_scale = definition_dict.get("text_scale", 1.0)
        line_height = definition_dict.get("line_height", 1.5 * text_scale)
        transition_ids = definition_dict.get("transition_ids", [])
        draw_missed = definition_dict.get("draw_missed", False)

        file_name = definition_dict.get("file_name")
        if file_name is None:
            file_name = f"{airport_id}_{self.map_type}_{procedure_id}"

        self.airport_id = airport_id
        self.procedure_id = procedure_id
        self.line_style = line_style
        self.draw_symbols = draw_symbols
        self.symbol_scale = symbol_scale
        self.draw_altitudes = draw_altitudes
        self.draw_speeds = draw_speeds
        self.draw_names = draw_names
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.text_scale = text_scale
        self.line_height = line_height
        self.transition_ids = transition_ids
        self.draw_missed = draw_missed
        self.file_name = file_name
        self.is_valid = True
        return

    def _process(self) -> None:
        core_query = self._build_query_string()
        core_rows = query_db(self.db_cursor, core_query)
        if not self.draw_missed:
            core_rows = self._remove_missed(core_rows)
        self.core = core_rows
        for transition in self.transition_ids:
            transition_query = self._build_query_string(transition)
            transition_rows = query_db(self.db_cursor, transition_query)
            self.transitions.extend(transition_rows)

    def _remove_missed(self, db_rows: list[dict]) -> list[dict]:
        result = []
        missed_pattern = r"^.{3}M"
        for index, row in enumerate(db_rows):
            if "description_code" in row and re.match(
                missed_pattern, row["description_code"]
            ):
                result = db_rows[: index + 1]
                break
        return result

    def _remove_runway(self, db_rows: list[dict]) -> list[dict]:
        result = db_rows
        for index, row in enumerate(db_rows):
            if "fix_id" in row and row["fix_id"] and row["fix_id"].startswith("RW"):
                result.pop(index)
                break
        return result

    def _build_query_string(self, transition_id: str = "") -> str:
        fac_id = f"'{self.airport_id}'"
        fac_sub_code = "'F'"
        procedure_id = f"'{self.procedure_id}'"
        transition_id_string = "IS NULL"
        if transition_id != "":
            transition_id_string = f"= '{transition_id}'"
        result = select_procedure_points(
            fac_id, fac_sub_code, procedure_id, transition_id_string
        )
        return result

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        if self.line_style != "none":
            if self.draw_symbols:
                feature = get_line_strings(
                    self.core + self.transitions,
                    self.line_style,
                    True,
                    self.symbol_scale,
                )
            else:
                feature = get_line_strings(
                    self.core + self.transitions,
                    self.line_style,
                )
            feature_collection.add_feature(feature)

        if self.draw_names:
            core = self.core
            core = self._remove_runway(core)
            feature_list = get_text_features(
                core + self.transitions,
                self.x_offset,
                self.y_offset,
                self.text_scale,
                self.line_height,
                self.draw_altitudes,
                self.draw_speeds,
            )
            feature_collection.add_features(feature_list)

        if self.draw_symbols:
            feature_list = get_symbol_features(
                self.core + self.transitions,
                self.symbol_scale,
            )
            feature_collection.add_features(feature_list)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
