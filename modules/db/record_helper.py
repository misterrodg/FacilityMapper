def segment_records(records: list[any], segment_fields: list[str]) -> list[list[any]]:
    def get_composite_key(record):
        return tuple(getattr(record, field, None) for field in segment_fields)

    last_key = None
    segment = []
    result = []

    for record in records:
        current_key = get_composite_key(record)
        if current_key != last_key and last_key is not None:
            result.append(segment)
            segment = []
        segment.append(record)
        last_key = current_key

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
