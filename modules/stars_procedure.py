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
    DE_LEADING_PROCEDURE_TYPES,
    DE_CORE_PROCEDURE_TYPES,
    DE_TRAILING_PROCEDURE_TYPES,
    F_LEADING_PROCEDURE_TYPES,
    get_line_feature,
    get_symbol_features,
    get_text_features,
    translate_map_type,
)
from modules.query_handler import query_db
from modules.v_nas import LINE_STYLES

from sqlite3 import Cursor

ERROR_HEADER = "STARS Procedure: "

PROCEDURE_TYPES = ["SID", "STAR", "IAP"]
LEADING = "leading"
CORE = "core"
TRAILING = "trailing"
PROCEDURE_SEGMENTS = [LEADING, CORE, TRAILING]


class STARSProcedure:
    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.airport_id: str = None
        self.sub_code: str = None
        self.procedure_type: str = None
        self.procedure_id: str = None
        self.line_style: str = None
        self.draw_names: bool = False
        self.draw_altitudes: bool = False
        self.draw_speeds: bool = False
        self.draw_symbols: bool = False
        self.append_name: str = None
        self.x_offset: float = None
        self.y_offset: float = None
        self.symbol_scale: float = None
        self.text_scale: float = None
        self.line_height: float = None
        self.leading_transitions: list[str] = []  # Enroute or IAF Transitions
        self.trailing_transitions: list[str] = []  # Runway Transitions
        self.draw_missed: bool = False
        self.file_name: str = None
        self.db_cursor: Cursor = db_cursor
        self.is_valid: bool = False

        self.core: JoinedProcedureRecords = None
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

        procedure_type = definition_dict.get("procedure_type")
        if procedure_type is None:
            print(
                f"{ERROR_HEADER}Missing `procedure_type` in:\n{print_top_level(definition_dict)}."
            )
            return
        if procedure_type not in PROCEDURE_TYPES:
            print(f"{ERROR_HEADER}procedure_type '{procedure_type}' not recognized.")
            print(f"{ERROR_HEADER}Supported types are {", ".join(PROCEDURE_TYPES)}.")
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

        draw_names = definition_dict.get("draw_names", False)
        draw_altitudes = definition_dict.get("draw_altitudes", False)
        draw_speeds = definition_dict.get("draw_speeds", False)
        draw_symbols = definition_dict.get("draw_symbols", False)
        append_name = definition_dict.get("append_name")
        if append_name and append_name not in PROCEDURE_SEGMENTS:
            append_name = None
        x_offset = definition_dict.get("x_offset", 0) * ARC_MIN
        y_offset = definition_dict.get("y_offset", 0) * ARC_MIN
        symbol_scale = definition_dict.get("symbol_scale", 1.0)
        text_scale = definition_dict.get("text_scale", 1.0)
        line_height = definition_dict.get("line_height", 1.5 * text_scale)
        draw_missed = definition_dict.get("draw_missed", False)
        leading_transitions = definition_dict.get("leading_transitions", [])
        trailing_transitions = definition_dict.get("trailing_transitions", [])

        file_name = definition_dict.get("file_name")
        if file_name is None:
            file_name = f"{airport_id}_{self.procedure_type}_{procedure_id}"

        self.airport_id = airport_id
        self.sub_code = translate_map_type(procedure_type)
        self.procedure_type = procedure_type
        self.procedure_id = procedure_id
        self.line_style = line_style
        self.draw_symbols = draw_symbols
        self.draw_altitudes = draw_altitudes
        self.draw_speeds = draw_speeds
        self.draw_names = draw_names
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.symbol_scale = symbol_scale
        self.text_scale = text_scale
        self.line_height = line_height
        self.leading_transitions = leading_transitions
        self.trailing_transitions = trailing_transitions
        self.draw_missed = draw_missed
        self.file_name = file_name
        self.is_valid = True
        return

    def _process_iap(self) -> None:
        core_procedure_type = [self.procedure_id[:1]]
        self.core = self._retrieve_records(procedure_types_list=core_procedure_type)
        self.core.trim_missed(True)

        if self.leading_transitions:
            self.leading = self._retrieve_records(
                self.leading_transitions, F_LEADING_PROCEDURE_TYPES
            )
        return

    def _process_sid_star(self) -> None:
        self.core = self._retrieve_records(procedure_types_list=DE_CORE_PROCEDURE_TYPES)

        if self.leading_transitions:
            self.leading = self._retrieve_records(
                self.leading_transitions, DE_LEADING_PROCEDURE_TYPES
            )

        if self.trailing_transitions:
            self.trailing = self._retrieve_records(
                self.trailing_transitions, DE_TRAILING_PROCEDURE_TYPES
            )
        return

    def _process(self) -> None:
        if self.sub_code == "F":
            self._process_iap()
        else:
            self._process_sid_star()
            if self.append_name:
                self._append_name()
        return

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        if self.line_style != "none":
            feature = self._draw_lines()
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

    def _retrieve_records(
        self, transition_list: list[str] = [], procedure_types_list: list[str] = []
    ) -> JoinedProcedureRecords:
        query_string = select_joined_procedure_points(
            self.airport_id,
            self.sub_code,
            self.procedure_id,
            transitions=transition_list,
            procedure_types=procedure_types_list,
        )
        query_result = query_db(self.db_cursor, query_string)
        result = JoinedProcedureRecords(query_result)
        return result

    def _draw_lines(self) -> Feature:
        result = Feature()
        joined_procedure_records_tuples_list = []
        if self.core:
            joined_procedure_records_tuples_list.append((self.core, False))

        if self.leading:
            joined_procedure_records_tuples_list.append((self.leading, True))

        if self.trailing:
            joined_procedure_records_tuples_list.append((self.trailing, True))

        if joined_procedure_records_tuples_list:
            if self.symbol_scale:
                result = get_line_feature(
                    joined_procedure_records_tuples_list, self.symbol_scale
                )
            else:
                result = get_line_feature(joined_procedure_records_tuples_list)

        return result

    def _draw_symbols(self) -> list[Feature]:
        result = []
        joined_procedure_records_list = []
        if self.core:
            joined_procedure_records_list.append(self.core)

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
        if self.core:
            joined_procedure_records_list.append(self.core)

        if self.leading:
            joined_procedure_records_list.append(self.leading)

        if self.trailing:
            joined_procedure_records_list.append(self.trailing)

        if joined_procedure_records_list:
            features = get_text_features(
                joined_procedure_records_list,
                self.draw_names,
                self.draw_altitudes,
                self.draw_speeds,
                True,
                self.x_offset,
                self.y_offset,
                self.text_scale,
                self.line_height,
            )
            result.extend(features)

        return result

    def _append_name(self) -> None:
        if self.sub_code == "D":
            if self.trailing and self.append_name == TRAILING:
                self.trailing.add_procedure_name_to_enroute_transitions()
            elif self.core.records and self.append_name == CORE:
                self.core.add_procedure_name_to_core(True)
            elif self.leading.records and self.append_name == LEADING:
                self.leading.add_procedure_name_to_runway_transitions()

        if self.sub_code == "E":
            if self.leading and self.append_name == LEADING:
                self.leading.add_procedure_name_to_enroute_transitions()
            elif self.core.records and self.append_name == CORE:
                self.core.add_procedure_name_to_core()
            elif self.trailing.records and self.append_name == TRAILING:
                self.trailing.add_procedure_name_to_runway_transitions()

        return
