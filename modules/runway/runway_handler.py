from modules.geo_json import Coordinate, Feature, LineString, MultiLineString
from modules.runway.runway_pair import RunwayPair


def get_line_strings(airport_list: list[list[RunwayPair]]) -> Feature:
    feature = Feature()
    multi_line_string = MultiLineString()
    for airport in airport_list:
        for runway_pair in airport:
            line_string = LineString()
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
