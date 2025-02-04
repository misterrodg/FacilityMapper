from modules.dir_paths import MANIFEST_DIR, NAVDATA_DIR, VIDMAP_DIR
from modules.file_handler import check_path, delete_all_in_subdir
from modules.manifest import Manifest
from modules.map_list import MapList

from cifparse import CIFP

import argparse
import os
import sqlite3

DB_FILE_PATH = f"{NAVDATA_DIR}/FAACIFP18.db"
CIFP_FILE_PATH = f"{NAVDATA_DIR}/FAACIFP18"
DEFAULT_MANIFEST_NAME = "manifest.json"


def purge_vidmaps() -> None:
    if check_path(VIDMAP_DIR):
        delete_all_in_subdir(".geojson", VIDMAP_DIR)


def purge_maplist() -> None:
    if check_path(VIDMAP_DIR):
        delete_all_in_subdir(".txt", VIDMAP_DIR)


def refresh_database() -> None:
    if os.path.exists(DB_FILE_PATH):
        os.remove(DB_FILE_PATH)
    connection = sqlite3.connect(DB_FILE_PATH)
    cursor = connection.cursor()

    c = CIFP(CIFP_FILE_PATH)
    c.initialize_database(cursor)
    c.parse()
    c.to_db(cursor)

    connection.commit()
    connection.close()


def main():
    parser = argparse.ArgumentParser(description="FacilityMapper")
    parser.add_argument(
        "-p", "--purge", action="store_true", help="purge files from vidmaps dir"
    )
    parser.add_argument("-r", "--refresh", action="store_true", help="refresh database")
    parser.add_argument(
        "-m", "--manifest", type=str, help="user-defined manifest file name"
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="create STARS map list"
    )
    parser.add_argument("-n", "--nodraw", action="store_true", help="skip draw")
    args = parser.parse_args()
    should_purge = args.purge
    should_refresh = args.refresh
    should_skip_draw = args.nodraw
    should_create_map_list = args.list
    alternate_manifest_file = args.manifest
    if should_purge:
        purge_vidmaps()
        purge_maplist()
    if should_refresh:
        refresh_database()

    if not should_skip_draw:
        connection = sqlite3.connect(DB_FILE_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        manifest_file = DEFAULT_MANIFEST_NAME
        if alternate_manifest_file != None:
            manifest_file = f"{MANIFEST_DIR}/{alternate_manifest_file}"

        map_list = None
        if should_create_map_list:
            map_list = MapList()

        Manifest(cursor, manifest_file, map_list)

        if map_list is not None:
            map_list.write()
        connection.close()


if __name__ == "__main__":
    main()
