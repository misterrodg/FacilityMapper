from modules.db import translate_wildcard
from modules.draw_helper import ARC_MIN
from modules.error_helper import print_top_level
from modules.geo_json import FeatureCollection, GeoJSON
from modules.line_handler import get_line_strings
from modules.query_handler import query_db
from modules.sidstar_queries import select_procedure_points
from modules.symbol_handler import get_arrow_line_symbol_features, get_symbol_features
from modules.text_handler import get_text_features
from modules.v_nas import LINE_STYLES

from sqlite3 import Cursor

ERROR_HEADER = "SID/STAR: "
SIDSTAR_LINE_TYPES = ["none", "arrows"]


class SIDSTAR:
    def __init__(self, db_cursor: Cursor, map_type: str, definition_dict: dict):
        self.map_type = map_type
        self.airport_id = None
        self.procedure_id = None
        self.line_style = None
        self.draw_symbols = False
        self.symbol_scale = None
        self.draw_altitudes = False
        self.draw_speeds = False
        self.draw_names = False
        self.x_offset = None
        self.y_offset = None
        self.text_scale = None
        self.line_height = None
        self.vector_length = None
        self.core: list[dict] = []
        self.draw_enroute_transitions = True
        self.enroute_transitions: list[dict] = []
        self.draw_runway_transitions = False
        self.runway_transitions: list[dict] = []
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

        line_style = definition_dict.get("line_type", "solid")
        available_styles = SIDSTAR_LINE_TYPES + LINE_STYLES
        if line_style not in available_styles:
            print(f"{ERROR_HEADER}line_type '{line_style}' not recognized.")
            print(f"{ERROR_HEADER}Supported types are {", ".join(available_styles)}.")
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
        vector_length = definition_dict.get("vector_length", 2.5)
        draw_enroute_transitions = definition_dict.get("draw_enroute_transitions", True)
        draw_runway_transitions = definition_dict.get("draw_runway_transitions", False)
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
        self.vector_length = vector_length
        self.draw_enroute_transitions = draw_enroute_transitions
        self.draw_runway_transitions = draw_runway_transitions
        self.file_name = file_name
        self.is_valid = True
        return

    def _process(self) -> None:
        core_query = self._build_query_string()
        self.core = query_db(self.db_cursor, core_query)
        if self.draw_enroute_transitions:
            enroute_transition_query = self._build_query_string("enroute")
            self.enroute_transitions = query_db(
                self.db_cursor, enroute_transition_query
            )
        if self.draw_runway_transitions:
            runway_transition_query = self._build_query_string("runway")
            self.runway_transitions = query_db(self.db_cursor, runway_transition_query)

    def _map_type_to_fac_sub_code(self) -> str:
        result = ""
        if self.map_type == "SID":
            result = "'D'"
        if self.map_type == "STAR":
            result = "'E'"
        return result

    def _get_route_type_list(self, transition_name: str = "") -> list:
        if self.map_type == "SID":
            if transition_name == "runway":
                return ["1", "4"]
            if transition_name == "enroute":
                return ["3", "6"]
        if self.map_type == "STAR":
            if transition_name == "enroute":
                return ["1", "4"]
            if transition_name == "runway":
                return ["3", "6"]
        return ["2", "5"]

    def _get_selected_route_types(self) -> list:
        result = ["2", "5"]
        if self.map_type == "SID":
            if self.draw_runway_transitions:
                result = ["1", "4"] + result
            if self.draw_enroute_transitions:
                result = result + ["3", "6"]
        if self.map_type == "STAR":
            if self.draw_enroute_transitions:
                result = ["1", "4"] + result
            if self.draw_runway_transitions:
                result = result + ["3", "6"]
        return result
    
    def _get_path_term_list(self) -> list:
        result = ['FM','HA','HF','HM','PI','VM']
        if self.map_type == "STAR":
            result = ['HA','HF','HM','PI']
        return result

    def _build_query_string(self, segment: str = "") -> str:
        fac_id = f"'{self.airport_id}'"
        fac_sub_code = self._map_type_to_fac_sub_code()
        procedure_id = f"'{translate_wildcard(self.procedure_id)}'"
        route_type_list = self._get_route_type_list(segment)
        route_type_string = ",".join(f"'{str(x)}'" for x in route_type_list)
        path_term_list = self._get_path_term_list()
        path_term_string = ",".join(f"'{str(x)}'" for x in path_term_list)
        result = select_procedure_points(
            fac_id, fac_sub_code, procedure_id, route_type_string, path_term_string
        )
        return result

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        if self.line_style == "arrows":
            selected_route_types = self._get_selected_route_types()
            feature_list = get_arrow_line_symbol_features(
                self.runway_transitions + self.core + self.enroute_transitions,
                selected_route_types,
                self.symbol_scale,
            )
            feature_collection.add_features(feature_list)

        if self.line_style not in ["none", "arrows"]:
            if self.draw_symbols:
                feature = get_line_strings(
                    self.runway_transitions + self.core + self.enroute_transitions,
                    self.line_style,
                    self.vector_length,
                    self.symbol_scale,
                    True,
                )
            else:
                feature = get_line_strings(
                    self.runway_transitions + self.core + self.enroute_transitions,
                    self.line_style,
                    self.vector_length,
                )
            feature_collection.add_feature(feature)

        if self.draw_names:
            feature_list = get_text_features(
                self.runway_transitions + self.core + self.enroute_transitions,
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
                self.runway_transitions + self.core + self.enroute_transitions,
                self.symbol_scale,
            )
            feature_collection.add_features(feature_list)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
