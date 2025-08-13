from sqlite3 import Cursor


def create_table_and_indexes(db_cursor: Cursor, query_list: list) -> None:
    for query_string in query_list:
        db_cursor.execute(query_string)
    return


def query_db(db_cursor: Cursor, query_string: str) -> list[dict]:
    db_cursor.execute(query_string)
    return [dict(row) for row in db_cursor.fetchall()]


def query_db_one(db_cursor: Cursor, query_string: str) -> dict:
    db_cursor.execute(query_string)
    row = db_cursor.fetchone()
    return dict(row) if row else None
