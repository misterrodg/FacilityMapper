from modules.Manifest import Manifest

from cifparse import CIFP

import os
import sqlite3

DB_FILE_PATH = "./navdata/FAACIFP18.db"
CIFP_FILE_PATH = "./navdata/FAACIFP18"


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
    refreshArgument = False
    if refreshArgument:
        refreshDatabase()

    connection = sqlite3.connect(DB_FILE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    Manifest(cursor, "manifest.json")

    connection.close()


if __name__ == "__main__":
    main()
