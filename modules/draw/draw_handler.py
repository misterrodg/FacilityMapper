from modules.draw_helper import (
    haversine_great_circle_bearing,
    haversine_great_circle_distance,
    inverse_bearing,
    lat_lon_from_pbd,
    normalize_bearing,
)
from modules.geo_json import Coordinate, LineString

ARROW_ANGLE = 150.0
ARROW_LENGTH = 0.5
DEFAULT_DASH_LENGTH = 1.0


def draw_simple_line(
    from_lat: float,
    from_lon: float,
    to_lat: float,
    to_lon: float,
) -> list[Coordinate]:
    result = LineString()
    coordinate = Coordinate(from_lat, from_lon)
    result.add_coordinate(coordinate)
    coordinate = Coordinate(to_lat, to_lon)
    result.add_coordinate(coordinate)

    return result


def _normalize_pattern(pattern: list = None) -> list:
    if pattern is None:
        return [DEFAULT_DASH_LENGTH, DEFAULT_DASH_LENGTH]

    if not 1 <= len(pattern) <= 4:
        pattern = pattern[:4]
        print("Pattern must have between 1 and 4 values.")

    if len(pattern) == 1:
        return [pattern[0], pattern[0]]
    elif len(pattern) == 2:
        return list(pattern)
    elif len(pattern) == 3:
        return [pattern[0], pattern[1], pattern[2], pattern[1]]
    else:
        return list(pattern)


def draw_dashed_line(
    from_lat: float,
    from_lon: float,
    to_lat: float,
    to_lon: float,
    pattern: list = None,
    shift: bool = False,
) -> list[list[Coordinate]]:
    pattern = _normalize_pattern(pattern)
    result = []
    bearing = haversine_great_circle_bearing(from_lat, from_lon, to_lat, to_lon)
    total_distance = haversine_great_circle_distance(from_lat, from_lon, to_lat, to_lon)
    pattern_length = sum(pattern)
    full_patterns = int(total_distance // pattern_length)
    current_distance = 0
    EVEN_MODULUS = 2
    remainder = 1 if shift else 0

    for _ in range(full_patterns):
        for i, segment_length in enumerate(pattern):
            next_distance = current_distance + segment_length
            if i % EVEN_MODULUS == remainder:
                result.append(
                    _handle_dash_segment(
                        from_lat, from_lon, bearing, current_distance, next_distance
                    )
                )
            current_distance = next_distance

    for i, segment_length in enumerate(pattern):
        if current_distance >= total_distance:
            break
        next_distance = current_distance + segment_length
        if next_distance > total_distance:
            next_distance = total_distance
        if i % EVEN_MODULUS == remainder:
            result.append(
                _handle_dash_segment(
                    from_lat, from_lon, bearing, current_distance, next_distance
                )
            )
        current_distance = next_distance
    return result


def _handle_dash_segment(
    from_lat: float,
    from_lon: float,
    bearing: float,
    current_distance: float,
    next_distance: float,
) -> list[Coordinate]:
    result = []
    start_point = lat_lon_from_pbd(from_lat, from_lon, bearing, current_distance)
    coordinate = Coordinate(start_point.get("lat"), start_point.get("lon"))
    result.append(coordinate)

    end_point = lat_lon_from_pbd(from_lat, from_lon, bearing, next_distance)
    coordinate = Coordinate(end_point.get("lat"), end_point.get("lon"))
    result.append(coordinate)
    return result


def draw_truncated_line(
    self,
    from_lat: float,
    from_lon: float,
    to_lat: float,
    to_lon: float,
    buffer_length: float,
) -> list[Coordinate]:
    bearing = haversine_great_circle_bearing(from_lat, from_lon, to_lat, to_lon)
    new_from = lat_lon_from_pbd(from_lat, from_lon, bearing, buffer_length)
    inverse = inverse_bearing(bearing)
    new_to = lat_lon_from_pbd(to_lat, to_lon, inverse, buffer_length)

    result = self._draw_simple_line(
        new_from.get("lat"),
        new_from.get("lon"),
        new_to.get("lat"),
        new_to.get("lon"),
    )

    return result


def draw_vector_lines(
    from_lat: float,
    from_lon: float,
    course: float,
    vector_length: float,
) -> LineString:
    result = LineString()
    coordinate = Coordinate(from_lat, from_lon)
    result.add_coordinate(coordinate)

    end_point = lat_lon_from_pbd(from_lat, from_lon, course, vector_length)
    center_coordinate = Coordinate(end_point.get("lat"), end_point.get("lon"))
    result.add_coordinate(center_coordinate)

    left_angle = normalize_bearing(course - ARROW_ANGLE)
    vector_arrow_point = lat_lon_from_pbd(
        end_point.get("lat"), end_point.get("lon"), left_angle, ARROW_LENGTH
    )
    coordinate = Coordinate(
        vector_arrow_point.get("lat"), vector_arrow_point.get("lon")
    )
    result.add_coordinate(coordinate)

    result.add_coordinate(center_coordinate)

    right_angle = normalize_bearing(course + ARROW_ANGLE)
    vector_arrow_point = lat_lon_from_pbd(
        end_point.get("lat"), end_point.get("lon"), right_angle, ARROW_LENGTH
    )
    coordinate = Coordinate(
        vector_arrow_point.get("lat"), vector_arrow_point.get("lon")
    )
    result.add_coordinate(coordinate)

    return result
