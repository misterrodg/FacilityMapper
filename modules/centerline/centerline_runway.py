from modules.centerline import get_line_strings
from modules.draw_helper import (
    haversine_great_circle_bearing,
    haversine_great_circle_distance,
    inverse_bearing,
)
from modules.error_helper import print_top_level
from modules.geo_json import LineString
from modules.db import (
    LOC_GS_Record,
    JoinedProcedureRecords,
    RunwayRecord,
    select_joined_procedure_points,
    select_loc_gs_by_airport_id_and_loc_id,
    select_runway_by_airport_id_and_runway_id,
)
from modules.query_handler import query_db, query_db_one
from modules.runway.runway_helper import inverse_runway
from modules.symbol_draw import SymbolDraw

from sqlite3 import Cursor
import math
import re

ERROR_HEADER = "CENTERLINE RUNWAY: "
DEFAULT_CENTERLINE_LENGTH = 10
DEFAULT_CROSSBAR_SCALE = 0.5
IAP_SUB_CODE = "F"


class CenterlineRunway:
    def __init__(self, db_cursor: Cursor, airport_id: str, definition_dict: dict):
        self.airport_id = airport_id
        self.runway_id = None
        self.inverse_runway_id = None
        self.length = None
        self.crossbar_scale = None
        self.base_lat = None
        self.base_lon = None
        self.bearing = None
        self.selected_loc = None
        self.selected_transition = None
        self.selected_iap = None
        self.runway_record = None
        self.iap_records = None
        self.centerline_multi_line: list[LineString] = []
        self.crossbar_line_strings: list[LineString] = []
        self.db_cursor = db_cursor
        self.is_valid = False

        self._validate(definition_dict)
        self._process()

    def get_line_strings(self) -> list[LineString]:
        result = []
        if self.selected_iap is not None:
            self._draw_crossbars()
            self._draw_centerline()
        else:
            self._draw_centerline()
        result.extend(self.centerline_line_strings)
        result.extend(self.crossbar_line_strings)
        return result

    def _validate(self, definition_dict: dict) -> None:
        runway_id = definition_dict.get("runway_id")
        if runway_id is None:
            print(
                f"{ERROR_HEADER}Missing `runway_id` in:\n{print_top_level(definition_dict)}."
            )
            return

        length = definition_dict.get("length")
        if length is None:
            length = DEFAULT_CENTERLINE_LENGTH

        crossbar_scale = definition_dict.get("crossbar_scale")
        if crossbar_scale is None:
            crossbar_scale = DEFAULT_CROSSBAR_SCALE

        selected_iap = definition_dict.get("selected_iap")
        selected_transition = definition_dict.get("selected_transition")
        selected_loc = definition_dict.get("selected_loc")

        self.runway_id = runway_id
        self.length = length
        self.crossbar_scale = crossbar_scale
        self.selected_iap = selected_iap
        self.selected_transition = selected_transition
        self.selected_loc = selected_loc
        self.is_valid = self._format_runway()
        return

    def _process(self) -> None:
        runway_query = self._build_query_string(self.runway_id)
        query_result = query_db_one(self.db_cursor, runway_query)

        if query_result is None:
            print(
                f"{ERROR_HEADER}Selected Runway {self.runway_id} not available for {self.airport_id}."
            )
            self.is_valid = False
            return

        self.runway_record = RunwayRecord(query_result)
        self.base_lat = self.runway_record.lat
        self.base_lon = self.runway_record.lon

        if self.selected_iap is not None:
            iap_query = self._build_iap_query_string()
            query_result = query_db(self.db_cursor, iap_query)
            procedure_records = JoinedProcedureRecords(query_result)
            self.iap_records = procedure_records.trim_missed()

            rec_vhf = None
            for record in self.iap_records:
                if record.rec_vhf:
                    rec_vhf = record.rec_vhf

            if rec_vhf:
                loc_query = self._build_loc_query_string(rec_vhf)
                loc_record = query_db_one(self.db_cursor, loc_query)
                localizer = LOC_GS_Record(loc_record)
                if localizer.plus_minus in ["+", "-"]:
                    self.base_lat = localizer.loc_lat
                    self.base_lon = localizer.loc_lon

    def _build_query_string(self, runway_id: str) -> str:
        airport_id = f"'{self.airport_id}'"
        runway_id = f"'{runway_id}'"
        result = select_runway_by_airport_id_and_runway_id(airport_id, runway_id)
        return result

    def _build_iap_query_string(self) -> str:
        airport_id = self.airport_id
        iap_id = f"'{self.selected_iap}'"
        iap_sub_code = IAP_SUB_CODE
        if self.selected_transition:
            result = select_joined_procedure_points(
                airport_id, iap_sub_code, iap_id, [self.selected_transition]
            )
        else:
            result = select_joined_procedure_points(airport_id, iap_sub_code, iap_id)
        return result

    def _build_loc_query_string(self, loc_id: str) -> str:
        airport_id = f"'{self.airport_id}'"
        loc_id = f"'{loc_id}'"
        result = select_loc_gs_by_airport_id_and_loc_id(airport_id, loc_id)
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

    def _draw_centerline(self) -> None:
        if self.selected_iap is None:
            runway = self.runway_record
            lat = runway.lat
            lon = runway.lon

            if self.selected_loc in [1, 2] and self.selected_iap is None:
                selected_loc = None
                if self.selected_loc == 1 and runway.ls_ident is not None:
                    selected_loc = runway.ls_ident
                if self.selected_loc == 2 and runway.ls_ident_2 is not None:
                    selected_loc = runway.ls_ident_2
                if selected_loc is not None:
                    loc_query = self._build_loc_query_string(selected_loc)
                    loc_record = query_db_one(self.db_cursor, loc_query)
                    localizer = LOC_GS_Record(loc_record)

                    bearing = inverse_bearing(localizer.loc_bearing + localizer.mag_var)
                    lat = localizer.loc_lat
                    lon = localizer.loc_lon

                else:
                    print(
                        f"{ERROR_HEADER}Selected LOC {self.selected_loc} not available for {self.airport_id} : {runway.runway_id}."
                    )
                    return

            else:
                inverse_runway_query = self._build_query_string(self.inverse_runway_id)
                inverse_record = query_db_one(self.db_cursor, inverse_runway_query)
                inverse_runway = RunwayRecord(inverse_record)

                bearing = haversine_great_circle_bearing(
                    inverse_runway.lat, inverse_runway.lon, lat, lon
                )
        else:
            if not self.iap_records:
                print(
                    f"{ERROR_HEADER}Selected IAP {self.selected_iap} not available for {self.airport_id}."
                )
                return
            lat = self.base_lat
            lon = self.base_lon
            bearing = self.bearing

        length = self._round_up_next_dash(self.length)
        self.centerline_line_strings = get_line_strings(lat, lon, bearing, length)
        return

    def _draw_crossbars(self) -> None:
        if self.iap_records:
            procedure_points = self.iap_records
            max_distance = 0
            first_point = procedure_points[0]
            last_point = procedure_points[-1]
            bearing = haversine_great_circle_bearing(
                last_point.lat, last_point.lon, first_point.lat, first_point.lon
            )
            for procedure_point in procedure_points:
                symbol = SymbolDraw(
                    "CROSSBAR",
                    procedure_point.lat,
                    procedure_point.lon,
                    bearing,
                    self.crossbar_scale,
                )
                self.crossbar_line_strings.extend(symbol.get_lines())
                point_distance = haversine_great_circle_distance(
                    self.base_lat,
                    self.base_lon,
                    procedure_point.lat,
                    procedure_point.lon,
                )
                if point_distance > max_distance:
                    max_distance = point_distance
            if max_distance > self.length:
                self.length = max_distance
            self.bearing = bearing
            return
