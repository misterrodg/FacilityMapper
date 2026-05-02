from sqlite3 import Cursor


def create_table_and_indexes(db_cursor: Cursor, query_list: list[str]) -> None:
    for query_string in query_list:
        db_cursor.execute(query_string)
    return


def query_db(db_cursor: Cursor, query_string: str) -> list[dict[str, object]]:
    db_cursor.execute(query_string)
    return [dict(row) for row in db_cursor.fetchall()]


def query_db_one(db_cursor: Cursor, query_string: str) -> dict[str, object]:
    db_cursor.execute(query_string)
    row = db_cursor.fetchone()
    if row is None:
        return {}
    return dict(row)
