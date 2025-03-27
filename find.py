from modules.definitions import (
    Centerline,
    Centerlines,
    Composite,
    Controlled,
    IAP,
    Manifest,
    Map,
    MapType,
    Restrictive,
    Runways,
    SID,
    STAR,
    STARSDefinition,
)
from modules.dir_paths import NAVDATA_DIR
from modules.query_handler import query_db, query_db_one
from modules.runway import split_runway_id

import argparse
import os
import sqlite3

DB_FILE_PATH = f"{NAVDATA_DIR}/FAACIFP18.db"
GENERATED_PREFIX = "generated"

if os.path.exists(DB_FILE_PATH):
    connection = sqlite3.connect(DB_FILE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    parser = argparse.ArgumentParser(description="FacilityMapper Finder")
    parser.add_argument(
        "--runways",
        type=lambda s: s.split(","),
        help="generate a list of Runways (min_lat,min_lon,max_lat,max_lon)",
    )
    # Airport Options
    airport_group = parser.add_argument_group("Airport Options")
    airport_group.add_argument("--airport", type=str, help="find airport-related data")
    airport_group.add_argument(
        "--iap", action="store_true", help="generate a list of IAPs for --airport"
    )
    airport_group.add_argument(
        "--sid", action="store_true", help="generate a list of SIDs for --airport"
    )
    airport_group.add_argument(
        "--star", action="store_true", help="generate a list of STARs for --airport"
    )
    airport_group.add_argument(
        "--centerlines",
        action="store_true",
        help="generate a list of Centerlines for --airport",
    )
    airport_group.add_argument(
        "--select",
        action="store_true",
        help="select an IAP for each Centerline for --airport (if it exists)",
    )
    # Airspace Options
    airspace_group = parser.add_argument_group("Airspace Options")
    airspace_group.add_argument(
        "--controlled",
        type=lambda s: s.split(","),
        help="generate a list of Controlled Airspace (min_lat,min_lon,max_lat,max_lon)",
    )
    airspace_group.add_argument(
        "--restrictive",
        type=lambda s: s.split(","),
        help="generate a list of Restrictive Airspace (min_lat,min_lon,max_lat,max_lon)",
    )
    airspace_group.add_argument(
        "--composite",
        action="store_true",
        help="generate a composite from the individual maps",
    )

    args = parser.parse_args()
    airport_id = args.airport
    find_iap = args.iap
    find_sid = args.sid
    find_star = args.star
    find_centerlines = args.centerlines
    select_iap = args.select
    controlled = args.controlled
    restrictive = args.restrictive
    composite = args.composite
    runways = args.runways

    if airport_id:
        airport_id = airport_id.upper()
        manifest = Manifest()
        map_id = 1

        if find_sid:
            print(f"Finding SIDs for {airport_id}")
            query = f"SELECT DISTINCT procedure_id FROM procedure_points WHERE fac_id = '{airport_id}' AND fac_sub_code = 'D';"
            procedure_list = query_db(cursor, query)

            for procedure in procedure_list:
                map = Map(MapType.SID_TYPE)
                definition = SID(airport_id, procedure["procedure_id"])
                map_name = definition.file_name.replace("_", " ")
                stars_definition = STARSDefinition(map_name, map_id)
                map.add_definition(definition)
                map.add_stars_definition(stars_definition)
                manifest.add_map(map)
                map_id += 1

        if find_star:
            print(f"Finding STARs for {airport_id}")
            query = f"SELECT DISTINCT procedure_id FROM procedure_points WHERE fac_id = '{airport_id}' AND fac_sub_code = 'E';"
            procedure_list = query_db(cursor, query)

            for procedure in procedure_list:
                map = Map(MapType.STAR_TYPE)
                definition = STAR(airport_id, procedure["procedure_id"])
                map_name = definition.file_name.replace("_", " ")
                stars_definition = STARSDefinition(map_name, map_id)
                map.add_definition(definition)
                map.add_stars_definition(stars_definition)
                manifest.add_map(map)
                map_id += 1

        if find_iap:
            print(f"Finding IAPs for {airport_id}")
            query = f"SELECT DISTINCT procedure_id FROM procedure_points WHERE fac_id = '{airport_id}' AND fac_sub_code = 'F';"
            procedure_list = query_db(cursor, query)

            for procedure in procedure_list:
                map = Map(MapType.IAP_TYPE)
                definition = IAP(airport_id, procedure["procedure_id"])
                map_name = definition.file_name.replace("_", " ")
                stars_definition = STARSDefinition(map_name, map_id)
                map.add_definition(definition)
                map.add_stars_definition(stars_definition)
                manifest.add_map(map)
                map_id += 1

        if find_centerlines:
            query = f"SELECT runway_id, ls_ident FROM runways WHERE airport_id = '{airport_id}';"
            runway_list = query_db(cursor, query)

            map = Map(MapType.CENTERLINES)
            definition = Centerlines(airport_id)
            map_name = definition.file_name.replace("_", " ")
            stars_definition = STARSDefinition(map_name, map_id)

            for runway in runway_list:
                runway_id_dict = split_runway_id(runway["runway_id"])
                trimmed_runway = f"{runway_id_dict["bearing_component"]}{runway_id_dict["side_component"]}"
                centerline = Centerline(trimmed_runway)

                if select_iap and runway["ls_ident"]:
                    procedure_wildcard = "_" + trimmed_runway + "%"
                    rec_vhf = runway["ls_ident"]
                    query = f"""
                    SELECT DISTINCT procedure_id 
                    FROM procedure_points 
                    WHERE procedure_id LIKE '{procedure_wildcard}' AND fac_id = '{airport_id}' AND fac_sub_code = 'F' AND rec_vhf = '{rec_vhf}' 
                    ORDER BY 
                        CASE 
                            WHEN procedure_id LIKE 'I%' THEN 1
                            WHEN procedure_id LIKE 'L%' THEN 2
	                        WHEN procedure_id LIKE 'LOC%' THEN 3
                            WHEN procedure_id LIKE 'X%' THEN 4
	                        WHEN procedure_id LIKE 'LDA%' THEN 5
                            ELSE 6
                        END
                    LIMIT 1;
                    """
                    procedure = query_db_one(cursor, query)
                    centerline.selected_iap = procedure["procedure_id"]

                definition.add_centerline(centerline)

            map_id += 1
            map.add_definition(definition)
            map.add_stars_definition(stars_definition)
            manifest.add_map(map)

        manifest.to_file(f"{GENERATED_PREFIX}_{airport_id}")

    if controlled:
        manifest = Manifest()
        map_id = 1

        min_lat = controlled[0]
        max_lat = controlled[2]
        min_lon = controlled[1]
        max_lon = controlled[3]
        print(
            f"Finding Controlled Airspace in box defined by {min_lat},{min_lon} {max_lat},{max_lon}"
        )
        query = f"SELECT DISTINCT center_id, airspace_class FROM controlled_airspace_points WHERE (lat BETWEEN {min_lat} AND {max_lat} AND lon BETWEEN {min_lon} AND {max_lon}) OR (arc_lat BETWEEN {min_lat} AND {max_lat} AND arc_lon BETWEEN {min_lon} AND {max_lon});"
        controlled_list = query_db(cursor, query)

        file_names = []

        for cont in controlled_list:
            map = Map(MapType.CONTROLLED_TYPE)
            definition = Controlled(cont["center_id"], cont["airspace_class"])
            file_name = definition.file_name
            file_names.append(file_name)
            map_name = file_name.replace("_", " ")
            stars_definition = STARSDefinition(map_name, map_id)
            map.add_definition(definition)
            map.add_stars_definition(stars_definition)
            manifest.add_map(map)
            map_id += 1

        if composite:
            composite_map = Map(MapType.COMPOSITE_TYPE)
            definition = Composite(file_names, "ALL_CONTROLLED")
            map_name = definition.file_name.replace("_", " ")
            stars_definition = STARSDefinition(map_name, 0)
            composite_map.add_definition(definition)
            composite_map.add_stars_definition(stars_definition)
            manifest.add_map(composite_map)

        manifest.to_file(f"{GENERATED_PREFIX}_controlled")

    if restrictive:
        manifest = Manifest()
        map_id = 1

        min_lat = restrictive[0]
        max_lat = restrictive[2]
        min_lon = restrictive[1]
        max_lon = restrictive[3]
        print(
            f"Finding Restrictive Airspace in box defined by {min_lat},{min_lon} {max_lat},{max_lon}"
        )
        query = f"SELECT DISTINCT restrictive_designation, restrictive_type FROM restrictive_airspace_points WHERE (lat BETWEEN {min_lat} AND {max_lat} AND lon BETWEEN {min_lon} AND {max_lon}) OR (arc_lat BETWEEN {min_lat} AND {max_lat} AND arc_lon BETWEEN {min_lon} AND {max_lon});"
        restrictive_list = query_db(cursor, query)

        file_names = []

        for rest in restrictive_list:
            map = Map(MapType.RESTRICTIVE_TYPE)
            definition = Restrictive(
                rest["restrictive_designation"], rest["restrictive_type"]
            )
            file_name = definition.file_name
            file_names.append(file_name)
            map_name = file_name.replace("_", " ")
            stars_definition = STARSDefinition(map_name, map_id)
            map.add_definition(definition)
            map.add_stars_definition(stars_definition)
            manifest.add_map(map)
            map_id += 1

        if composite:
            composite_map = Map(MapType.COMPOSITE_TYPE)
            definition = Composite(file_names, "ALL_RESTRICTIVE")
            map_name = definition.file_name.replace("_", " ")
            stars_definition = STARSDefinition(map_name, 0)
            composite_map.add_definition(definition)
            composite_map.add_stars_definition(stars_definition)
            manifest.add_map(composite_map)

        manifest.to_file(f"{GENERATED_PREFIX}_restrictive")

    if runways:
        manifest = Manifest()

        min_lat = runways[0]
        max_lat = runways[2]
        min_lon = runways[1]
        max_lon = runways[3]
        print(
            f"Finding Runways in box defined by {min_lat},{min_lon} {max_lat},{max_lon}"
        )
        query = f"SELECT DISTINCT a.airport_id FROM airports AS a JOIN runways AS r ON a.airport_id = r.airport_id WHERE a.lat BETWEEN {min_lat} AND {max_lat} AND a.lon BETWEEN {min_lon} AND {max_lon};"
        runways_list = query_db(cursor, query)

        airport_list = []
        for rwy in runways_list:
            airport_list.append(rwy["airport_id"])

        map = Map(MapType.RUNWAYS_TYPE)
        definition = Runways(airport_list, "RUNWAYS")
        map_name = definition.file_name.replace("_", " ")
        stars_definition = STARSDefinition(map_name, 1)
        map.add_definition(definition)
        map.add_stars_definition(stars_definition)
        manifest.add_map(map)

        manifest.to_file(f"{GENERATED_PREFIX}_runways")


else:
    print(f"No database found at {DB_FILE_PATH}.")
    print(f"Ensure the FAACIFP18 file is in the {NAVDATA_DIR} directory and run:")
    print("python3 main.py --nodraw --refresh")
