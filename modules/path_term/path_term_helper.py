from modules.db import JoinedProcedureRecord
from modules.draw import (
    draw_arc,
    haversine_great_circle_bearing,
    lat_lon_from_pbd,
    normalize_bearing,
    EARTH_RADIUS_NM,
)
from modules.geo_json import Coordinate

import math
from typing import Any, TypeGuard

SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOUR_TO_SECOND = MINUTES_PER_HOUR * SECONDS_PER_MINUTE
GROUND_SPEED = 200
CLIMB_RATE = 1000
STANDARD_TURN_RATE = 3
STANDARD_INTERCEPT = 30
STANDARD_HOLD_DIR = "R"
TURN_TOLERANCE = 45


def _validate_and_extract_coordinate(
    coordinate: Coordinate | None, name: str = "coordinate"
) -> tuple[float, float] | None:
    if not _validate_coordinate_values(coordinate, name):
        print(f"{name}: invalid coordinate — skipping leg")
        return None
    values = _coordinate_to_tuple(coordinate)
    if values is None:
        print(f"{name}: invalid coordinate values — skipping leg")
        return None
    return values


def _validate_and_extract_bearing(
    bearing: float | None, name: str = "bearing"
) -> float | None:
    if not _validate_bearing(bearing, name):
        print(f"{name}: cannot determine bearing — skipping leg")
        return None
    return bearing


def _dme_intersection_handler(
    last_lat, last_lon, bearing, dme_lat, dme_lon, dme_distance, label
):
    if dme_lat is None or dme_lon is None or dme_distance is None:
        print(f"{label}: DME source coordinates/distance missing — skipping leg")
        return None
    intersection = _intersection_from_bearing_along_circle(
        last_lat, last_lon, bearing, dme_lat, dme_lon, dme_distance
    )
    if intersection is None:
        print(f"{label}: course {bearing} does not intersect DME arc — skipping leg")
        return None
    intersection_values = _lat_lon_dict_to_tuple(intersection)
    if intersection_values is None:
        print(f"{label}: invalid intersection point — skipping leg")
        return None
    return intersection_values


def _altitude_endpoint_handler(
    initial_lat, initial_lon, bearing, initial_altitude, target_altitude, label
):
    altitude_distance = _altitudes_to_distance(initial_altitude, target_altitude)
    end_of_climb = lat_lon_from_pbd(
        initial_lat, initial_lon, bearing, altitude_distance
    )
    end_values = _lat_lon_dict_to_tuple(end_of_climb)
    if end_values is None:
        print(f"{label}: unable to compute climb endpoint — skipping leg")
        return None
    return end_values


def _validate_coordinate_values(
    coordinate: Coordinate | None, name: str = "coordinate"
) -> bool:
    """Check that a Coordinate has valid lat/lon. Return False if either is None."""
    if coordinate is None or coordinate.lat is None or coordinate.lon is None:
        return False
    return True


def _validate_bearing(bearing: float | None, name: str = "bearing") -> TypeGuard[float]:
    """Check that a bearing is not None."""
    return bearing is not None


class SymbolPoint:
    type: str
    coordinate: Coordinate
    rotation: float

    def __init__(self, type: str, coordinate: Coordinate, rotation: float):
        self.type = type
        self.coordinate = coordinate
        self.rotation = rotation


class PathData:
    last_bearing: float | None
    coordinates: list[Coordinate]
    symbol_points: list[SymbolPoint]

    def __init__(
        self,
        last_bearing: float | None = None,
        coordinates: list[Coordinate] | None = None,
        symbol_points: list[SymbolPoint] | None = None,
    ):
        self.last_bearing = last_bearing
        self.coordinates = coordinates if coordinates is not None else []
        self.symbol_points = symbol_points if symbol_points is not None else []

    def get_last_coordinate(self) -> Coordinate | None:
        return self.coordinates[-1] if len(self.coordinates) > 0 else None


def _coordinate_to_tuple(coordinate: Coordinate | None) -> tuple[float, float] | None:
    if coordinate is None:
        return None
    lat = coordinate.lat
    lon = coordinate.lon
    if lat is None or lon is None:
        return None
    return lat, lon


def _lat_lon_dict_to_tuple(point: dict[str, Any] | None) -> tuple[float, float] | None:
    if point is None:
        return None
    lat = point.get("lat")
    lon = point.get("lon")
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return None
    return float(lat), float(lon)


def _wrap360(x: float) -> float:
    return x % 360.0


def _wrap180(x: float) -> float:
    y = (x + 180.0) % 360.0 - 180.0
    return y if y != -180.0 else 180.0


def _side_of_inbound_track(
    lat_a: float, lon_a: float, lat_b: float, lon_b: float, inbound_course_to_b: float
) -> str:
    """
    Returns 'R' if A is to the right of the inbound track to B,
            'L' if to the left (right/left defined looking *along the inbound course* toward B).
    """
    course_out_of_b = _wrap360(inbound_course_to_b + 180.0)
    brg_b_to_a = haversine_great_circle_bearing(lat_b, lon_b, lat_a, lon_a)
    diff = _wrap180(brg_b_to_a - course_out_of_b)
    return "R" if diff > 0 else "L"


def _calculate_standard_intercept(
    lat_a: float,
    lon_a: float,
    lat_b: float,
    lon_b: float,
    inbound_course_to_b: float,
    offset_deg: float = STANDARD_INTERCEPT,
) -> tuple[str, float]:
    side = _side_of_inbound_track(lat_a, lon_a, lat_b, lon_b, inbound_course_to_b)
    trial = inbound_course_to_b + (offset_deg if side == "R" else -offset_deg)
    return side, _wrap360(trial)


def _return_coordinate(
    joined_procedure_record: JoinedProcedureRecord,
) -> Coordinate | None:
    if (
        joined_procedure_record.fix_lat is None
        or joined_procedure_record.fix_lon is None
    ):
        return None
    return Coordinate(joined_procedure_record.fix_lat, joined_procedure_record.fix_lon)


def _altitudes_to_distance(initial: float, desired: float) -> float:
    return abs(initial - desired) / CLIMB_RATE


def _correct_course(
    joined_procedure_record: JoinedProcedureRecord, last_course: float | None = None
) -> float | None:
    if joined_procedure_record.course is None and last_course is None:
        return None
    course = last_course if last_course is not None else joined_procedure_record.course
    if course is None:
        return None
    if joined_procedure_record.fix_mag_var is not None:
        return normalize_bearing(course + joined_procedure_record.fix_mag_var)
    if joined_procedure_record.rec_vhf_mag_var is not None:
        return normalize_bearing(course + joined_procedure_record.rec_vhf_mag_var)
    if joined_procedure_record.airport_mag_var is not None:
        return normalize_bearing(course + joined_procedure_record.airport_mag_var)
    return normalize_bearing(course)


def _is_forward(lat_from, lon_from, brg, lat_to, lon_to, tolerance=5.0):
    """Check that the candidate lies along the intended course (within tolerance)."""
    brg_gc = haversine_great_circle_bearing(lat_from, lon_from, lat_to, lon_to)
    return abs(_ang_diff(brg_gc, brg)) < tolerance


def _intersection_candidates(lat_1, lon_1, brg_1, lat_2, lon_2, brg_2):
    """Return both possible intersection points of two great-circle bearings."""
    phi_1, lam_1, brg_1 = map(math.radians, [lat_1, lon_1, brg_1])
    phi_2, lam_2, brg_2 = map(math.radians, [lat_2, lon_2, brg_2])

    d_lam = lam_2 - lam_1

    bearing_12 = math.atan2(
        math.sin(d_lam) * math.cos(phi_2),
        math.cos(phi_1) * math.sin(phi_2)
        - math.sin(phi_1) * math.cos(phi_2) * math.cos(d_lam),
    )
    bearing_21 = math.atan2(
        math.sin(-d_lam) * math.cos(phi_1),
        math.cos(phi_2) * math.sin(phi_1)
        - math.sin(phi_2) * math.cos(phi_1) * math.cos(-d_lam),
    )

    d_phi = phi_2 - phi_1
    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi_1) * math.cos(phi_2) * math.sin(d_lam / 2) ** 2
    )
    delta_sigma = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    angle1 = math.acos(
        math.sin(brg_1) * math.sin(bearing_12) + math.cos(brg_1) * math.cos(bearing_12)
    )
    angle2 = math.acos(
        math.sin(brg_2) * math.sin(bearing_21) + math.cos(brg_2) * math.cos(bearing_21)
    )

    angle_int = math.acos(
        -math.cos(angle1) * math.cos(angle2)
        + math.sin(angle1) * math.sin(angle2) * math.cos(delta_sigma)
    )

    d1 = math.atan2(math.sin(delta_sigma) * math.sin(angle2), math.sin(angle_int))

    phi_int1 = math.asin(
        math.sin(phi_1) * math.cos(d1)
        + math.cos(phi_1) * math.sin(d1) * math.cos(brg_1)
    )
    lam_int1 = lam_1 + math.atan2(
        math.sin(brg_1) * math.sin(d1) * math.cos(phi_1),
        math.cos(d1) - math.sin(phi_1) * math.sin(phi_int1),
    )

    phi_int2 = -phi_int1
    lam_int2 = (lam_int1 + math.pi) % (2 * math.pi) - math.pi

    return [
        {"lat": math.degrees(phi_int1), "lon": math.degrees(lam_int1)},
        {"lat": math.degrees(phi_int2), "lon": math.degrees(lam_int2)},
    ]


def _intersection_from_bearings(lat_1, lon_1, brg_1, lat_2, lon_2, brg_2):
    candidates = _intersection_candidates(lat_1, lon_1, brg_1, lat_2, lon_2, brg_2)
    for candidate in candidates:
        if _is_forward(
            lat_1, lon_1, brg_1, candidate["lat"], candidate["lon"]
        ) and _is_forward(lat_2, lon_2, brg_2, candidate["lat"], candidate["lon"]):
            return candidate
    return None


def _intersection_from_bearing_along_circle(
    path_lat_deg: float,
    path_lon_deg: float,
    path_bearing_deg: float,
    center_lat_deg: float,
    center_lon_deg: float,
    circle_radius_nm: float,
) -> dict[str, float] | None:
    path_lat = math.radians(path_lat_deg)
    path_lon = math.radians(path_lon_deg)
    path_bearing = math.radians(path_bearing_deg)

    center_lat = math.radians(center_lat_deg)
    center_lon = math.radians(center_lon_deg)

    delta_lon = center_lon - path_lon

    y = math.sin(delta_lon) * math.cos(center_lat)
    x = math.cos(path_lat) * math.sin(center_lat) - math.sin(path_lat) * math.cos(
        center_lat
    ) * math.cos(delta_lon)

    bearing_to_center = math.atan2(y, x)

    great_circle_distance_rad = math.acos(
        math.sin(path_lat) * math.sin(center_lat)
        + math.cos(path_lat) * math.cos(center_lat) * math.cos(delta_lon)
    )

    cross_track_distance_rad = math.asin(
        math.sin(great_circle_distance_rad) * math.sin(bearing_to_center - path_bearing)
    )

    cross_track_distance_nm = cross_track_distance_rad * EARTH_RADIUS_NM

    if abs(cross_track_distance_nm) > circle_radius_nm:
        return None

    along_track_distance_rad = math.atan2(
        math.sin(great_circle_distance_rad)
        * math.cos(bearing_to_center - path_bearing),
        math.cos(great_circle_distance_rad),
    )
    along_track_distance_nm = along_track_distance_rad * EARTH_RADIUS_NM

    offset_nm = math.sqrt(circle_radius_nm**2 - cross_track_distance_nm**2)

    dist1_nm = along_track_distance_nm - offset_nm
    dist2_nm = along_track_distance_nm + offset_nm

    def calculate_destination(
        start_lat: float, start_lon: float, bearing: float, distance_nm: float
    ) -> dict[str, float]:
        angular_dist = distance_nm / EARTH_RADIUS_NM
        new_lat = math.asin(
            math.sin(start_lat) * math.cos(angular_dist)
            + math.cos(start_lat) * math.sin(angular_dist) * math.cos(bearing)
        )
        new_lon = start_lon + math.atan2(
            math.sin(bearing) * math.sin(angular_dist) * math.cos(start_lat),
            math.cos(angular_dist) - math.sin(start_lat) * math.sin(new_lat),
        )
        result = {"lat": math.degrees(new_lat), "lon": math.degrees(new_lon)}
        return result

    result = None
    if dist1_nm >= 0:
        result = calculate_destination(path_lat, path_lon, path_bearing, dist1_nm)
    if dist2_nm >= 0:
        if not result or (abs(dist2_nm - dist1_nm) > 1e-9):
            result = calculate_destination(path_lat, path_lon, path_bearing, dist2_nm)

    return result


def _ang_diff(a: float, b: float) -> float:
    return abs(((a - b + 540) % 360) - 180)


def _tangent_heading(rad: float, turn_direction: str) -> float:
    return (rad + (90 if turn_direction == "R" else -90)) % 360


def _should_turn(
    last_bearing: float,
    next_bearing: float,
    tolerance: float = TURN_TOLERANCE,
) -> bool:
    angular_difference = _ang_diff(last_bearing, next_bearing)
    if angular_difference > tolerance:
        return True
    return False


def _arc_to_fix(
    lat_a: float,
    lon_a: float,
    bearing: float,
    lat_b: float,
    lon_b: float,
    turn_direction: str | None = None,
    speed_kt: float = GROUND_SPEED,
    turn_rate_dps: float = STANDARD_TURN_RATE,
    step_deg: float = 1.0,
    tolerance_deg: float = 0.5,
    max_sweep_deg: float = 540.0,
) -> PathData:
    result = PathData()
    direct_bearing = haversine_great_circle_bearing(lat_a, lon_a, lat_b, lon_b)
    if turn_direction is None:
        right_delta = (direct_bearing - bearing + 360) % 360
        left_delta = (bearing - direct_bearing + 360) % 360
        turn_direction = "R" if right_delta <= left_delta else "L"

    omega = math.radians(turn_rate_dps)
    v = speed_kt / HOUR_TO_SECOND
    radius_nm = v / omega if omega > 0 else 0.0

    center_az = (bearing + (90 if turn_direction == "R" else -90)) % 360
    center_coordinate = lat_lon_from_pbd(lat_a, lon_a, center_az, radius_nm)
    center_values = _lat_lon_dict_to_tuple(center_coordinate)
    if center_values is None:
        result.last_bearing = direct_bearing
        result.coordinates = [Coordinate(lat_a, lon_a), Coordinate(lat_b, lon_b)]
        return result
    center_lat, center_lon = center_values

    radial = haversine_great_circle_bearing(
        center_lat,
        center_lon,
        lat_a,
        lon_a,
    )

    cur_lat, cur_lon = lat_a, lon_a

    if (
        _ang_diff(
            _tangent_heading(radial, turn_direction),
            haversine_great_circle_bearing(cur_lat, cur_lon, lat_b, lon_b),
        )
        <= tolerance_deg
    ):
        result.last_bearing = radial
        result.coordinates = [Coordinate(lat_a, lon_a), Coordinate(cur_lat, cur_lon)]
        return result

    swept = 0.0
    step = abs(step_deg)
    signed_step = step if turn_direction == "R" else -step

    while swept <= max_sweep_deg:
        radial = (radial + signed_step) % 360
        swept += step

        p = lat_lon_from_pbd(
            center_lat,
            center_lon,
            radial,
            radius_nm,
        )
        point_values = _lat_lon_dict_to_tuple(p)
        if point_values is None:
            result.last_bearing = radial
            result.coordinates = [Coordinate(lat_a, lon_a), Coordinate(lat_b, lon_b)]
            return result
        cur_lat, cur_lon = point_values

        to_bearing = haversine_great_circle_bearing(cur_lat, cur_lon, lat_b, lon_b)
        if (
            _ang_diff(_tangent_heading(radial, turn_direction), to_bearing)
            <= tolerance_deg
        ):
            break
    else:
        result.last_bearing = radial
        result.coordinates = [Coordinate(lat_a, lon_a), Coordinate(cur_lat, cur_lon)]
        return result

    arc = draw_arc(
        center_lat,
        center_lon,
        radius_nm,
        lat_a,
        lon_a,
        cur_lat,
        cur_lon,
        turn_direction,
    )
    result.last_bearing = _tangent_heading(radial, turn_direction)
    result.coordinates = arc.coordinates
    return result


def _total_turn_degrees(
    current_course: float, target_course: float, turn_direction: str | None
) -> tuple[str, float]:
    raw_diff = target_course - current_course
    normalized_shortest_path = (raw_diff + 180) % 360 - 180
    turn_angle = normalized_shortest_path

    if turn_direction:
        if turn_direction == "R":
            if normalized_shortest_path < 0:
                turn_angle = 360 + normalized_shortest_path
        elif turn_direction == "L":
            if normalized_shortest_path > 0:
                turn_angle = normalized_shortest_path - 360
        else:
            print(
                f"Warning: Invalid direction preference '{turn_direction}'. Reverting to shortest path."
            )
    else:
        # If turn_direction is None and turn is exactly 180°, default to left turn
        if abs(abs(normalized_shortest_path) - 180.0) < 0.1:
            turn_angle = -180.0

    if turn_angle < 0:
        direction = "L"
        magnitude = abs(turn_angle)
    else:
        direction = "R"
        magnitude = turn_angle

    return direction, magnitude


def _generate_turn_arc_coordinates(
    center_lat: float,
    center_lon: float,
    radius_nm: float,
    start_radial: float,
    end_radial: float,
    direction: str,
    step_deg: float = 0.5,
) -> list[Coordinate]:
    result: list[Coordinate] = []

    start = normalize_bearing(start_radial)
    end = normalize_bearing(end_radial)

    start_point = _lat_lon_dict_to_tuple(
        lat_lon_from_pbd(center_lat, center_lon, start, radius_nm)
    )
    if start_point is not None:
        result.append(Coordinate(start_point[0], start_point[1]))

    if direction == "R":
        sweep = (end - start + 360) % 360
        progressed = step_deg
        while progressed < sweep:
            radial = normalize_bearing(start + progressed)
            point = _lat_lon_dict_to_tuple(
                lat_lon_from_pbd(center_lat, center_lon, radial, radius_nm)
            )
            if point is not None:
                result.append(Coordinate(point[0], point[1]))
            progressed += step_deg
    else:
        sweep = (start - end + 360) % 360
        progressed = step_deg
        while progressed < sweep:
            radial = normalize_bearing(start - progressed)
            point = _lat_lon_dict_to_tuple(
                lat_lon_from_pbd(center_lat, center_lon, radial, radius_nm)
            )
            if point is not None:
                result.append(Coordinate(point[0], point[1]))
            progressed += step_deg

    end_point = _lat_lon_dict_to_tuple(
        lat_lon_from_pbd(center_lat, center_lon, end, radius_nm)
    )
    if end_point is not None:
        result.append(Coordinate(end_point[0], end_point[1]))

    return result


def _turn_arc(
    lat_a: float,
    lon_a: float,
    bearing: float,
    turn_degrees: float,
    turn_direction: str | None = STANDARD_HOLD_DIR,
    speed_kt: float = GROUND_SPEED,
    turn_rate_dps: float = STANDARD_TURN_RATE,
) -> PathData:
    resolved_turn_direction = (
        turn_direction if turn_direction is not None else STANDARD_HOLD_DIR
    )

    omega = math.radians(turn_rate_dps)
    v = speed_kt / HOUR_TO_SECOND
    radius_nm = v / omega if omega > 0 else 0.0

    center_az = (bearing + (90 if resolved_turn_direction == "R" else -90)) % 360
    center = lat_lon_from_pbd(lat_a, lon_a, center_az, radius_nm)
    center_values = _lat_lon_dict_to_tuple(center)
    if center_values is None:
        return PathData(bearing, [Coordinate(lat_a, lon_a)], [])
    center_lat, center_lon = center_values

    # Use center-based radial sweep for endpoint geometry. A course is tangent to
    # the arc and cannot be used directly as a center radial.
    start_radial = haversine_great_circle_bearing(center_lat, center_lon, lat_a, lon_a)
    end_radial = (
        start_radial
        + (turn_degrees if resolved_turn_direction == "R" else -turn_degrees)
    ) % 360

    end_point = lat_lon_from_pbd(center_lat, center_lon, end_radial, radius_nm)
    end_values = _lat_lon_dict_to_tuple(end_point)
    if end_values is None:
        return PathData(bearing, [Coordinate(lat_a, lon_a)], [])

    end_bearing = _tangent_heading(end_radial, resolved_turn_direction)

    arc_coordinates = _generate_turn_arc_coordinates(
        center_lat,
        center_lon,
        radius_nm,
        start_radial,
        end_radial,
        resolved_turn_direction,
    )
    if not arc_coordinates:
        arc_coordinates = [
            Coordinate(lat_a, lon_a),
            Coordinate(end_values[0], end_values[1]),
        ]

    symbol_points = [SymbolPoint("CIRCLE_S", arc_coordinates[-1], 0)]

    result = PathData(end_bearing, arc_coordinates, symbol_points)
    return result


def _calculate_radial_reintercept_turn(
    lat_a: float,
    lon_a: float,
    current_heading: float,
    fix_lat: float,
    fix_lon: float,
    published_inbound_radial: float,
    turn_direction: str | None = None,
    speed_kt: float = GROUND_SPEED,
    turn_rate_dps: float = STANDARD_TURN_RATE,
) -> tuple[str, float]:
    """
    Calculate the turn needed to re-intercept a published radial from a fix.

    When on a reversal leg (e.g., FA→CF), the aircraft needs to turn back toward
    the fix along the published inbound radial. This calculates the geometric
    re-intercept point where the aircraft's turn circle intersects the radial line,
    then returns the turn direction and degrees needed to reach that point.

    Args:
        lat_a, lon_a: Current aircraft position
        current_heading: Current track/heading (outbound)
        fix_lat, fix_lon: Fix position
        published_inbound_radial: The radial we must re-intercept (e.g., 340° from HLN)
        turn_direction: Override turn direction if specified
        speed_kt, turn_rate_dps: Aircraft dynamics for turn radius calculation

    Returns:
        (turn_direction, turn_degrees) to reach the re-intercept point
    """
    # Calculate outbound radial from fix (opposite of inbound)
    outbound_radial = (published_inbound_radial + 180.0) % 360.0

    # Calculate turn radius based on dynamics
    omega = math.radians(turn_rate_dps)
    v = speed_kt / HOUR_TO_SECOND
    radius_nm = v / omega if omega > 0 else 0.0

    # Determine turn direction if not specified
    if turn_direction is None:
        # Choose direction that turns toward the fix
        to_fix = haversine_great_circle_bearing(lat_a, lon_a, fix_lat, fix_lon)
        right_delta = (to_fix - current_heading + 360) % 360
        left_delta = (current_heading - to_fix + 360) % 360
        turn_direction = "R" if right_delta <= left_delta else "L"

    # Calculate turn circle center
    center_az = (current_heading + (90 if turn_direction == "R" else -90)) % 360
    center = lat_lon_from_pbd(lat_a, lon_a, center_az, radius_nm)
    center_values = _lat_lon_dict_to_tuple(center)
    if center_values is None:
        # Fallback: just turn toward the fix
        to_fix = haversine_great_circle_bearing(lat_a, lon_a, fix_lat, fix_lon)
        return _total_turn_degrees(current_heading, to_fix, turn_direction)

    center_lat, center_lon = center_values

    # Find where the turn circle intersects the published inbound radial line.
    # The inbound radial is a line from the fix outward at angle (published_inbound_radial + 180°)
    # Calculate intersection of turn circle with that radial line
    intersection = _intersection_from_bearing_along_circle(
        center_lat,
        center_lon,
        radius_nm,
        fix_lat,
        fix_lon,
        outbound_radial,
    )

    if intersection is not None:
        # Found re-intercept point on the radial; calculate turn to that point
        intersection_values = _lat_lon_dict_to_tuple(intersection)
        if intersection_values is not None:
            int_lat, int_lon = intersection_values
            target_bearing = haversine_great_circle_bearing(
                lat_a,
                lon_a,
                int_lat,
                int_lon,
            )
            return _total_turn_degrees(current_heading, target_bearing, turn_direction)

    # Fallback: turn directly toward fix
    to_fix = haversine_great_circle_bearing(lat_a, lon_a, fix_lat, fix_lon)
    return _total_turn_degrees(current_heading, to_fix, turn_direction)
