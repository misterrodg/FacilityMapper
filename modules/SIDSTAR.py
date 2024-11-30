from modules.DrawHelper import (
    ARC_MIN,
    haversine_great_circle_bearing,
    inverse_bearing,
    lat_lon_from_pbd,
)
from modules.ErrorHelper import print_top_level
from modules.GeoJSON import (
    Coordinate,
    Feature,
    FeatureCollection,
    GeoJSON,
    LineString,
    MultiLineString,
)
from modules.QueryHandler import query_db
from modules.QueryHelper import filter_query, translate_wildcard, segment_query
from modules.SIDSTARQueries import select_procedure_points
from modules.SymbolDraw import SymbolDraw
from modules.TextDraw import TextDraw
from modules.vNAS import LINE_STYLES

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
        self.line_buffer = None
        self.core: list[dict] = []
        self.draw_enroute_transitions = True
        self.enroute_transitions: list[dict] = []
        self.draw_runway_transitions = False
        self.runway_transitions: list[dict] = []
        self.file_name = None
        self.db_cursor = db_cursor
        self.is_valid = False

        self._validate(definition_dict)
        self._process()

        if self.is_valid:
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

        line_buffer = definition_dict.get("line_buffer", 1.5)

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
        self.line_buffer = line_buffer
        self.draw_enroute_transitions = draw_enroute_transitions
        self.draw_runway_transitions = draw_runway_transitions
        self.file_name = file_name
        self.is_valid = True
        return

    def _process(self) -> None:
        core_query = self._to_query()
        self.core = query_db(self.db_cursor, core_query)
        if self.draw_enroute_transitions:
            enroute_transition_query = self._to_query("enroute")
            self.enroute_transitions = query_db(
                self.db_cursor, enroute_transition_query
            )
        if self.draw_runway_transitions:
            runway_transitions_query = self._to_query("runway")
            self.runway_transitions = query_db(self.db_cursor, runway_transitions_query)

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

    def _to_query(self, segment: str = "") -> str:
        fac_id = f"'{self.airport_id}'"
        fac_sub_code = self._map_type_to_fac_sub_code()
        procedure_id = f"'{translate_wildcard(self.procedure_id)}'"
        route_type_list = self._get_route_type_list(segment)
        route_type_string = ",".join(f"'{str(x)}'" for x in route_type_list)
        result = select_procedure_points(
            fac_id, fac_sub_code, procedure_id, route_type_string
        )
        return result

    def _get_line_strings(self, rows: list) -> MultiLineString:
        segment_list = segment_query(rows, "transition_id")
        multi_line_string = MultiLineString()
        for segment_item in segment_list:
            line_string = LineString()
            for segment in segment_item:
                coordinate = Coordinate(segment.get("lat"), segment.get("lon"))
                line_string.add_coordinate(coordinate)
            multi_line_string.add_line_string(line_string)
        return multi_line_string

    def _get_truncated_line_strings(self, rows: list) -> MultiLineString:
        segment_list = segment_query(rows, "transition_id")
        multi_line_string = MultiLineString()
        for segment_item in segment_list:
            if len(segment_item) > 1:
                for from_point, to_point in zip(segment_item, segment_item[1:]):
                    line_string = LineString()
                    bearing = haversine_great_circle_bearing(
                        from_point.get("lat"),
                        from_point.get("lon"),
                        to_point.get("lat"),
                        to_point.get("lon"),
                    )
                    new_from = lat_lon_from_pbd(
                        from_point.get("lat"),
                        from_point.get("lon"),
                        bearing,
                        self.symbol_scale,
                    )
                    inverse = inverse_bearing(bearing)
                    new_to = lat_lon_from_pbd(
                        to_point.get("lat"),
                        to_point.get("lon"),
                        inverse,
                        self.symbol_scale,
                    )
                    coordinate = Coordinate(new_from.get("lat"), new_from.get("lon"))
                    line_string.add_coordinate(coordinate)
                    coordinate = Coordinate(new_to.get("lat"), new_to.get("lon"))
                    line_string.add_coordinate(coordinate)
                    multi_line_string.add_line_string(line_string)
        return multi_line_string

    def _get_arrow_line_features(self, rows: list) -> list[Feature]:
        selected_route_types = self._get_selected_route_types()
        start_types = selected_route_types[:2]
        end_types = selected_route_types[-2:]
        segment_list = segment_query(rows, "transition_id")
        result = []
        for segment_item in segment_list:
            if len(segment_item) > 1:
                for index, (from_point, to_point) in enumerate(
                    zip(segment_item, segment_item[1:])
                ):
                    bearing = haversine_great_circle_bearing(
                        from_point.get("lat"),
                        from_point.get("lon"),
                        to_point.get("lat"),
                        to_point.get("lon"),
                    )
                    arrow_head = SymbolDraw(
                        "ARROW_HEAD",
                        from_point.get("lat"),
                        from_point.get("lon"),
                        bearing,
                        self.symbol_scale,
                    )
                    result.append(arrow_head.get_feature())
                    arrow_tail = SymbolDraw(
                        "ARROW_TAIL",
                        to_point.get("lat"),
                        to_point.get("lon"),
                        bearing,
                        self.symbol_scale,
                    )
                    result.append(arrow_tail.get_feature())
                    if index == 0 and from_point.get("route_type") in start_types:
                        circle = SymbolDraw(
                            "CIRCLE_S",
                            from_point.get("lat"),
                            from_point.get("lon"),
                            0,
                            self.symbol_scale,
                        )
                        result.append(circle.get_feature())
                    if (
                        index == len(segment_item) - 2
                        and to_point.get("route_type") in end_types
                    ):
                        arrow_head = SymbolDraw(
                            "ARROW_HEAD_HOLLOW",
                            to_point.get("lat"),
                            to_point.get("lon"),
                            bearing,
                            self.symbol_scale,
                        )
                        result.append(arrow_head.get_feature())
        return result

    def _get_text_features(self, rows: list) -> list[Feature]:
        filtered_rows = filter_query(rows, "fix_id")
        result = []
        for row in filtered_rows:
            offset_lat = self.y_offset + row["lat"]
            offset_lon = self.x_offset + row["lon"]
            text_draw = TextDraw(row["fix_id"], offset_lat, offset_lon, self.text_scale)
            result.append(text_draw.get_feature())
            lines_used = 1

            if self.draw_altitudes:
                if (
                    row["altitude"]
                    or row["flight_level"]
                    or row["altitude_2"]
                    or row["flight_level_2"]
                ):
                    alt_desc = row["alt_desc"]
                    if row["altitude"] or row["flight_level"]:
                        offset_lat = (
                            self.y_offset
                            + row["lat"]
                            - (self.line_buffer * lines_used * ARC_MIN)
                        )
                        offset_lon = self.x_offset + row["lon"]
                        altitude_value = (
                            row["altitude"]
                            if row["altitude"]
                            else f"FL{row["flight_level"]}"
                        )
                        altitude_value = (
                            f"{alt_desc}{altitude_value}"
                            if alt_desc in ["+", "-"]
                            else altitude_value
                        )
                        text_draw = TextDraw(
                            str(altitude_value), offset_lat, offset_lon, self.text_scale
                        )
                        result.append(text_draw.get_feature())
                        lines_used += 1
                    if row["altitude_2"] or row["flight_level_2"]:
                        offset_lat = (
                            self.y_offset
                            + row["lat"]
                            - (self.line_buffer * lines_used * ARC_MIN)
                        )
                        offset_lon = self.x_offset + row["lon"]
                        altitude_value = (
                            row["altitude_2"]
                            if row["altitude_2"]
                            else f"FL{row["flight_level_2"]}"
                        )
                        text_draw = TextDraw(
                            str(altitude_value), offset_lat, offset_lon, self.text_scale
                        )
                        result.append(text_draw.get_feature())
                        lines_used += 1

            if self.draw_speeds:
                if row["speed_limit"]:
                    offset_lat = (
                        self.y_offset
                        + row["lat"]
                        - (self.line_buffer * lines_used * ARC_MIN)
                    )
                    offset_lon = self.x_offset + row["lon"]
                    text_draw = TextDraw(
                        str(row["speed_limit"]),
                        offset_lat,
                        offset_lon,
                        self.text_scale,
                    )
                    result.append(text_draw.get_feature())
        return result

    def _get_symbol_features(self, rows: list) -> list[Feature]:
        filtered_rows = filter_query(rows, "fix_id")
        result = []
        for row in filtered_rows:
            if row["type"] == "W":
                symbol_draw = SymbolDraw(
                    "RNAV", row["lat"], row["lon"], symbol_scale=self.symbol_scale
                )
                result.append(symbol_draw.get_feature())
            if row["type"] in ["C", "R"]:
                symbol_draw = SymbolDraw(
                    "TRIANGLE", row["lat"], row["lon"], symbol_scale=self.symbol_scale
                )
                result.append(symbol_draw.get_feature())
            if row["type"] == "VORDME":
                symbol_draw = SymbolDraw(
                    "DME_BOX", row["lat"], row["lon"], symbol_scale=self.symbol_scale
                )
                result.append(symbol_draw.get_feature())
                symbol_draw = SymbolDraw(
                    "HEXAGON", row["lat"], row["lon"], symbol_scale=self.symbol_scale
                )
                result.append(symbol_draw.get_feature())
            if row["type"] == "VOR":
                symbol_draw = SymbolDraw(
                    "HEXAGON", row["lat"], row["lon"], symbol_scale=self.symbol_scale
                )
                result.append(symbol_draw.get_feature())
            if row["type"] == "DME":
                symbol_draw = SymbolDraw(
                    "DME_BOX", row["lat"], row["lon"], symbol_scale=self.symbol_scale
                )
                result.append(symbol_draw.get_feature())
            if row["type"] == "NDB":
                symbol_draw = SymbolDraw(
                    "CIRCLE_L", row["lat"], row["lon"], symbol_scale=self.symbol_scale
                )
                result.append(symbol_draw.get_feature())
        return result

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        if self.line_style == "arrows":
            feature_array = self._get_arrow_line_features(
                self.runway_transitions + self.core + self.enroute_transitions
            )
            for feature in feature_array:
                feature_collection.add_feature(feature)

        if self.line_style not in ["none", "arrows"]:
            if self.draw_symbols:
                multi_line_string = self._get_truncated_line_strings(
                    self.runway_transitions + self.core + self.enroute_transitions
                )
            else:
                multi_line_string = self._get_line_strings(
                    self.runway_transitions + self.core + self.enroute_transitions
                )

            feature = Feature()
            feature.add_multi_line_string(multi_line_string)

            feature_collection.add_feature(feature)

        if self.draw_names:
            feature_array = self._get_text_features(
                self.runway_transitions + self.core + self.enroute_transitions
            )
            for feature in feature_array:
                feature_collection.add_feature(feature)

        if self.draw_symbols:
            feature_array = self._get_symbol_features(
                self.runway_transitions + self.core + self.enroute_transitions
            )
            for feature in feature_array:
                feature_collection.add_feature(feature)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return
