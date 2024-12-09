from modules.geo_json import Coordinate, Feature, LineString, MultiLineString
from modules.runway import RunwayPair


def get_line_strings(airport_list: list[list[dict]]) -> Feature:
    feature = Feature()
    multi_line_string = MultiLineString()
    for airport in airport_list:
        for runway in airport:
            line_string = LineString()
            airport_id = runway["airport_id"]
            base_id = runway["base_id"]
            base_lat = runway["base_lat"]
            base_lon = runway["base_lon"]
            base_displaced = runway["base_displaced"]
            reciprocal_id = runway["reciprocal_id"]
            reciprocal_lat = runway["reciprocal_lat"]
            reciprocal_lon = runway["reciprocal_lon"]
            reciprocal_displaced = runway["reciprocal_displaced"]
            runway_pair = RunwayPair(
                airport_id,
                base_id,
                base_lat,
                base_lon,
                base_displaced,
                reciprocal_id,
                reciprocal_lat,
                reciprocal_lon,
                reciprocal_displaced,
            )
            if runway_pair.is_valid:
                base_coordinate = Coordinate(
                    runway_pair.base_lat, runway_pair.base_displaced_lon
                )
                reciprocal_coordinate = Coordinate(
                    runway_pair.reciprocal_lat, runway_pair.reciprocal_lon
                )
                line_string.add_coordinate(base_coordinate)
                line_string.add_coordinate(reciprocal_coordinate)
                multi_line_string.add_line_string(line_string)
    feature.add_multi_line_string(multi_line_string)
    return feature
