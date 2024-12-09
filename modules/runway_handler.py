from modules.draw_helper import (
    FEET_IN_NM,
    haversine_great_circle_bearing,
    inverse_bearing,
    lat_lon_from_pbd,
)
from modules.geo_json import Coordinate, Feature, LineString, MultiLineString


def get_line_strings(airport_list: list[list[dict]]) -> Feature:
    feature = Feature()
    multi_line_string = MultiLineString()
    for airport in airport_list:
        for runway in airport:
            line_string = LineString()
            base_lat = runway["base_lat"]
            base_lon = runway["base_lon"]
            base_displaced = runway["base_displaced"]
            base_coordinate = Coordinate(base_lat, base_lon)
            reciprocal_lat = runway["reciprocal_lat"]
            reciprocal_lon = runway["reciprocal_lon"]
            reciprocal_displaced = runway["reciprocal_displaced"]
            reciprocal_coordinate = Coordinate(reciprocal_lat, reciprocal_lon)
            if base_displaced > 0 or reciprocal_displaced > 0:
                base_course = haversine_great_circle_bearing(
                    base_lat, base_lon, reciprocal_lat, reciprocal_lon
                )
                if reciprocal_displaced > 0:
                    new_reciprocal = lat_lon_from_pbd(
                        reciprocal_lat,
                        reciprocal_lon,
                        base_course,
                        reciprocal_displaced / FEET_IN_NM,
                    )
                    reciprocal_coordinate = Coordinate(
                        new_reciprocal.get("lat"), new_reciprocal.get("lon")
                    )
                if base_displaced > 0:
                    reciprocal_course = inverse_bearing(base_course)
                    new_base = lat_lon_from_pbd(
                        base_lat,
                        base_lon,
                        reciprocal_course,
                        base_displaced / FEET_IN_NM,
                    )
                    base_coordinate = Coordinate(
                        new_base.get("lat"), new_base.get("lon")
                    )
            line_string.add_coordinate(base_coordinate)
            line_string.add_coordinate(reciprocal_coordinate)
            multi_line_string.add_line_string(line_string)
    feature.add_multi_line_string(multi_line_string)
    return feature
