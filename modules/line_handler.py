from modules.db import segment_query
from modules.draw_helper import (
    haversine_great_circle_bearing,
    haversine_great_circle_distance,
    inverse_bearing,
    normalize_bearing,
    lat_lon_from_pbd,
)
from modules.geo_json import Coordinate, Feature, LineString, MultiLineString

SHORT_DASH_LENGTH = 0.5
LONG_DASH_LENGTH = 1.5
ARROW_ANGLE = 150.0
ARROW_LENGTH = 0.5


def get_line_strings(
    db_rows: list,
    line_style: str,
    vector_length: float = 2.5,
    symbol_scale: float = 1.0,
    truncate: bool = False,
) -> Feature:
    segment_list = segment_query(db_rows, "transition_id")
    feature = Feature()
    if line_style == "solid" and not truncate:
        multi_line_string = _draw_simple_line(segment_list, vector_length)
    else:
        if truncate:
            multi_line_string = _draw_truncated_line(
                segment_list, line_style, symbol_scale, vector_length
            )
        else:
            multi_line_string = _draw_complex_line(segment_list, line_style)

    feature.add_multi_line_string(multi_line_string)
    return feature


def _draw_simple_line(
    segment_list: list[list[dict]], vector_length: float
) -> MultiLineString:
    last_segment = None
    multi_line_string = MultiLineString()
    for segment_item in segment_list:
        line_string = LineString()
        for segment in segment_item:
            path_term = segment.get("path_term")
            if path_term not in ["FM", "VM"]:
                lat = segment.get("lat")
                lon = segment.get("lon")
                if not lat or not lon:
                    continue
                coordinate = Coordinate(lat, lon)
                line_string.add_coordinate(coordinate)
            else:
                lat = None
                lon = None
                if path_term == "FM":
                    lat = segment.get("lat")
                    lon = segment.get("lon")

                if path_term == "VM":
                    lat = last_segment.get("lat")
                    lon = last_segment.get("lon")

                if lat is not None and lon is not None:
                    corrected_course = normalize_bearing(
                        segment.get("course") + segment.get("mag_var")
                    )
                    line = _draw_vector_lines(
                        lat,
                        lon,
                        corrected_course,
                        vector_length,
                    )
                    multi_line_string.add_line_string(line)

            last_segment = segment
        multi_line_string.add_line_string(line_string)
    return multi_line_string


def _draw_complex_line(
    segment_list: list[list[dict]], line_style: str
) -> MultiLineString:
    multi_line_string = MultiLineString()
    for segment_item in segment_list:
        if len(segment_item) > 1:
            for from_point, to_point in zip(segment_item, segment_item[1:]):
                from_lat = from_point.get("lat")
                from_lon = from_point.get("lon")
                to_lat = to_point.get("lat")
                to_lon = to_point.get("lon")
                if not from_lat or not from_lon or not to_lat or not to_lon:
                    continue
                line_string_list = _draw_dashed_line(
                    from_lat, from_lon, to_lat, to_lon, line_style
                )
                for line in line_string_list:
                    multi_line_string.add_line_string(line)
    return multi_line_string


def _draw_truncated_line(
    segment_list: list[list[dict]],
    line_style: str,
    symbol_scale: float,
    vector_length: float,
) -> MultiLineString:
    multi_line_string = MultiLineString()
    for segment_item in segment_list:
        if len(segment_item) > 1:
            for from_point, to_point in zip(segment_item, segment_item[1:]):
                path_term = to_point.get("path_term")
                if path_term not in ["FM", "VM"]:
                    from_lat = from_point.get("lat")
                    from_lon = from_point.get("lon")
                    to_lat = to_point.get("lat")
                    to_lon = to_point.get("lon")
                    if not from_lat or not from_lon or not to_lat or not to_lon:
                        continue
                    line_string = LineString()
                    bearing = haversine_great_circle_bearing(
                        from_lat, from_lon, to_lat, to_lon
                    )
                    new_from = lat_lon_from_pbd(
                        from_lat, from_lon, bearing, symbol_scale
                    )
                    inverse = inverse_bearing(bearing)
                    new_to = lat_lon_from_pbd(to_lat, to_lon, inverse, symbol_scale)
                    if line_style == "solid":
                        coordinate = Coordinate(
                            new_from.get("lat"), new_from.get("lon")
                        )
                        line_string.add_coordinate(coordinate)
                        coordinate = Coordinate(new_to.get("lat"), new_to.get("lon"))
                        line_string.add_coordinate(coordinate)
                        multi_line_string.add_line_string(line_string)
                    else:
                        line_string_list = _draw_dashed_line(
                            new_from.get("lat"),
                            new_from.get("lon"),
                            new_to.get("lat"),
                            new_to.get("lon"),
                            line_style,
                        )
                        for line in line_string_list:
                            multi_line_string.add_line_string(line)
                else:
                    if path_term == "FM":
                        corrected_course = normalize_bearing(
                            to_point.get("course") + to_point.get("mag_var")
                        )
                        new_from = lat_lon_from_pbd(
                            to_point.get("lat"),
                            to_point.get("lon"),
                            corrected_course,
                            symbol_scale,
                        )
                        line = _draw_vector_lines(
                            new_from.get("lat"),
                            new_from.get("lon"),
                            corrected_course,
                            vector_length,
                        )
                        multi_line_string.add_line_string(line)

                    if path_term == "VM":
                        corrected_course = normalize_bearing(
                            to_point.get("course") + from_point.get("mag_var")
                        )
                        new_from = lat_lon_from_pbd(
                            from_point.get("lat"),
                            from_point.get("lon"),
                            corrected_course,
                            symbol_scale,
                        )
                        line = _draw_vector_lines(
                            new_from.get("lat"),
                            new_from.get("lon"),
                            corrected_course,
                            vector_length,
                        )
                        multi_line_string.add_line_string(line)
    return multi_line_string


def _draw_dashed_line(
    from_lat: float,
    from_lon: float,
    to_lat: float,
    to_lon: float,
    line_style: str = "shortDashed",
) -> list[LineString]:
    result = []
    bearing = haversine_great_circle_bearing(from_lat, from_lon, to_lat, to_lon)
    total_distance = haversine_great_circle_distance(from_lat, from_lon, to_lat, to_lon)
    pattern = [SHORT_DASH_LENGTH, SHORT_DASH_LENGTH]
    if line_style == "longDashed":
        pattern = [LONG_DASH_LENGTH, LONG_DASH_LENGTH]
    if line_style == "longDashShortDash":
        pattern = [
            LONG_DASH_LENGTH,
            SHORT_DASH_LENGTH,
            SHORT_DASH_LENGTH,
            SHORT_DASH_LENGTH,
        ]
    pattern_length = sum(pattern)
    full_patterns = int(total_distance // pattern_length)
    current_distance = 0

    for _ in range(full_patterns):
        for i, segment_length in enumerate(pattern):
            next_distance = current_distance + segment_length
            if i % 2 == 0:
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
        if i % 2 == 0:
            result.append(
                _handle_dash_segment(
                    from_lat, from_lon, bearing, current_distance, next_distance
                )
            )
        current_distance = next_distance
    return result


def _draw_vector_lines(
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


def _handle_dash_segment(
    from_lat: float,
    from_lon: float,
    bearing: float,
    current_distance: float,
    next_distance: float,
) -> LineString:
    result = LineString()
    start_point = lat_lon_from_pbd(from_lat, from_lon, bearing, current_distance)
    coordinate = Coordinate(start_point.get("lat"), start_point.get("lon"))
    result.add_coordinate(coordinate)

    end_point = lat_lon_from_pbd(from_lat, from_lon, bearing, next_distance)
    coordinate = Coordinate(end_point.get("lat"), end_point.get("lon"))
    result.add_coordinate(coordinate)
    return result
