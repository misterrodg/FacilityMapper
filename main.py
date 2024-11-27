from modules.DirPaths import NAVDATA_DIR, VIDMAP_DIR
from modules.FileHandler import checkPath, deleteAllInSubdir
from modules.Manifest import Manifest

from cifparse import CIFP

import argparse
import os
import sqlite3

DB_FILE_PATH = f"{NAVDATA_DIR}/FAACIFP18.db"
CIFP_FILE_PATH = f"{NAVDATA_DIR}/FAACIFP18"


def purgeVidmaps() -> None:
    if checkPath(VIDMAP_DIR):
        deleteAllInSubdir(".geojson", VIDMAP_DIR)


def refreshDatabase() -> None:
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
    shouldPurge = args.purge
    shouldRefresh = args.refresh
    shouldSkipDraw = args.nodraw
    if shouldPurge:
        purgeVidmaps()
    if shouldRefresh:
        refreshDatabase()

    if not shouldSkipDraw:
        connection = sqlite3.connect(DB_FILE_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        Manifest(cursor, "manifest.json")

        connection.close()


if __name__ == "__main__":
    main()
