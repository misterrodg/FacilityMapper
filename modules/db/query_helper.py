def str_to_sql_string(string: str) -> str:
    result = f"'{string}'"
    return result


def list_to_sql_string(list: list) -> str:
    result = ",".join(f"'{str(x)}'" for x in list)
    result = f"({result})"
    return result


def translate_condition(field: str, value: str) -> str:
    result = f"{field} = {value}"
    if "#" in value:
        wildcard_value = translate_wildcard(value)
        result = f"{field} LIKE '{wildcard_value}'"
    return result


def translate_wildcard(wildcard_string: str) -> str:
    return wildcard_string.replace("#", "_")


def segment_query(query_result: list, dict_id: str) -> list[list[dict]]:
    last_id = ""
    segment = []
    result = []
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


def filter_query(query_result: list, dict_id: str) -> list[dict]:
    result = []
    seen_ids = set()
    for record in query_result:
        if record[dict_id] not in seen_ids:
            result.append(record)
            seen_ids.add(record[dict_id])
    return result
