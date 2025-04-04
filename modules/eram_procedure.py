from modules.db.joined_procedure_records import (
    JoinedProcedureRecords,
    select_joined_procedure_points,
)
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
from modules.error_helper import print_top_level
from modules.procedure import (
    DE_LEADING_ROUTE_TYPES,
    DE_CORE_ROUTE_TYPES,
    DE_TRAILING_ROUTE_TYPES,
    F_LEADING_ROUTE_TYPES,
    get_line_feature,
    get_symbol_features,
    get_text_features,
    translate_map_type,
)
from modules.query_handler import query_db

from sqlite3 import Cursor

ERROR_HEADER = "ERAM Procedure: "

PROCEDURE_TYPES = ["SID", "STAR", "IAP"]


class ERAMProcedure:
    def __init__(self, db_cursor: Cursor, definition_dict: dict):
        self.airport_id: str = None
        self.sub_code: str = None
        self.procedure_type: str = None
        self.procedure_id: str = None
        self.draw_names: bool = False
        self.draw_altitudes: bool = False
        self.draw_speeds: bool = False
        self.draw_symbols: bool = False
        self.draw_lines: bool = True
        self.suppress_core: bool = False
        self.line_defaults: LineProperties = None
        self.symbol_defaults: SymbolProperties = None
        self.text_defaults: TextProperties = None
        self.leading_transitions: list[str] = []  # Enroute or IAF Transitions
        self.trailing_transitions: list[str] = []  # Runway Transitions
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

        draw_names = definition_dict.get("draw_names", False)
        draw_altitudes = definition_dict.get("draw_altitudes", False)
        draw_speeds = definition_dict.get("draw_speeds", False)
        draw_symbols = definition_dict.get("draw_symbols", False)
        draw_lines = definition_dict.get("draw_lines", True)
        leading_transitions = definition_dict.get("leading_transitions", [])
        suppress_core = definition_dict.get("suppress_core", False)
        trailing_transitions = definition_dict.get("trailing_transitions", [])
        file_name = definition_dict.get("file_name")
        if file_name is None:
            file_name = f"{airport_id}_{self.procedure_type}_{procedure_id}"

        line_defaults = definition_dict.get("line_defaults")
        if draw_lines and not line_defaults:
            print(f"{ERROR_HEADER}line draw specified without line_defaults.")
            return
        if line_defaults:
            line_defaults = LineProperties(line_defaults, True)

        symbol_defaults = definition_dict.get("symbol_defaults")
        if draw_symbols and not symbol_defaults:
            print(f"{ERROR_HEADER}draw_symbols specified without symbol_defaults.")
            return
        if symbol_defaults:
            symbol_defaults = SymbolProperties(symbol_defaults, True)

        text_defaults = definition_dict.get("text_defaults")
        if (draw_names or draw_altitudes or draw_speeds) and not text_defaults:
            print(f"{ERROR_HEADER}text draw specified without text_defaults.")
            return
        if text_defaults:
            text_defaults = TextProperties(text_defaults, True)

        self.airport_id = airport_id
        self.sub_code = translate_map_type(procedure_type)
        self.procedure_type = procedure_type
        self.procedure_id = procedure_id
        self.draw_symbols = draw_symbols
        self.draw_altitudes = draw_altitudes
        self.draw_speeds = draw_speeds
        self.draw_names = draw_names
        self.draw_lines = draw_lines
        self.line_defaults = line_defaults
        self.symbol_defaults = symbol_defaults
        self.text_defaults = text_defaults
        self.leading_transitions = leading_transitions
        self.suppress_core = suppress_core
        self.trailing_transitions = trailing_transitions
        self.file_name = file_name
        self.is_valid = True

        return

    def _process_iap(self) -> None:
        if not self.suppress_core:
            core_route_type = [self.procedure_id[:1]]
            self.core = self._retrieve_records(route_types_list=core_route_type)
            self.core.trim_missed(True)

        if self.leading_transitions:
            self.leading = self._retrieve_records(
                self.leading_transitions, F_LEADING_ROUTE_TYPES
            )

        return

    def _process_sid_star(self) -> None:
        if not self.suppress_core:
            self.core = self._retrieve_records(route_types_list=DE_CORE_ROUTE_TYPES)

        if self.leading_transitions:
            self.leading = self._retrieve_records(
                self.leading_transitions, DE_LEADING_ROUTE_TYPES
            )

        if self.trailing_transitions:
            self.trailing = self._retrieve_records(
                self.trailing_transitions, DE_TRAILING_ROUTE_TYPES
            )

        return

    def _process(self) -> None:
        if self.sub_code == "F":
            self._process_iap()
        else:
            self._process_sid_star()

        return

    def _to_file(self) -> None:
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
        self, transition_list: list[str] = [], route_types_list: list[str] = []
    ) -> JoinedProcedureRecords:
        query_string = select_joined_procedure_points(
            self.airport_id,
            self.sub_code,
            self.procedure_id,
            transitions=transition_list,
            route_types=route_types_list,
        )
        query_result = query_db(self.db_cursor, query_string)
        result = JoinedProcedureRecords(query_result)
        return result

    def _process_defaults(self, defaults: vNASProperties) -> Feature:
        result = Feature()
        default_point = Point()
        default_point.set_coordinate(Coordinate(0, 0))
        properties = Properties()
        properties.from_dict(defaults.to_dict())
        result.add_point(default_point)
        result.add_properties(properties)
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
            features = get_symbol_features(joined_procedure_records_list)
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
            )
            result.extend(features)

        return result
