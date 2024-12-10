from modules.db.airspace_record import AirspaceRecord
from modules.airspace.airspace_helper import draw_arc, draw_circle
from modules.geo_json import Coordinate, Feature, FeatureCollection, LineString


def get_line_strings(
    airspace_segments: list[list[AirspaceRecord]],
) -> FeatureCollection:
    feature_collection = FeatureCollection()
    for segment in airspace_segments:
        feature = Feature()
        if len(segment) > 1:
            line_string = LineString()
            shifted_item = segment[1:] + segment[:1]
            last_boundary_type = None
            for from_point, to_point in zip(segment, shifted_item):
                boundary_via = from_point.boundary_via
                boundary_type = from_point.boundary_type
                end_marker = from_point.end_marker
                next_boundary_type = to_point.boundary_type
                if boundary_type in ["L", "R"]:
                    start_lat = from_point.lat
                    start_lon = from_point.lon
                    arc_lat = from_point.arc_lat
                    arc_lon = from_point.arc_lon
                    arc_radius_nm = from_point.arc_dist
                    stop_lat = to_point.lat
                    stop_lon = to_point.lon
                    arc_lines = draw_arc(
                        arc_lat,
                        arc_lon,
                        arc_radius_nm,
                        start_lat,
                        start_lon,
                        stop_lat,
                        stop_lon,
                        boundary_type,
                    )
                    line_string.add_coordinates(arc_lines)
                if boundary_type in ["G", "H"]:
                    if (
                        last_boundary_type in ["L", "R"]
                        and next_boundary_type in ["L", "R"]
                        and end_marker != "E"
                    ):
                        continue
                    lat = from_point.lat
                    lon = from_point.lon
                    coordinate = Coordinate(lat, lon)
                    line_string.add_coordinate(coordinate)
                if end_marker == "E":
                    line_string.close_line()
                last_boundary_type = boundary_type
            feature.add_line_string(line_string)
        else:
            line = segment[0]
            boundary_via = line.boundary_via
            if boundary_via == "CE":
                center_lat = line.arc_lat
                center_lon = line.arc_lon
                radius_nm = line.arc_dist
                circle_lines = draw_circle(center_lat, center_lon, radius_nm)
                feature.add_line_string(circle_lines)
        feature_collection.add_feature(feature)
    return feature_collection
