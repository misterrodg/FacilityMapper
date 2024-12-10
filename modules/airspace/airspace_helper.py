from modules.draw_helper import (
    haversine_great_circle_bearing,
    lat_lon_from_pbd,
)
from modules.geo_json import (
    Coordinate,
    LineString,
)


def draw_arc(
    arc_lat: float,
    arc_lon: float,
    arc_radius_nm: float,
    start_lat: float,
    start_lon: float,
    stop_lat: float,
    stop_lon: float,
    direction: str = "R",
) -> list[Coordinate]:
    result = []

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
        result.append(coordinate)
    return result


def draw_circle(center_lat: float, center_lon: float, radius_nm: float) -> LineString:
    line_string = LineString()

    num_segments = max(36, int(radius_nm * 4))

    bearings = _get_intermediate_bearings(num_segments)

    for bearing in bearings:
        new_point = lat_lon_from_pbd(center_lat, center_lon, bearing, radius_nm)
        coordinate = Coordinate(new_point.get("lat"), new_point.get("lon"))
        line_string.add_coordinate(coordinate)
    return line_string


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
