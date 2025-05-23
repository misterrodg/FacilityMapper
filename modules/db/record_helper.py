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


def segment_from_to(
    records: list[any], segment_field: str
) -> list[list[tuple[any, any]]]:
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
        result.append(cast_from_to(segment))
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


def cast_from_to(records: list[any]) -> list[tuple[any, any]]:
    return zip(records, records[1:])


def revert_from_to(records: list[tuple[any, any]]) -> list[any]:
    if not records:
        return []

    first_element = records[0][0]
    to_records = [to for _, to in records]

    return [first_element] + to_records
