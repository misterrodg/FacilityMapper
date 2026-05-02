from typing import Any, TypeVar


T = TypeVar("T")


def segment_records(records: list[T], segment_field: str) -> list[list[T]]:
    sentinel = object()
    last_id: Any = sentinel
    segment: list[T] = []
    result: list[list[T]] = []
    for record in records:
        current_id = getattr(record, segment_field, None)
        if current_id != last_id and last_id is not sentinel:
            result.append(segment)
            segment = []
        segment.append(record)
        last_id = current_id
    if segment:
        result.append(segment)
    return result


def segment_from_to(
    records: list[T], segment_field: str
) -> list[list[tuple[T, T]]]:
    sentinel = object()
    last_id: Any = sentinel
    segment: list[T] = []
    result: list[list[tuple[T, T]]] = []
    for record in records:
        current_id = getattr(record, segment_field, None)
        if current_id != last_id and last_id is not sentinel:
            result.append(cast_from_to(segment))
            segment = []
        segment.append(record)
        last_id = current_id
    if segment:
        result.append(cast_from_to(segment))
    return result


def filter_records(records: list[T], segment_field: str) -> list[T]:
    result: list[T] = []
    seen_ids: set[Any] = set()
    for record in records:
        field_value = getattr(record, segment_field, None)
        if field_value not in seen_ids:
            result.append(record)
            seen_ids.add(field_value)
    return result


def cast_from_to(records: list[T]) -> list[tuple[T, T]]:
    return list(zip(records, records[1:]))


def revert_from_to(records: list[tuple[T, T]]) -> list[T]:
    if not records:
        return []

    first_element = records[0][0]
    to_records = [to for _, to in records]

    return [first_element] + to_records
