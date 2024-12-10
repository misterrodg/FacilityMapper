def segment_records(records: list[any], segment_field: str) -> list[list[any]]:
    last_id = ""
    segment = []
    result = []
    for record in records:
        current_id = getattr(record, segment_field, None)
        if current_id != last_id and last_id != "":
            result.append(segment)
            segment = []
        segment.append(record)
        last_id = current_id
    if segment:
        result.append(segment)
    return result


def filter_records(records: list[any], segment_field: str) -> list[any]:
    result = []
    seen_ids = set()
    for record in records:
        field_value = getattr(record, segment_field, None)
        if field_value not in seen_ids:
            result.append(record)
            seen_ids.add(field_value)
    return result
