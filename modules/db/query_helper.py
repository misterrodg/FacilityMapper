from collections.abc import Sequence


def str_to_sql_string(string: str) -> str:
    result = f"'{string}'"
    return result


def list_to_sql_string(items: Sequence[object]) -> str:
    result = ",".join(f"'{str(x)}'" for x in items)
    result = f"({result})"
    return result


def translate_condition(field: str, value: str) -> str:
    result = f"{field} = '{value}'"
    if "#" in value:
        wildcard_value = translate_wildcard(value)
        result = f"{field} LIKE '{wildcard_value}'"
    return result


def translate_wildcard(wildcard_string: str) -> str:
    return wildcard_string.replace("#", "_")


def segment_query(
    query_result: list[dict[str, object]], dict_id: str
) -> list[list[dict[str, object]]]:
    last_id: object = ""
    segment: list[dict[str, object]] = []
    result: list[list[dict[str, object]]] = []
    for record in query_result:
        record_dict = dict(record)
        current_id = record_dict.get(dict_id)
        if current_id != last_id and last_id != "":
            result.append(segment)
            segment = []
        segment.append(record_dict)
        last_id = current_id
    if len(segment) > 0:
        result.append(segment)
    return result


def filter_query(
    query_result: list[dict[str, object]], dict_id: str
) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    seen_ids: set[object] = set()
    for record in query_result:
        if record[dict_id] not in seen_ids:
            result.append(record)
            seen_ids.add(record[dict_id])
    return result
