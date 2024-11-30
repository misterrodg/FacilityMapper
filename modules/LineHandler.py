from modules.DrawHelper import (
    haversine_great_circle_bearing,
    inverse_bearing,
    lat_lon_from_pbd,
)
from modules.GeoJSON import Coordinate, Feature, LineString, MultiLineString
from modules.QueryHelper import segment_query


def get_line_strings(
    db_rows: list, truncate: bool = False, symbol_scale: float = 1.0
) -> Feature:
    segment_list = segment_query(db_rows, "transition_id")
    feature = Feature()
    if truncate:
        multi_line_string = _draw_truncated_line(segment_list, symbol_scale)
    else:
        multi_line_string = _draw_simple_line(segment_list)
    feature.add_multi_line_string(multi_line_string)
    return feature


def _draw_simple_line(segment_list: list[list[dict]]) -> MultiLineString:
    multi_line_string = MultiLineString()
    for segment_item in segment_list:
        line_string = LineString()
        for segment in segment_item:
            lat = segment.get("lat")
            lon = segment.get("lon")
            if not lat or not lon:
                continue
            coordinate = Coordinate(lat, lon)
            line_string.add_coordinate(coordinate)
        multi_line_string.add_line_string(line_string)
    return multi_line_string


def _draw_truncated_line(
    segment_list: list[list[dict]], symbol_scale: float
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
                line_string = LineString()
                bearing = haversine_great_circle_bearing(
                    from_lat, from_lon, to_lat, to_lon
                )
                new_from = lat_lon_from_pbd(from_lat, from_lon, bearing, symbol_scale)
                inverse = inverse_bearing(bearing)
                new_to = lat_lon_from_pbd(to_lat, to_lon, inverse, symbol_scale)
                coordinate = Coordinate(new_from.get("lat"), new_from.get("lon"))
                line_string.add_coordinate(coordinate)
                coordinate = Coordinate(new_to.get("lat"), new_to.get("lon"))
                line_string.add_coordinate(coordinate)
                multi_line_string.add_line_string(line_string)
    return multi_line_string
