from modules.db.joined_procedure_records import (
    JoinedProcedureRecords,
    select_joined_procedure_points,
)
from modules.definitions.procedure import (
    Procedure as ProcedureDefinition,
    LEADING,
    CORE,
    TRAILING,
)
from modules.geo_json import Feature
from modules.procedure import (
    DE_LEADING_PROCEDURE_TYPES,
    DE_CORE_PROCEDURE_TYPES,
    DE_TRAILING_PROCEDURE_TYPES,
    F_LEADING_PROCEDURE_TYPES,
    LineOptions,
    ProcedurePoints,
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

    core: ProcedurePoints
    leading: ProcedurePoints
    trailing: ProcedurePoints

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
        self.core = ProcedurePoints([])
        self.leading = ProcedurePoints([])
        self.trailing = ProcedurePoints([])
        self.file_name = ""
        self.db_cursor = db_cursor
        self.base_valid = False

        self._base_validate(definition_dict)

    def _base_validate(self, definition_dict: dict[str, object]) -> None:
        normalized, errors = ProcedureDefinition.validate(definition_dict)
        if errors:
            for error in errors:
                print(f"{ERROR_HEADER}{error}")
            return
        if normalized is None:
            return

        self.airport_id = normalized["airport_id"]
        self.sub_code = translate_map_type(normalized["procedure_type"])
        self.procedure_type = normalized["procedure_type"]
        self.procedure_id = normalized["procedure_id"]
        self.draw_names = normalized["draw_names"]
        self.draw_altitudes = normalized["draw_altitudes"]
        self.draw_speeds = normalized["draw_speeds"]
        self.draw_symbols = normalized["draw_symbols"]
        self.append_name = normalized["append_name"]
        self.leading_transitions = normalized["leading_transitions"]
        self.suppress_core = normalized["suppress_core"]
        self.trailing_transitions = normalized["trailing_transitions"]
        self.file_name = (
            normalized["file_name"]
            or f"{normalized['airport_id']}_{normalized['procedure_type']}_{normalized['procedure_id']}"
        )
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
    ) -> ProcedurePoints:
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
        result = ProcedurePoints.from_joined_records(JoinedProcedureRecords(query_result))
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
