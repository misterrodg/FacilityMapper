from modules.DirPaths import NAVDATA_DIR, VIDMAP_DIR
from modules.FileHandler import check_path, delete_all_in_subdir
from modules.Manifest import Manifest

from cifparse import CIFP

import argparse
import os
import sqlite3

DB_FILE_PATH = f"{NAVDATA_DIR}/FAACIFP18.db"
CIFP_FILE_PATH = f"{NAVDATA_DIR}/FAACIFP18"


def purge_vidmaps() -> None:
    if check_path(VIDMAP_DIR):
        delete_all_in_subdir(".geojson", VIDMAP_DIR)


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
    parser.add_argument("-n", "--nodraw", action="store_true", help="skip draw")
    args = parser.parse_args()
    should_purge = args.purge
    should_refresh = args.refresh
    should_skip_draw = args.nodraw
    if should_purge:
        purge_vidmaps()
    if should_refresh:
        refresh_database()

    if not should_skip_draw:
        connection = sqlite3.connect(DB_FILE_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        Manifest(cursor, "manifest.json")

        connection.close()


if __name__ == "__main__":
    main()
