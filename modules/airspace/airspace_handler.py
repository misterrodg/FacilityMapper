from modules.db.airspace_record import AirspaceRecord
from modules.airspace.airspace_helper import draw_arc, draw_circle
from modules.geo_json import Coordinate, Feature, FeatureCollection, LineString


def get_line_strings(
    airspace_segments: list[list[AirspaceRecord]],
) -> FeatureCollection:
    feature_collection = FeatureCollection()
    for segment in airspace_segments:
        if len(segment) > 1:
            feature = _build_multi_segment_feature(segment)
            feature_collection.add_feature(feature)
        else:
            feature = _build_single_segment_feature(segment[0])
            if feature is not None:
                feature_collection.add_feature(feature)
    return feature_collection


def _build_multi_segment_feature(segment: list[AirspaceRecord]) -> Feature:
    feature = Feature()
    line_string = LineString()
    shifted_item = segment[1:] + segment[:1]
    last_boundary_type: str | None = None
    for from_point, to_point in zip(segment, shifted_item):
        boundary_type = from_point.boundary_type
        end_marker = from_point.end_marker
        next_boundary_type = to_point.boundary_type
        if boundary_type in ["L", "R"]:
            _process_arc_segment(line_string, from_point, to_point, boundary_type)
        if boundary_type in ["G", "H"]:
            _process_great_circle_point(
                line_string, from_point, last_boundary_type, next_boundary_type, end_marker
            )
        if end_marker == "E":
            line_string.close_line()
        last_boundary_type = boundary_type
    feature.add_line_string(line_string)
    return feature


def _process_arc_segment(
    line_string: LineString,
    from_point: AirspaceRecord,
    to_point: AirspaceRecord,
    boundary_type: str,
) -> None:
    arc_lat = from_point.arc_lat
    arc_lon = from_point.arc_lon
    arc_radius_nm = from_point.arc_dist
    start_lat = from_point.lat
    start_lon = from_point.lon
    stop_lat = to_point.lat
    stop_lon = to_point.lon
    if (
        arc_lat is None
        or arc_lon is None
        or arc_radius_nm is None
        or start_lat is None
        or start_lon is None
        or stop_lat is None
        or stop_lon is None
    ):
        return
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


def _process_great_circle_point(
    line_string: LineString,
    from_point: AirspaceRecord,
    last_boundary_type: str | None,
    next_boundary_type: str | None,
    end_marker: str | None,
) -> None:
    if (
        last_boundary_type in ["L", "R"]
        and next_boundary_type in ["L", "R"]
        and end_marker != "E"
    ):
        return
    lat = from_point.lat
    lon = from_point.lon
    if lat is None or lon is None:
        return
    line_string.add_coordinate(Coordinate(lat, lon))


def _build_single_segment_feature(line: AirspaceRecord) -> Feature | None:
    if line.boundary_via != "CE":
        return Feature()
    center_lat = line.arc_lat
    center_lon = line.arc_lon
    radius_nm = line.arc_dist
    if center_lat is None or center_lon is None or radius_nm is None:
        return None
    feature = Feature()
    feature.add_line_string(draw_circle(center_lat, center_lon, radius_nm))
    return feature
