from modules.centerline import get_line_strings
from modules.draw import (
    haversine_great_circle_bearing,
    haversine_great_circle_distance,
    inverse_bearing,
    lat_lon_from_pbd,
)
from modules.error_helper import print_top_level
from modules.geo_json import LineString
from modules.db import (
    LOC_GS_Record,
    JoinedProcedureRecord,
    JoinedProcedureRecords,
    RunwayRecord,
    select_joined_procedure_points,
    select_loc_gs_by_airport_id_and_loc_id,
    select_runway_by_airport_id_and_runway_id,
)
from modules.query_handler import query_db, query_db_one
from modules.runway.runway_helper import inverse_runway
from modules.stars_draw.symbol_draw import SymbolDraw
from modules.stars_draw.symbol_plots import CROSSBAR_SYMBOL

from sqlite3 import Cursor
import math
import re

ERROR_HEADER = "CENTERLINE RUNWAY: "
DEFAULT_CENTERLINE_LENGTH = 10
DEFAULT_CROSSBAR_SCALE = 0.5
IAP_SUB_CODE = "F"


class CenterlineRunway:
    airport_id: str
    runway_id: str
    inverse_runway_id: str
    length: float
    crossbar_scale: float
    base_lat: float | None
    base_lon: float | None
    bearing: float | None
    selected_loc: int | None
    selected_transition: str | None
    selected_iap: str | None
    selected_distances: list[float] | None
    runway_record: RunwayRecord | None
    iap_records: list[JoinedProcedureRecord]
    centerline_line_strings: list[LineString]
    crossbar_line_strings: list[LineString]
    db_cursor: Cursor
    is_valid: bool

    def __init__(
        self, db_cursor: Cursor, airport_id: str, definition_dict: dict[str, object]
    ):
        self.airport_id = airport_id
        self.runway_id = ""
        self.inverse_runway_id = ""
        self.length = float(DEFAULT_CENTERLINE_LENGTH)
        self.crossbar_scale = float(DEFAULT_CROSSBAR_SCALE)
        self.base_lat = None
        self.base_lon = None
        self.bearing = None
        self.selected_loc = None
        self.selected_transition = None
        self.selected_iap = None
        self.selected_distances = None
        self.runway_record = None
        self.iap_records = []
        self.centerline_line_strings = []
        self.crossbar_line_strings = []
        self.db_cursor = db_cursor
        self.is_valid = False

        self._validate(definition_dict)
        if self.is_valid:
            self._process()

    def get_line_strings(self) -> list[LineString]:
        result = []
        if self.selected_iap is not None:
            self._draw_crossbars()
            self._draw_centerline()
        elif self.selected_distances is not None:
            self._draw_centerline()
            self._draw_crossbars()
        else:
            self._draw_centerline()
        result.extend(self.centerline_line_strings)
        result.extend(self.crossbar_line_strings)
        return result

    def _validate(self, definition_dict: dict[str, object]) -> None:
        runway_id = definition_dict.get("runway_id")
        if not isinstance(runway_id, str):
            print(
                f"{ERROR_HEADER}Missing or invalid `runway_id` in:\n{print_top_level(definition_dict)}."
            )
            return

        length = definition_dict.get("length")
        if length is None:
            length = float(DEFAULT_CENTERLINE_LENGTH)
        elif isinstance(length, (int, float)):
            length = float(length)
        else:
            print(
                f"{ERROR_HEADER}Invalid `length` in:\n{print_top_level(definition_dict)}."
            )
            return

        crossbar_scale = definition_dict.get("crossbar_scale")
        if crossbar_scale is None:
            crossbar_scale = float(DEFAULT_CROSSBAR_SCALE)
        elif isinstance(crossbar_scale, (int, float)):
            crossbar_scale = float(crossbar_scale)
        else:
            print(
                f"{ERROR_HEADER}Invalid `crossbar_scale` in:\n{print_top_level(definition_dict)}."
            )
            return

        selected_iap = definition_dict.get("selected_iap")
        if selected_iap is not None and not isinstance(selected_iap, str):
            print(
                f"{ERROR_HEADER}Invalid `selected_iap` in:\n{print_top_level(definition_dict)}."
            )
            return

        selected_transition = definition_dict.get("selected_transition")
        if selected_transition is not None and not isinstance(selected_transition, str):
            print(
                f"{ERROR_HEADER}Invalid `selected_transition` in:\n{print_top_level(definition_dict)}."
            )
            return

        selected_loc = definition_dict.get("selected_loc")
        if selected_loc is not None and (
            not isinstance(selected_loc, int) or isinstance(selected_loc, bool)
        ):
            print(
                f"{ERROR_HEADER}Invalid `selected_loc` in:\n{print_top_level(definition_dict)}."
            )
            return

        selected_distances = definition_dict.get("selected_distances")
        if selected_distances is not None:
            if not isinstance(selected_distances, list):
                print(
                    f"{ERROR_HEADER}Invalid `selected_distances` in:\n{print_top_level(definition_dict)}."
                )
                return
            distance_list: list[float] = []
            for item in selected_distances:
                if not isinstance(item, (int, float)):
                    print(
                        f"{ERROR_HEADER}Invalid distance in `selected_distances` in:\n{print_top_level(definition_dict)}."
                    )
                    return
                distance_list.append(float(item))
            selected_distances = distance_list

        self.runway_id = runway_id
        self.length = length
        self.crossbar_scale = crossbar_scale
        self.selected_iap = selected_iap
        self.selected_transition = selected_transition
        self.selected_loc = selected_loc
        self.selected_distances = selected_distances
        self.is_valid = self._format_runway()
        return

    def _process(self) -> None:
        runway_query = self._build_query_string(self.runway_id)
        query_result = query_db_one(self.db_cursor, runway_query)

        if not query_result:
            print(
                f"{ERROR_HEADER}Selected Runway {self.runway_id} not available for {self.airport_id}."
            )
            self.is_valid = False
            return

        self.runway_record = RunwayRecord(query_result)
        runway_lat = self.runway_record.lat
        runway_lon = self.runway_record.lon
        if runway_lat is None or runway_lon is None:
            print(
                f"{ERROR_HEADER}Selected Runway {self.runway_id} has invalid coordinates for {self.airport_id}."
            )
            self.is_valid = False
            return
        self.base_lat = runway_lat
        self.base_lon = runway_lon

        if self.selected_iap is not None:
            self._load_iap_records()

    def _build_query_string(self, runway_id: str) -> str:
        result = select_runway_by_airport_id_and_runway_id(self.airport_id, runway_id)
        return result

    def _build_iap_query_string(self) -> str | None:
        airport_id = self.airport_id
        iap_id = self.selected_iap
        if iap_id is None:
            return None
        iap_sub_code = IAP_SUB_CODE
        if self.selected_transition:
            result = select_joined_procedure_points(
                airport_id, iap_sub_code, iap_id, transitions=[self.selected_transition]
            )
        else:
            result = select_joined_procedure_points(airport_id, iap_sub_code, iap_id)
        return result

    def _build_loc_query_string(self, loc_id: str) -> str:
        result = select_loc_gs_by_airport_id_and_loc_id(self.airport_id, loc_id)
        return result

    def _format_runway(self) -> bool:
        match = re.fullmatch(r"(\d{1,2})([LCR]?)", self.runway_id)
        if match:
            num, char = match.groups()
            self.runway_id = f"RW{int(num):02}{char}"
            self.inverse_runway_id = inverse_runway(self.runway_id)
            return True
        print(f"{ERROR_HEADER}Unrecognized runway format: {self.runway_id}.")
        return False

    def _round_up_next_dash(self, length: float) -> float:
        return math.ceil(length / 2) * 2

    def _load_iap_records(self) -> None:
        iap_query = self._build_iap_query_string()
        if iap_query is None:
            return

        query_result = query_db(self.db_cursor, iap_query)
        procedure_records = JoinedProcedureRecords(query_result)
        procedure_records.trim_missed()
        self.iap_records = procedure_records.get_records()

        rec_vhf = None
        for record in self.iap_records:
            if record.rec_vhf:
                rec_vhf = record.rec_vhf

        if rec_vhf is None:
            return

        loc_query = self._build_loc_query_string(rec_vhf)
        loc_record = query_db_one(self.db_cursor, loc_query)
        if not loc_record:
            return

        localizer = LOC_GS_Record(loc_record)
        if (
            localizer.plus_minus in ["+", "-"]
            and localizer.loc_lat is not None
            and localizer.loc_lon is not None
        ):
            self.base_lat = localizer.loc_lat
            self.base_lon = localizer.loc_lon

    def _resolve_centerline_origin(self) -> tuple[float, float, float] | None:
        if self.selected_iap is not None:
            return self._resolve_iap_origin()
        return self._resolve_runway_origin()

    def _resolve_iap_origin(self) -> tuple[float, float, float] | None:
        if not self.iap_records:
            print(
                f"{ERROR_HEADER}Selected IAP {self.selected_iap} not available for {self.airport_id}."
            )
            return None

        if self.base_lat is None or self.base_lon is None or self.bearing is None:
            print(
                f"{ERROR_HEADER}Insufficient data to draw selected IAP {self.selected_iap} for {self.airport_id}."
            )
            return None

        return self.base_lat, self.base_lon, self.bearing

    def _resolve_runway_origin(self) -> tuple[float, float, float] | None:
        runway = self.runway_record
        if runway is None or runway.lat is None or runway.lon is None:
            print(f"{ERROR_HEADER}Invalid runway geometry for {self.airport_id}.")
            return None

        if self.selected_loc in [1, 2]:
            return self._resolve_localizer_origin(runway)
        return self._resolve_inverse_runway_origin(runway)

    def _resolve_localizer_origin(
        self, runway: RunwayRecord
    ) -> tuple[float, float, float] | None:
        selected_loc_id: str | None = None
        if self.selected_loc == 1 and runway.ls_ident_1 is not None:
            selected_loc_id = runway.ls_ident_1
        if self.selected_loc == 2 and runway.ls_ident_2 is not None:
            selected_loc_id = runway.ls_ident_2

        if selected_loc_id is None:
            print(
                f"{ERROR_HEADER}Selected LOC {self.selected_loc} not available for {self.airport_id} : {runway.runway_id}."
            )
            return None

        loc_query = self._build_loc_query_string(selected_loc_id)
        loc_record = query_db_one(self.db_cursor, loc_query)
        if not loc_record:
            print(
                f"{ERROR_HEADER}Selected LOC {selected_loc_id} not available for {self.airport_id}."
            )
            return None

        localizer = LOC_GS_Record(loc_record)
        if (
            localizer.loc_bearing is None
            or localizer.mag_var is None
            or localizer.loc_lat is None
            or localizer.loc_lon is None
        ):
            print(
                f"{ERROR_HEADER}Selected LOC {selected_loc_id} has invalid geometry for {self.airport_id}."
            )
            return None

        bearing = inverse_bearing(localizer.loc_bearing + localizer.mag_var)
        self.bearing = bearing
        return localizer.loc_lat, localizer.loc_lon, bearing

    def _resolve_inverse_runway_origin(
        self, runway: RunwayRecord
    ) -> tuple[float, float, float] | None:
        runway_lat = runway.lat
        runway_lon = runway.lon
        if runway_lat is None or runway_lon is None:
            print(f"{ERROR_HEADER}Invalid runway geometry for {self.airport_id}.")
            return None

        if self.inverse_runway_id == "":
            print(f"{ERROR_HEADER}Inverse runway not set for {self.runway_id}.")
            return None

        inverse_runway_query = self._build_query_string(self.inverse_runway_id)
        inverse_record = query_db_one(self.db_cursor, inverse_runway_query)
        if not inverse_record:
            print(
                f"{ERROR_HEADER}Inverse runway {self.inverse_runway_id} not available for {self.airport_id}."
            )
            return None

        inverse_runway = RunwayRecord(inverse_record)
        if inverse_runway.lat is None or inverse_runway.lon is None:
            print(
                f"{ERROR_HEADER}Inverse runway {self.inverse_runway_id} has invalid geometry for {self.airport_id}."
            )
            return None

        bearing = haversine_great_circle_bearing(
            inverse_runway.lat, inverse_runway.lon, runway_lat, runway_lon
        )
        self.bearing = bearing
        if self.selected_distances:
            max_selected_distance = max(self.selected_distances)
            if max_selected_distance > self.length:
                self.length = max_selected_distance
        return runway_lat, runway_lon, bearing

    def _draw_centerline(self) -> None:
        resolved_origin = self._resolve_centerline_origin()
        if resolved_origin is None:
            return

        lat, lon, bearing = resolved_origin
        length = self._round_up_next_dash(self.length)
        self.centerline_line_strings = get_line_strings(lat, lon, bearing, length)
        return

    def _draw_crossbars(self) -> None:
        if self.iap_records:
            self._draw_iap_crossbars()

        if self.selected_distances:
            self._draw_selected_distance_crossbars()

        return

    def _draw_iap_crossbars(self) -> None:
        procedure_points = self.iap_records
        first_point = procedure_points[0]
        last_point = procedure_points[-1]
        if (
            first_point.fix_lat is None
            or first_point.fix_lon is None
            or last_point.fix_lat is None
            or last_point.fix_lon is None
        ):
            return

        bearing = haversine_great_circle_bearing(
            last_point.fix_lat,
            last_point.fix_lon,
            first_point.fix_lat,
            first_point.fix_lon,
        )

        if self.base_lat is None or self.base_lon is None:
            return

        max_distance = 0.0
        for procedure_point in procedure_points:
            if procedure_point.fix_lat is None or procedure_point.fix_lon is None:
                continue

            symbol = SymbolDraw(
                CROSSBAR_SYMBOL,
                procedure_point.fix_lat,
                procedure_point.fix_lon,
                bearing,
                self.crossbar_scale,
            )
            self.crossbar_line_strings.extend(symbol.get_lines())

            point_distance = haversine_great_circle_distance(
                self.base_lat,
                self.base_lon,
                procedure_point.fix_lat,
                procedure_point.fix_lon,
            )
            if point_distance > max_distance:
                max_distance = point_distance

        if max_distance > self.length:
            self.length = max_distance
        self.bearing = bearing

    def _draw_selected_distance_crossbars(self) -> None:
        if (
            self.selected_distances is None
            or self.base_lat is None
            or self.base_lon is None
            or self.bearing is None
        ):
            return

        for selected_distance in self.selected_distances:
            point = lat_lon_from_pbd(
                self.base_lat, self.base_lon, self.bearing, selected_distance
            )
            symbol = SymbolDraw(
                CROSSBAR_SYMBOL,
                point["lat"],
                point["lon"],
                self.bearing,
                self.crossbar_scale,
            )
            self.crossbar_line_strings.extend(symbol.get_lines())
