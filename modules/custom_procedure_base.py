from modules.definitions.procedure import (
    CORE,
    LEADING,
    PROCEDURE_SEGMENTS,
    PROCEDURE_TYPES,
    TRAILING,
)
from modules.error_helper import print_top_level
from modules.geo_json import Feature
from modules.procedure import (
    LineOptions,
    ProcedurePoint,
    ProcedurePoints,
    SymbolOptions,
    TextOptions,
    get_line_feature,
    get_symbol_features,
    get_text_features,
)

ERROR_HEADER = "Custom Procedure: "


class CustomProcedureBase:
    procedure_type: str
    draw_names: bool
    draw_altitudes: bool
    draw_speeds: bool
    draw_symbols: bool
    append_name: str
    leading_segments: list[ProcedurePoints]
    core_segment: ProcedurePoints
    trailing_segments: list[ProcedurePoints]
    file_name: str
    base_valid: bool

    def __init__(self, definition_dict: dict[str, object]):
        self.procedure_type = ""
        self.draw_names = False
        self.draw_altitudes = False
        self.draw_speeds = False
        self.draw_symbols = False
        self.append_name = ""
        self.leading_segments = []
        self.core_segment = ProcedurePoints([])
        self.trailing_segments = []
        self.file_name = ""
        self.base_valid = False

        self._base_validate(definition_dict)

    def _parse_point(
        self, point: dict[str, object], field_label: str
    ) -> ProcedurePoint | None:
        fix_id = point.get("fix_id")
        if not isinstance(fix_id, str):
            fix_id = point.get("id")
        if not isinstance(fix_id, str):
            print(
                f"{ERROR_HEADER}Invalid `{field_label}` point `fix_id` in:\n{print_top_level(point)}."
            )
            return None

        fix_lat = point.get("fix_lat")
        if not isinstance(fix_lat, (int, float)):
            fix_lat = point.get("lat")
        if not isinstance(fix_lat, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `{field_label}` point `fix_lat` in:\n{print_top_level(point)}."
            )
            return None

        fix_lon = point.get("fix_lon")
        if not isinstance(fix_lon, (int, float)):
            fix_lon = point.get("lon")
        if not isinstance(fix_lon, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `{field_label}` point `fix_lon` in:\n{print_top_level(point)}."
            )
            return None

        symbol_name = point.get("symbol_name")
        if symbol_name is not None and not isinstance(symbol_name, str):
            symbol_name = None

        procedure_id = point.get("procedure_id")
        if procedure_id is not None and not isinstance(procedure_id, str):
            procedure_id = None

        procedure_type = point.get("procedure_type")
        if procedure_type is not None and not isinstance(procedure_type, str):
            procedure_type = None

        path_term = point.get("path_term")
        if path_term is not None and not isinstance(path_term, str):
            path_term = None

        course = point.get("course")
        if course is not None and not isinstance(course, (int, float)):
            course = None

        center_fix = point.get("center_fix")
        if center_fix is not None and not isinstance(center_fix, str):
            center_fix = None

        center_lat = point.get("center_lat")
        if center_lat is not None and not isinstance(center_lat, (int, float)):
            center_lat = None

        center_lon = point.get("center_lon")
        if center_lon is not None and not isinstance(center_lon, (int, float)):
            center_lon = None

        arc_radius = point.get("arc_radius")
        if arc_radius is not None and not isinstance(arc_radius, (int, float)):
            arc_radius = None

        turn_direction = point.get("turn_direction")
        if turn_direction is not None and not isinstance(turn_direction, str):
            turn_direction = None

        desc_code = point.get("desc_code")
        if desc_code is not None and not isinstance(desc_code, str):
            desc_code = None

        alt_desc = point.get("alt_desc")
        if alt_desc is not None and not isinstance(alt_desc, str):
            alt_desc = None

        alt_1 = point.get("alt_1")
        if alt_1 is not None and not isinstance(alt_1, int):
            alt_1 = None

        fl_1 = point.get("fl_1")
        if fl_1 is not None and not isinstance(fl_1, bool):
            fl_1 = None

        alt_2 = point.get("alt_2")
        if alt_2 is not None and not isinstance(alt_2, int):
            alt_2 = None

        fl_2 = point.get("fl_2")
        if fl_2 is not None and not isinstance(fl_2, bool):
            fl_2 = None

        speed_desc = point.get("speed_desc")
        if speed_desc is not None and not isinstance(speed_desc, str):
            speed_desc = None

        speed_limit = point.get("speed_limit")
        if speed_limit is not None and not isinstance(speed_limit, int):
            speed_limit = None

        fix_source = point.get("fix_source")
        if fix_source is not None and not isinstance(fix_source, str):
            fix_source = None

        fix_type = point.get("fix_type")
        if fix_type is not None and not isinstance(fix_type, str):
            fix_type = None

        fix_mag_var = point.get("fix_mag_var")
        if fix_mag_var is not None and not isinstance(fix_mag_var, (int, float)):
            fix_mag_var = None

        return ProcedurePoint(
            fix_id=fix_id,
            fix_lat=float(fix_lat),
            fix_lon=float(fix_lon),
            fix_source=fix_source,
            fix_type=fix_type,
            fix_mag_var=(
                float(fix_mag_var) if isinstance(fix_mag_var, (int, float)) else None
            ),
            symbol_name=symbol_name,
            procedure_id=procedure_id,
            procedure_type=procedure_type,
            path_term=path_term,
            course=float(course) if isinstance(course, (int, float)) else None,
            center_fix=center_fix,
            center_lat=(
                float(center_lat) if isinstance(center_lat, (int, float)) else None
            ),
            center_lon=(
                float(center_lon) if isinstance(center_lon, (int, float)) else None
            ),
            arc_radius=(
                float(arc_radius) if isinstance(arc_radius, (int, float)) else None
            ),
            turn_direction=turn_direction,
            desc_code=desc_code,
            alt_desc=alt_desc,
            alt_1=alt_1,
            fl_1=fl_1,
            alt_2=alt_2,
            fl_2=fl_2,
            speed_desc=speed_desc,
            speed_limit=speed_limit,
        )

    def _parse_path(
        self, path: list[dict[str, object]], field_label: str
    ) -> ProcedurePoints | None:
        points: list[ProcedurePoint] = []
        for point in path:
            point_data = self._parse_point(point, field_label)
            if point_data is None:
                return None
            points.append(point_data)
        return ProcedurePoints.from_point_list(points)

    def _base_validate(self, definition_dict: dict[str, object]) -> None:
        procedure_type = definition_dict.get("procedure_type")
        if not isinstance(procedure_type, str):
            print(
                f"{ERROR_HEADER}Invalid `procedure_type` in:\n{print_top_level(definition_dict)}."
            )
            return
        if procedure_type not in PROCEDURE_TYPES:
            print(f"{ERROR_HEADER}procedure_type '{procedure_type}' not recognized.")
            print(f"{ERROR_HEADER}Supported types are {", ".join(PROCEDURE_TYPES)}.")
            return

        draw_names = definition_dict.get("draw_names", False)
        if not isinstance(draw_names, bool):
            draw_names = False

        draw_altitudes = definition_dict.get("draw_altitudes", False)
        if not isinstance(draw_altitudes, bool):
            draw_altitudes = False

        draw_speeds = definition_dict.get("draw_speeds", False)
        if not isinstance(draw_speeds, bool):
            draw_speeds = False

        draw_symbols = definition_dict.get("draw_symbols", False)
        if not isinstance(draw_symbols, bool):
            draw_symbols = False

        append_name = definition_dict.get("append_name")
        if not isinstance(append_name, str) or append_name not in PROCEDURE_SEGMENTS:
            append_name = ""

        leading_segments = definition_dict.get("leading_segments", [])
        if not isinstance(leading_segments, list):
            print(
                f"{ERROR_HEADER}Invalid `leading_segments` in:\n{print_top_level(definition_dict)}."
            )
            return
        parsed_leading: list[ProcedurePoints] = []
        for index, segment in enumerate(leading_segments):
            if not isinstance(segment, list):
                print(
                    f"{ERROR_HEADER}Invalid `leading_segments[{index}]` in:\n{print_top_level(definition_dict)}."
                )
                return
            if not all(isinstance(item, dict) for item in segment):
                print(
                    f"{ERROR_HEADER}Invalid `leading_segments[{index}]` in:\n{print_top_level(definition_dict)}."
                )
                return
            parsed_segment = self._parse_path(segment, f"leading_segments[{index}]")
            if parsed_segment is None:
                return
            parsed_leading.append(parsed_segment)

        core_segment = definition_dict.get("core_segment", [])
        if not isinstance(core_segment, list):
            print(
                f"{ERROR_HEADER}Invalid `core_segment` in:\n{print_top_level(definition_dict)}."
            )
            return
        if not all(isinstance(item, dict) for item in core_segment):
            print(
                f"{ERROR_HEADER}Invalid `core_segment` in:\n{print_top_level(definition_dict)}."
            )
            return
        parsed_core = self._parse_path(core_segment, "core_segment")
        if parsed_core is None:
            return

        trailing_segments = definition_dict.get("trailing_segments", [])
        if not isinstance(trailing_segments, list):
            print(
                f"{ERROR_HEADER}Invalid `trailing_segments` in:\n{print_top_level(definition_dict)}."
            )
            return
        parsed_trailing: list[ProcedurePoints] = []
        for index, segment in enumerate(trailing_segments):
            if not isinstance(segment, list):
                print(
                    f"{ERROR_HEADER}Invalid `trailing_segments[{index}]` in:\n{print_top_level(definition_dict)}."
                )
                return
            if not all(isinstance(item, dict) for item in segment):
                print(
                    f"{ERROR_HEADER}Invalid `trailing_segments[{index}]` in:\n{print_top_level(definition_dict)}."
                )
                return
            parsed_segment = self._parse_path(segment, f"trailing_segments[{index}]")
            if parsed_segment is None:
                return
            parsed_trailing.append(parsed_segment)

        file_name = definition_dict.get("file_name")
        if not isinstance(file_name, str):
            print(
                f"{ERROR_HEADER}Invalid `file_name` in:\n{print_top_level(definition_dict)}."
            )
            return

        self.procedure_type = procedure_type
        self.draw_names = draw_names
        self.draw_altitudes = draw_altitudes
        self.draw_speeds = draw_speeds
        self.draw_symbols = draw_symbols
        self.append_name = append_name
        self.leading_segments = parsed_leading
        self.core_segment = parsed_core
        self.trailing_segments = parsed_trailing

        self.file_name = file_name
        self.base_valid = True
        return

    def _process(self) -> None:
        if self.append_name and self.procedure_type in ("SID", "STAR"):
            self._append_name()
        return

    def _draw_lines(self, line_options: LineOptions | None = None) -> Feature:
        if line_options is None:
            line_options = LineOptions()

        if not self.draw_symbols:
            line_options.buffer_length = 0.0

        result = Feature()
        joined_procedure_records_tuples_list: list[tuple[ProcedurePoints, bool]] = []
        if self.core_segment:
            joined_procedure_records_tuples_list.append((self.core_segment, False))

        for segment in self.leading_segments:
            if segment:
                joined_procedure_records_tuples_list.append((segment, True))

        for segment in self.trailing_segments:
            if segment:
                joined_procedure_records_tuples_list.append((segment, True))

        if joined_procedure_records_tuples_list:
            result = get_line_feature(
                joined_procedure_records_tuples_list, line_options
            )

        return result

    def _draw_symbols(
        self, symbol_options: SymbolOptions | None = None
    ) -> list[Feature]:
        if symbol_options is None:
            symbol_options = SymbolOptions()

        result = []
        joined_procedure_records_list: list[ProcedurePoints] = []
        if self.core_segment:
            joined_procedure_records_list.append(self.core_segment)

        for segment in self.leading_segments:
            if segment:
                joined_procedure_records_list.append(segment)

        for segment in self.trailing_segments:
            if segment:
                joined_procedure_records_list.append(segment)

        if joined_procedure_records_list:
            features = get_symbol_features(
                joined_procedure_records_list, symbol_options
            )
            result.extend(features)

        return result

    def _draw_text(self, text_options: TextOptions | None = None) -> list[Feature]:
        if text_options is None:
            text_options = TextOptions()

        result = []
        joined_procedure_records_list: list[ProcedurePoints] = []
        if self.core_segment:
            joined_procedure_records_list.append(self.core_segment)

        for segment in self.leading_segments:
            if segment:
                joined_procedure_records_list.append(segment)

        for segment in self.trailing_segments:
            if segment:
                joined_procedure_records_list.append(segment)

        if joined_procedure_records_list:
            features = get_text_features(joined_procedure_records_list, text_options)
            result.extend(features)
        return result

    def _append_name(self) -> None:
        if self.procedure_type == "SID":
            if self.trailing_segments and self.append_name == TRAILING:
                for segment in self.trailing_segments:
                    if segment:
                        segment.add_procedure_name_to_enroute_transitions()
            elif self.core_segment.records and self.append_name == CORE:
                self.core_segment.add_procedure_name_to_core(True)
            elif self.leading_segments and self.append_name == LEADING:
                for segment in self.leading_segments:
                    if segment:
                        segment.add_procedure_name_to_runway_transitions()

        if self.procedure_type == "STAR":
            if self.leading_segments and self.append_name == LEADING:
                for segment in self.leading_segments:
                    if segment:
                        segment.add_procedure_name_to_enroute_transitions()
            elif self.core_segment.records and self.append_name == CORE:
                self.core_segment.add_procedure_name_to_core()
            elif self.trailing_segments and self.append_name == TRAILING:
                for segment in self.trailing_segments:
                    if segment:
                        segment.add_procedure_name_to_runway_transitions()

        return
