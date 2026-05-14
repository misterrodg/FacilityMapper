from modules.db import JoinedProcedureRecords
from modules.dir_paths import NAVDATA_DIR
from modules.draw.draw_helper import inverse_bearing
from modules.geo_json import (
    Coordinate,
    Feature,
    GeoJSON,
    FeatureCollection,
    LineString,
    Properties,
)
from modules.path_term_handler import (
    handle_ca,
    handle_cd,
    handle_cf,
    handle_ci,
    handle_df,
    handle_fa,
    handle_fm,
    handle_hm,
    handle_if,
    handle_tf,
    handle_va,
    handle_vd,
    handle_vi,
    handle_vm,
    SymbolPoint,
)
from modules.query_handler import query_db, query_db_one
from modules.runway.runway_helper import check_for_combined, inverse_runway
from modules.stars_draw.symbol_draw import SymbolDraw

# CI
# AF

import sqlite3
import os

# fac_id = "KSBA"
# procedure_id = "FLOUT5"
# sub_code = "D"
# transition_ids = [
#     "RW15B",
# ]

# fac_id = "KHLN"
# procedure_id = "HLN5"
# sub_code = "D"
# transition_ids = ["RW05", "RW09", "RW27"]

fac_id = "KBWI"
procedure_id = "TERPZ8"
sub_code = "D"
transition_ids = [
    "RW10",
    "RW15L",
    "RW15R",
    "RW28",
    "RW33B",
]

# fac_id = "KDCA"
# procedure_id = "AMEEE1"
# sub_code = "D"
# transition_ids = ["RW01", "RW19", "RW33", "RW04", "RW15"]

# fac_id = "KIAD"
# procedure_id = "BUNZZ3"
# sub_code = "D"
# transition_ids = ["RW01B", "RW19B", "RW30"]

# fac_id = "KLGA"
# procedure_id = "JUTES4"
# sub_code = "D"
# transition_ids = ["RW22"]

# fac_id = "KLAX"
# procedure_id = "DOTSS2"
# sub_code = "D"
# transition_ids = ["RW24L", "RW24R", "RW25L", "RW25R"]

fac_id = "KJYO"
procedure_id = "PTOMC2"
sub_code = "D"
transition_ids = ["RW17", "RW35"]

fac_id = "KDEN"
procedure_id = "CHUWY1"
sub_code = "D"
transition_ids = ["RW08", "RW16B", "RW17B", "RW25", "RW34L", "RW34R", "RW35L", "RW35R"]

fac_id = "KYKM"
procedure_id = "GROMO4"
sub_code = "D"
transition_ids = ["RW09", "RW22", "RW27"]

fac_id = "KSFO"
procedure_id = "NIITE4"
sub_code = "D"
transition_ids = ["RW01B", "RW28B"]

fac_id = "KGPI"
procedure_id = "RIDDG2"
sub_code = "D"
transition_ids = ["RW02", "RW20"]

fac_id = "KEGE"
procedure_id = "EKR4"
sub_code = "D"
transition_ids = ["RW25"]


def _seed_initial_course_from_runway(
    runway_id: str,
    runway_bearing: object,
) -> float | None:
    if isinstance(runway_bearing, (int, float)):
        return inverse_bearing(float(runway_bearing))

    runway_component = runway_id[2:4]
    if runway_component.isdigit():
        # Fallback to runway designator heading (e.g. RW19 -> 190 deg)
        return inverse_bearing(float(int(runway_component) * 10))

    print(f"Skipping runway course seed for {runway_id}: missing runway bearing")
    return None


seen_fixes: list[str] = []
fix_symbols: list[dict] = []
path_symbols: list[SymbolPoint] = []

feature_collection = FeatureCollection()

DB_FILE_PATH = f"{NAVDATA_DIR}/FAACIFP18.db"
if os.path.exists(DB_FILE_PATH):
    connection = sqlite3.connect(DB_FILE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    for transition_id in transition_ids:

        procedure_query_string = f"""
            SELECT p.*,a.mag_var AS airport_mag_var,up.lat AS fix_lat,up.lon AS fix_lon,up.source AS fix_source,up.type AS fix_type,up.mag_var AS fix_mag_var,un.lat AS rec_vhf_lat,un.lon AS rec_vhf_lon,un.dme_lat AS rec_vhf_dme_lat,un.dme_lon AS rec_vhf_dme_lon,un.mag_var AS rec_vhf_mag_var,t.lat AS center_lat,t.lon AS center_lon
            FROM procedure_points AS p
            JOIN airports AS a on p.fac_id = a.airport_id
            LEFT JOIN unified_points AS up ON p.fix_id = up.id AND (up.env_id = '{fac_id}' OR up.env_id IS NULL)
            LEFT JOIN unified_navaids AS un ON p.rec_vhf = un.id AND (p.rec_vhf_sub_code = un.sub_code OR un.sub_code IS NULL) AND p.rec_vhf_region = un.region
            LEFT JOIN terminal_waypoints AS t ON p.center_fix = t.waypoint_id AND t.environment_id = '{fac_id}'
            WHERE fac_id = '{fac_id}' AND fac_sub_code = '{sub_code}' AND procedure_id = '{procedure_id}' AND transition_id = '{transition_id}'
            ORDER BY p.procedure_id,p.procedure_type,p.transition_id DESC,p.seq_no;
        """

        procedure_list = query_db(cursor, procedure_query_string)

        records = JoinedProcedureRecords(procedure_list)

        runway_ids = check_for_combined(transition_id)

        for id in runway_ids:
            id = inverse_runway(id)
            runway_query_string = f"""
                SELECT lat,lon,threshold_elevation,bearing
                FROM runways
                WHERE airport_id = '{fac_id}' AND runway_id = '{id}';
            """

            runway = query_db_one(cursor, runway_query_string)
            if runway is None:
                continue
            runway_lat = runway.get("lat")
            runway_lon = runway.get("lon")
            if runway_lat is None or runway_lon is None:
                continue

            der_point = Coordinate(runway_lat, runway_lon)
            der_point_elev = runway.get("threshold_elevation")
            der_point_bearing = runway.get("bearing")

            line_string = LineString()
            line_string.add_coordinate(der_point)
            last_course = _seed_initial_course_from_runway(id, der_point_bearing)
            last_coordinate = line_string.coordinates[-1]
            last_altitude = None

            for record in records.get_records():
                if record.fix_id and record.fix_id not in seen_fixes:
                    fix_symbols.append(
                        {
                            "name": record.fix_id,
                            "type": record.fix_type_to_symbol_name(),
                            "coordinate": Coordinate(record.fix_lat, record.fix_lon),
                        }
                    )
                    seen_fixes.append(record.fix_id)
                if record.path_term == "CA":
                    path_data = handle_ca(record, der_point, der_point_elev)
                    coordinate = path_data.get_last_coordinate()
                    line_string.add_coordinate(coordinate)
                    last_course = path_data.last_bearing
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "CD":
                    path_data = handle_cd(record, last_coordinate)
                    coordinate = path_data.get_last_coordinate()
                    line_string.add_coordinate(coordinate)
                    last_course = record.course
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "CF":
                    path_data = handle_cf(record, last_coordinate, last_course)
                    coordinates = path_data.coordinates
                    line_string.add_coordinates(coordinates)
                    last_course = path_data.last_bearing
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "CI":
                    path_data = handle_ci(record, last_course, last_coordinate)
                    coordinates = path_data.coordinates
                    line_string.add_coordinates(coordinates)
                    last_course = path_data.last_bearing
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "DF":
                    path_data = handle_df(record, last_course, last_coordinate)
                    line_string.add_coordinates(path_data.coordinates)
                    last_course = path_data.last_bearing
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "FA":
                    path_data = handle_fa(
                        record, last_coordinate, last_course, last_altitude
                    )
                    coordinates = path_data.coordinates
                    line_string.add_coordinates(coordinates)
                    last_course = path_data.last_bearing
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "FM":
                    path_data = handle_fm(record, 2.5)
                    last_course = path_data.last_bearing
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "HM":
                    path_data = handle_hm(record)
                    coordinates = path_data.coordinates
                    line_string.add_coordinates(coordinates)
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "IF":
                    path_data = handle_if(record)
                    coordinate = path_data.get_last_coordinate()
                    line_string.add_coordinate(coordinate)
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "TF":
                    path_data = handle_tf(record)
                    coordinate = path_data.get_last_coordinate()
                    line_string.add_coordinate(coordinate)
                    last_course = record.course
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "VA":
                    path_data = handle_va(record, der_point, der_point_elev)
                    coordinate = path_data.get_last_coordinate()
                    line_string.add_coordinate(coordinate)
                    last_course = path_data.last_bearing
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "VD":
                    path_data = handle_vd(record, last_coordinate)
                    coordinate = path_data.get_last_coordinate()
                    line_string.add_coordinate(coordinate)
                    last_course = record.course
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "VI":
                    path_data = handle_vi(record, last_course, last_coordinate)
                    coordinates = path_data.coordinates
                    line_string.add_coordinates(coordinates)
                    last_course = path_data.last_bearing
                    path_symbols.extend(path_data.symbol_points)
                if record.path_term == "VM":
                    path_data = handle_vm(record, last_coordinate, 2.5)
                    coordinates = path_data.coordinates
                    line_string.add_coordinates(coordinates)
                    last_course = path_data.last_bearing
                    path_symbols.extend(path_data.symbol_points)

                last_coordinate = line_string.coordinates[-1]
                if record.alt_1 is not None:
                    last_altitude = record.alt_1

            feature = Feature()
            feature.add_line_string(line_string)
            if len(line_string.coordinates) >= 2:
                feature_collection.add_feature(feature)

SYMBOL_SCALE = 0.5
ROTATION = 0

for symbol in fix_symbols:
    coordinate = symbol.get("coordinate")
    if coordinate is None or coordinate.lat is None or coordinate.lon is None:
        continue
    symbol_draw = SymbolDraw(
        "RNAV", coordinate.lat, coordinate.lon, ROTATION, SYMBOL_SCALE
    )
    feature = symbol_draw.get_feature()
    props = Properties()
    props.properties["type"] = "RNAV"
    feature.add_properties(props)
    feature_collection.add_feature(feature)

for symbol in path_symbols:
    coordinate = symbol.coordinate
    type = symbol.type
    rotation = symbol.rotation
    if type == "RNAV":
        continue
    symbol_draw = SymbolDraw(
        type, coordinate.lat, coordinate.lon, rotation, SYMBOL_SCALE
    )
    feature = symbol_draw.get_feature()
    props = Properties()
    props.properties["type"] = type
    feature.add_properties(props)
    feature_collection.add_feature(feature)

geo_json = GeoJSON("example")
geo_json.add_feature_collection(feature_collection)

geo_json.to_file()
