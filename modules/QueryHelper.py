def translate_wildcard(wildcard_string: str) -> str:
    return wildcard_string.replace("#", "%")


def segment_query(query_result: list, dict_id: str) -> list[dict]:
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
