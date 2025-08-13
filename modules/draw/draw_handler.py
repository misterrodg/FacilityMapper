from .draw_helper import (
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
) -> LineString:
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
    from_lat: float,
    from_lon: float,
    to_lat: float,
    to_lon: float,
    buffer_length: float,
) -> LineString:
    bearing = haversine_great_circle_bearing(from_lat, from_lon, to_lat, to_lon)
    new_from = lat_lon_from_pbd(from_lat, from_lon, bearing, buffer_length)
    inverse = inverse_bearing(bearing)
    new_to = lat_lon_from_pbd(to_lat, to_lon, inverse, buffer_length)

    result = draw_simple_line(
        new_from.get("lat"),
        new_from.get("lon"),
        new_to.get("lat"),
        new_to.get("lon"),
    )

    return result


def _get_intermediate_bearings(
    num_segments: int,
    start_bearing: float = None,
    stop_bearing: float = None,
    direction: str = None,
) -> list:
    interval = 360 / num_segments

    if start_bearing is None or stop_bearing is None:
        bearings = [round(i * interval, 6) for i in range(num_segments + 1)]
        return bearings

    bearings = [round(i * interval, 6) - 360 for i in range(num_segments * 3 + 1)]

    if direction == "R":
        if stop_bearing <= start_bearing:
            stop_bearing += 360
    else:
        if stop_bearing >= start_bearing:
            stop_bearing -= 360
        bearings = bearings[::-1]

    start_index = 0
    stop_index = 0
    for i, bearing in enumerate(bearings):
        start_index = i
        if start_bearing < bearing and direction == "R":
            break
        if start_bearing > bearing and direction == "L":
            break
    bearings = bearings[start_index:]

    for i, bearing in enumerate(bearings):
        stop_index = i
        if stop_bearing < bearing and direction == "R":
            break
        if stop_bearing > bearing and direction == "L":
            break
    bearings = bearings[:stop_index]

    bearings = [start_bearing] + bearings + [stop_bearing]
    for i in range(len(bearings)):
        bearings[i] = bearings[i] % 360

    return bearings


def draw_arc(
    arc_lat: float,
    arc_lon: float,
    arc_radius_nm: float,
    start_lat: float,
    start_lon: float,
    stop_lat: float,
    stop_lon: float,
    direction: str = "R",
) -> LineString:
    result = LineString()

    start_bearing = haversine_great_circle_bearing(
        arc_lat, arc_lon, start_lat, start_lon
    )
    stop_bearing = haversine_great_circle_bearing(arc_lat, arc_lon, stop_lat, stop_lon)

    num_segments = max(36, int(arc_radius_nm * 4))

    bearings = _get_intermediate_bearings(
        num_segments, start_bearing, stop_bearing, direction
    )

    for bearing in bearings:
        new_point = lat_lon_from_pbd(arc_lat, arc_lon, bearing, arc_radius_nm)
        coordinate = Coordinate(new_point.get("lat"), new_point.get("lon"))
        result.add_coordinate(coordinate)
    return result


def _trim_coordinate_list(
    coordinate_list: list[Coordinate], buffer_length: float, backwards: bool = False
) -> list:
    start_index = 0
    final_index = len(coordinate_list) - 1 if not backwards else 0
    step = 1

    if backwards:
        start_index = len(coordinate_list) - 1
        final_index = 0
        step = -1

    previous_point = coordinate_list[start_index]
    remaining_distance = buffer_length

    for i in range(start_index, final_index, step):
        lat = coordinate_list[i].lat
        lon = coordinate_list[i].lon
        segment_distance = haversine_great_circle_distance(
            previous_point.lat, previous_point.lon, lat, lon
        )
        if remaining_distance < segment_distance:
            difference = segment_distance - remaining_distance
            bearing = haversine_great_circle_bearing(
                lat, lon, previous_point.lat, previous_point.lon
            )
            new_point = lat_lon_from_pbd(
                lat,
                lon,
                bearing,
                difference,
            )
            coordinate_list.insert(
                start_index, Coordinate(new_point.get("lat"), new_point.get("lon"))
            )
            break
        else:
            remaining_distance -= segment_distance
            previous_point = coordinate_list[i]
            coordinate_list[i] = None

    return coordinate_list


def draw_truncated_arc(
    arc_lat: float,
    arc_lon: float,
    arc_radius_nm: float,
    start_lat: float,
    start_lon: float,
    stop_lat: float,
    stop_lon: float,
    direction: str = "R",
    buffer_length: float = 0.0,
) -> LineString:
    result = draw_arc(
        arc_lat,
        arc_lon,
        arc_radius_nm,
        start_lat,
        start_lon,
        stop_lat,
        stop_lon,
        direction,
    )

    coordinates = result.coordinates
    _trim_coordinate_list(coordinates, buffer_length)
    _trim_coordinate_list(coordinates, buffer_length, True)

    i = 0
    while i < len(coordinates):
        if coordinates[i] is None:
            del coordinates[i]
        else:
            i += 1

    result.coordinates = coordinates
    return result


def draw_vector_lines(
    from_lat: float,
    from_lon: float,
    course: float,
    vector_length: float,
    buffer_length: float = 0.0,
) -> LineString:
    result = LineString()
    coordinate = Coordinate(from_lat, from_lon)

    if buffer_length > 0.0:
        shifted_coordinate = lat_lon_from_pbd(from_lat, from_lon, course, buffer_length)
        from_lat = shifted_coordinate.get("lat")
        from_lon = shifted_coordinate.get("lon")
        vector_length = vector_length - buffer_length
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
