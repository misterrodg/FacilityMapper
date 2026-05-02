from modules.db.joined_procedure_records import (
    JoinedProcedureRecords,
    select_joined_procedure_points,
)
from modules.error_helper import print_top_level
from modules.geo_json import Feature
from modules.procedure import (
    DE_LEADING_PROCEDURE_TYPES,
    DE_CORE_PROCEDURE_TYPES,
    DE_TRAILING_PROCEDURE_TYPES,
    F_LEADING_PROCEDURE_TYPES,
    LineOptions,
    SymbolOptions,
    TextOptions,
    get_line_feature,
    get_symbol_features,
    get_text_features,
    translate_map_type,
)
from modules.query_handler import query_db

from sqlite3 import Cursor

ERROR_HEADER = "Procedure: "

PROCEDURE_TYPES = ["SID", "STAR", "IAP"]
LEADING = "leading"
CORE = "core"
TRAILING = "trailing"
PROCEDURE_SEGMENTS = [LEADING, CORE, TRAILING]


class ProcedureBase:
    airport_id: str
    sub_code: str
    procedure_type: str
    procedure_id: str
    draw_names: bool
    draw_altitudes: bool
    draw_speeds: bool
    draw_symbols: bool
    append_name: str
    leading_transitions: list[str]
    suppress_core: bool
    trailing_transitions: list[str]

    core: JoinedProcedureRecords
    leading: JoinedProcedureRecords
    trailing: JoinedProcedureRecords

    file_name: str
    db_cursor: Cursor
    base_valid: bool

    def __init__(self, db_cursor: Cursor, definition_dict: dict[str, object]):
        self.airport_id = ""
        self.sub_code = ""
        self.procedure_type = ""
        self.procedure_id = ""
        self.draw_names = False
        self.draw_altitudes = False
        self.draw_speeds = False
        self.draw_symbols = False
        self.append_name = ""
        self.leading_transitions = []
        self.suppress_core = False
        self.trailing_transitions = []
        self.core = JoinedProcedureRecords([])
        self.leading = JoinedProcedureRecords([])
        self.trailing = JoinedProcedureRecords([])
        self.file_name = ""
        self.db_cursor = db_cursor
        self.base_valid = False

        self._base_validate(definition_dict)

    def _base_validate(self, definition_dict: dict[str, object]) -> None:
        airport_id = definition_dict.get("airport_id")
        if not isinstance(airport_id, str):
            print(
                f"{ERROR_HEADER}Invalid `airport_id` in:\n{print_top_level(definition_dict)}."
            )
            return

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

        procedure_id = definition_dict.get("procedure_id")
        if not isinstance(procedure_id, str):
            print(
                f"{ERROR_HEADER}Invalid `procedure_id` in:\n{print_top_level(definition_dict)}."
            )
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

        leading_transitions = definition_dict.get("leading_transitions", [])
        if not isinstance(leading_transitions, list):
            leading_transitions = []
        if not all(isinstance(item, str) for item in leading_transitions):
            print(
                f"{ERROR_HEADER}Invalid `leading_transitions` in:\n{print_top_level(definition_dict)}."
            )
            return

        suppress_core = definition_dict.get("suppress_core", False)
        if not isinstance(suppress_core, bool):
            suppress_core = False

        trailing_transitions = definition_dict.get("trailing_transitions", [])
        if not isinstance(trailing_transitions, list):
            trailing_transitions = []
        if not all(isinstance(item, str) for item in trailing_transitions):
            print(
                f"{ERROR_HEADER}Invalid `trailing_transitions` in:\n{print_top_level(definition_dict)}."
            )
            return

        file_name = definition_dict.get("file_name")
        if not isinstance(file_name, str):
            file_name = f"{airport_id}_{procedure_type}_{procedure_id}"

        self.airport_id = airport_id
        self.sub_code = translate_map_type(procedure_type)
        self.procedure_type = procedure_type
        self.procedure_id = procedure_id
        self.draw_names = draw_names
        self.draw_altitudes = draw_altitudes
        self.draw_speeds = draw_speeds
        self.draw_symbols = draw_symbols
        self.append_name = append_name
        self.leading_transitions = leading_transitions
        self.suppress_core = suppress_core
        self.trailing_transitions = trailing_transitions

        self.file_name = file_name
        self.base_valid = True
        return

    def _process_iap(self) -> None:
        if not self.suppress_core:
            core_procedure_types = ["NOT"]
            core_procedure_types.extend(F_LEADING_PROCEDURE_TYPES)
            self.core = self._retrieve_records(
                procedure_types_list=core_procedure_types
            )
            self.core.trim_missed(True)

        if self.leading_transitions:
            self.leading = self._retrieve_records(
                self.leading_transitions, F_LEADING_PROCEDURE_TYPES
            )

        return

    def _process_sid_star(self) -> None:
        if not self.suppress_core:
            self.core = self._retrieve_records(
                procedure_types_list=DE_CORE_PROCEDURE_TYPES
            )

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

    def _retrieve_records(
        self,
        transition_list: list[str] | None = None,
        procedure_types_list: list[str] | None = None,
    ) -> JoinedProcedureRecords:
        if transition_list is None:
            transition_list = []
        if procedure_types_list is None:
            procedure_types_list = []

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

    def _draw_lines(self, line_options: LineOptions | None = None) -> Feature:
        if line_options is None:
            line_options = LineOptions()

        if not self.draw_symbols:
            line_options.buffer_length = 0.0

        result = Feature()
        joined_procedure_records_tuples_list = []
        if self.core:
            joined_procedure_records_tuples_list.append((self.core, False))

        if self.leading:
            joined_procedure_records_tuples_list.append((self.leading, True))

        if self.trailing:
            joined_procedure_records_tuples_list.append((self.trailing, True))

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
        joined_procedure_records_list = []
        if self.core:
            joined_procedure_records_list.append(self.core)

        if self.leading:
            joined_procedure_records_list.append(self.leading)

        if self.trailing:
            joined_procedure_records_list.append(self.trailing)

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
        joined_procedure_records_list = []
        if self.core:
            joined_procedure_records_list.append(self.core)

        if self.leading:
            joined_procedure_records_list.append(self.leading)

        if self.trailing:
            joined_procedure_records_list.append(self.trailing)

        if joined_procedure_records_list:
            features = get_text_features(joined_procedure_records_list, text_options)
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
