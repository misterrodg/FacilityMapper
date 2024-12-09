from sqlite3 import Cursor


def query_db(db_cursor: Cursor, query_string: str) -> list[dict]:
    db_cursor.execute(query_string)
    return [dict(row) for row in db_cursor.fetchall()]
