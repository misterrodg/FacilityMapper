from modules.path_term.path_term_helper import (
    PathData,
    SymbolPoint,
    _altitudes_to_distance,
    _altitude_endpoint_handler,
    _arc_to_fix,
    _calculate_standard_intercept,
    _correct_course,
    _coordinate_to_tuple,
    _dme_intersection_handler,
    _intersection_from_bearings,
    _lat_lon_dict_to_tuple,
    _return_coordinate,
    _should_turn,
    _total_turn_degrees,
    _turn_arc,
    _validate_and_extract_bearing,
    _validate_and_extract_coordinate,
    _validate_bearing,
    GROUND_SPEED,
    MINUTES_PER_HOUR,
)
from modules.db import JoinedProcedureRecord
from modules.draw import (
    haversine_great_circle_distance,
    draw_vector_lines,
    haversine_great_circle_bearing,
    inverse_bearing,
    lat_lon_from_pbd,
    normalize_bearing,
)
from modules.geo_json import Coordinate

INTERCEPT_SNAP_NM = 0.05


def _get_fix_symbol(
    record: JoinedProcedureRecord,
) -> SymbolPoint | None:
    # Temporarily set an RNAV symbol at the fix location for testing purposes.
    if record.fix_id is None or record.fix_lat is None or record.fix_lon is None:
        return None
    fix_coord = Coordinate(record.fix_lat, record.fix_lon)
    return SymbolPoint("RNAV", fix_coord, 0)


def handle_af(
    joined_procedure_record: JoinedProcedureRecord,
    initial_coordinate: Coordinate,
) -> PathData:
    # Arc to Fix
    ...


def handle_ca(
    joined_procedure_record: JoinedProcedureRecord,
    initial_coordinate: Coordinate,
    initial_altitude: float | None,
) -> PathData:
    # Course to Altitude
    if initial_altitude is None:
        print("CA: initial altitude missing — skipping leg")
        return PathData(None, [], [])
    if joined_procedure_record.alt_1 is None:
        print("CA: target altitude missing — skipping leg")
        return PathData(None, [], [])
    coordinate_values = _validate_and_extract_coordinate(
        initial_coordinate, "CA: initial_coordinate"
    )
    if coordinate_values is None:
        return PathData(None, [], [])
    initial_lat, initial_lon = coordinate_values
    bearing = _correct_course(joined_procedure_record)
    bearing = _validate_and_extract_bearing(bearing, "CA: bearing")
    if bearing is None:
        return PathData(None, [], [])
    end_values = _altitude_endpoint_handler(
        initial_lat,
        initial_lon,
        bearing,
        initial_altitude,
        joined_procedure_record.alt_1,
        "CA",
    )
    if end_values is None:
        return PathData(None, [], [])
    coordinate = Coordinate(end_values[0], end_values[1])
    coordinates = [coordinate]
    symbol_points = [SymbolPoint("COMPUTED", coordinate, bearing)]
    result = PathData(bearing, coordinates, symbol_points)
    return result


def handle_cd(
    joined_procedure_record: JoinedProcedureRecord,
    last_coordinate: Coordinate,
) -> PathData:
    # Course to DME
    coordinate_values = _validate_and_extract_coordinate(
        last_coordinate, "CD: last_coordinate"
    )
    if coordinate_values is None:
        return PathData(None, [], [])
    last_lat, last_lon = coordinate_values
    bearing = _correct_course(joined_procedure_record)
    bearing = _validate_and_extract_bearing(bearing, "CD: bearing")
    if bearing is None:
        return PathData(None, [], [])
    intersection_values = _dme_intersection_handler(
        last_lat,
        last_lon,
        bearing,
        joined_procedure_record.rec_vhf_dme_lat,
        joined_procedure_record.rec_vhf_dme_lon,
        joined_procedure_record.dist_time,
        "CD",
    )
    if intersection_values is None:
        return PathData(bearing, [], [])
    coordinate = Coordinate(intersection_values[0], intersection_values[1])
    coordinates = [coordinate]
    symbol_points = [SymbolPoint("COMPUTED", coordinate, bearing)]
    result = PathData(bearing, coordinates, symbol_points)
    return result


def handle_cf(
    joined_procedure_record: JoinedProcedureRecord,
    last_coordinate: Coordinate,
    last_bearing: float | None,
) -> PathData:
    # Course to Fix
    if (
        joined_procedure_record.fix_lat is None
        or joined_procedure_record.fix_lon is None
    ):
        print("CF: fix coordinates missing — skipping leg")
        return PathData(None, [], [])
    coordinate_values = _validate_and_extract_coordinate(
        last_coordinate, "CF: last_coordinate"
    )
    if coordinate_values is None:
        return PathData(None, [], [])
    last_lat, last_lon = coordinate_values
    fix_lat = joined_procedure_record.fix_lat
    fix_lon = joined_procedure_record.fix_lon
    if last_bearing is None:
        last_bearing = haversine_great_circle_bearing(
            last_lat,
            last_lon,
            fix_lat,
            fix_lon,
        )
    coordinates = []
    corrected_course = _correct_course(joined_procedure_record)
    if not _validate_bearing(corrected_course, "corrected_course"):
        print("CF: cannot determine corrected course — skipping leg")
        return PathData(None, [], [])
    bearing_2 = inverse_bearing(corrected_course)

    # CF can require an explicit course-reversal turn before tracking inbound.
    # For near-opposite course entries, fly a procedure turn to a 45-degree
    # intercept heading for the inbound course and then re-intercept inbound.
    reversal_applied = False
    reversal_delta = abs(((last_bearing - corrected_course + 540) % 360) - 180)
    if reversal_delta >= 135.0:
        # Use nav-data direction when present (e.g., L). For a left reversal,
        # intercept inbound from 45 degrees below inbound course.
        reversal_direction = joined_procedure_record.turn_direction
        if reversal_direction == "R":
            intercept_course = normalize_bearing(corrected_course + 45.0)
        else:
            reversal_direction = "L"
            intercept_course = normalize_bearing(corrected_course - 45.0)

        turn_direction, turn_degrees = _total_turn_degrees(
            last_bearing,
            intercept_course,
            reversal_direction,
        )
        reversal_turn = _turn_arc(
            last_lat,
            last_lon,
            last_bearing,
            turn_degrees,
            turn_direction,
        )
        if reversal_turn.last_bearing is not None:
            last_bearing = reversal_turn.last_bearing
        next_coordinate = reversal_turn.get_last_coordinate()
        next_values = _coordinate_to_tuple(next_coordinate)
        if next_values is not None:
            last_lat, last_lon = next_values
        coordinates.extend(reversal_turn.coordinates)
        reversal_applied = True

    intersection = _intersection_from_bearings(
        last_lat,
        last_lon,
        last_bearing,
        fix_lat,
        fix_lon,
        bearing_2,
    )

    if intersection is None and not reversal_applied:
        inbound_course_to_fix = joined_procedure_record.course
        if inbound_course_to_fix is None:
            inbound_course_to_fix = corrected_course
        turn_direction, potential_intercept = _calculate_standard_intercept(
            last_lat,
            last_lon,
            fix_lat,
            fix_lon,
            inbound_course_to_fix,
        )
        turn_direction, turn_degrees = _total_turn_degrees(
            last_bearing, potential_intercept, turn_direction
        )
        additional_turn = _turn_arc(
            last_lat,
            last_lon,
            last_bearing,
            turn_degrees,
            turn_direction,
        )
        if additional_turn.last_bearing is not None:
            last_bearing = additional_turn.last_bearing
        next_coordinate = additional_turn.get_last_coordinate()
        next_values = _coordinate_to_tuple(next_coordinate)
        if next_values is not None:
            last_lat, last_lon = next_values
        coordinates.extend(additional_turn.coordinates)

    intersection = _intersection_from_bearings(
        last_lat,
        last_lon,
        last_bearing,
        fix_lat,
        fix_lon,
        bearing_2,
    )

    if intersection is None:
        final_coordinate = Coordinate(fix_lat, fix_lon)
        coordinates.append(final_coordinate)
        fallback_bearing = haversine_great_circle_bearing(
            last_lat,
            last_lon,
            fix_lat,
            fix_lon,
        )
        if not _validate_bearing(fallback_bearing, "fallback_bearing"):
            fallback_bearing = corrected_course
        return PathData(fallback_bearing, coordinates, [])
    intersection_values = _lat_lon_dict_to_tuple(intersection)
    if intersection_values is None:
        print("CF: invalid intersection point — drawing directly to fix")
        final_coordinate = Coordinate(fix_lat, fix_lon)
        coordinates.append(final_coordinate)
        return PathData(corrected_course, coordinates, [])
    intersection_lat, intersection_lon = intersection_values
    snap_distance = haversine_great_circle_distance(
        last_lat,
        last_lon,
        intersection_lat,
        intersection_lon,
    )
    snap_to_current = snap_distance <= INTERCEPT_SNAP_NM
    if snap_to_current:
        intersection_coordinate = Coordinate(last_lat, last_lon)
    else:
        intersection_coordinate = Coordinate(intersection_lat, intersection_lon)
        coordinates.append(intersection_coordinate)
    symbol_points = []
    if not snap_to_current:
        symbol_points.append(
            SymbolPoint("COMPUTED", intersection_coordinate, last_bearing),
        )
    final_coordinate = Coordinate(fix_lat, fix_lon)
    intersection_lat = intersection_coordinate.lat
    intersection_lon = intersection_coordinate.lon
    if intersection_lat is None or intersection_lon is None:
        return PathData(corrected_course, coordinates, symbol_points)
    coordinates.append(final_coordinate)
    final_leg_bearing = haversine_great_circle_bearing(
        intersection_lat,
        intersection_lon,
        fix_lat,
        fix_lon,
    )
    if not _validate_bearing(final_leg_bearing, "final_leg_bearing"):
        final_leg_bearing = corrected_course
    # Add symbol marker for named fixes
    fix_symbol = _get_fix_symbol(joined_procedure_record)
    if fix_symbol is not None:
        symbol_points.append(fix_symbol)
    result = PathData(final_leg_bearing, coordinates, symbol_points)
    return result


def handle_ci(
    joined_procedure_record: JoinedProcedureRecord,
    last_bearing: float | None,
    last_coordinate: Coordinate,
) -> PathData:
    # Course to Intercept
    if not _validate_bearing(last_bearing, "last_bearing"):
        print("CI: invalid last bearing — skipping leg")
        return PathData(None, [], [])
    coordinate_values = _validate_and_extract_coordinate(
        last_coordinate, "CI: last_coordinate"
    )
    if coordinate_values is None:
        return PathData(None, [], [])
    last_lat, last_lon = coordinate_values
    stop_bearing = _correct_course(joined_procedure_record)
    stop_bearing = _validate_and_extract_bearing(stop_bearing, "CI: stop_bearing")
    if stop_bearing is None:
        return PathData(None, [], [])
    should_plot_turn = _should_turn(
        last_bearing,
        stop_bearing,
    )

    if not should_plot_turn:
        result = PathData(stop_bearing, [last_coordinate])
        return result

    start_bearing = last_bearing
    turn_direction, turn_degrees = _total_turn_degrees(
        start_bearing,
        stop_bearing,
        joined_procedure_record.turn_direction,
    )
    result = _turn_arc(
        last_lat,
        last_lon,
        start_bearing,
        turn_degrees,
        turn_direction,
    )
    return result


def handle_cr() -> PathData:
    # Course to Radial
    ...


def handle_df(
    joined_procedure_record: JoinedProcedureRecord,
    last_bearing: float | None,
    last_coordinate: Coordinate,
) -> PathData:
    # Direct to Fix
    if (
        joined_procedure_record.fix_lat is None
        or joined_procedure_record.fix_lon is None
    ):
        print("DF: fix coordinates missing — skipping leg")
        return PathData(None, [], [])
    coordinate_values = _validate_and_extract_coordinate(
        last_coordinate, "DF: last_coordinate"
    )
    if coordinate_values is None:
        return PathData(None, [], [])
    last_lat, last_lon = coordinate_values
    next_coordinate = Coordinate(
        joined_procedure_record.fix_lat, joined_procedure_record.fix_lon
    )
    next_bearing = haversine_great_circle_bearing(
        last_lat,
        last_lon,
        joined_procedure_record.fix_lat,
        joined_procedure_record.fix_lon,
    )
    if not _validate_bearing(last_bearing, "last_bearing"):
        # If no prior track exists, seed with direct-to-fix course so the leg still renders.
        last_bearing = next_bearing
    if not _validate_bearing(next_bearing, "next_bearing"):
        print("DF: cannot determine direct-to-fix bearing — skipping leg")
        return PathData(None, [], [])
    use_tf = _should_turn(
        last_bearing,
        next_bearing,
    )
    if not use_tf:
        result = PathData(next_bearing, [next_coordinate])
        return result

    result = _arc_to_fix(
        last_lat,
        last_lon,
        last_bearing,
        joined_procedure_record.fix_lat,
        joined_procedure_record.fix_lon,
        joined_procedure_record.turn_direction,
    )
    if len(result.coordinates) == 0:
        return PathData(next_bearing, [next_coordinate])

    last_arc_coordinate = result.get_last_coordinate()
    last_arc_values = _coordinate_to_tuple(last_arc_coordinate)
    if last_arc_values is None:
        result.coordinates.append(next_coordinate)
        result.last_bearing = next_bearing
        return result

    remaining_distance = haversine_great_circle_distance(
        last_arc_values[0],
        last_arc_values[1],
        joined_procedure_record.fix_lat,
        joined_procedure_record.fix_lon,
    )
    if remaining_distance > INTERCEPT_SNAP_NM:
        result.coordinates.append(next_coordinate)
        result.last_bearing = haversine_great_circle_bearing(
            last_arc_values[0],
            last_arc_values[1],
            joined_procedure_record.fix_lat,
            joined_procedure_record.fix_lon,
        )
    else:
        result.last_bearing = next_bearing
    return result


def handle_fa(
    joined_procedure_record: JoinedProcedureRecord,
    last_coordinate: Coordinate,
    last_bearing: float | None,
    last_altitude: float | None,
) -> PathData:
    # Fix to Altitude
    if not _validate_bearing(last_bearing, "last_bearing"):
        print("FA: invalid last bearing — skipping leg")
        return PathData(None, [], [])
    if (
        joined_procedure_record.fix_lat is None
        or joined_procedure_record.fix_lon is None
    ):
        print("FA: fix coordinates missing — skipping leg")
        return PathData(None, [], [])
    if last_altitude is None:
        print("FA: last altitude missing — skipping leg")
        return PathData(None, [], [])
    if joined_procedure_record.alt_1 is None:
        print("FA: target altitude missing — skipping leg")
        return PathData(None, [], [])
    coordinate_values = _validate_and_extract_coordinate(
        last_coordinate, "FA: last_coordinate"
    )
    if coordinate_values is None:
        return PathData(None, [], [])
    last_lat, last_lon = coordinate_values
    fix_lat = joined_procedure_record.fix_lat
    fix_lon = joined_procedure_record.fix_lon
    coordinates = []
    bearing_2 = _correct_course(joined_procedure_record)
    if bearing_2 is None:
        print("FA: cannot determine corrected course — skipping leg")
        return PathData(None, [], [])

    intersection = _intersection_from_bearings(
        last_lat,
        last_lon,
        last_bearing,
        fix_lat,
        fix_lon,
        bearing_2,
    )
    print(f"{fix_lat},{fix_lon},{bearing_2}")

    if intersection is None:
        print("Adding turn")
        inbound_course_to_fix = joined_procedure_record.course
        if inbound_course_to_fix is None:
            inbound_course_to_fix = bearing_2
        turn_direction, potential_intercept = _calculate_standard_intercept(
            last_lat,
            last_lon,
            fix_lat,
            fix_lon,
            inbound_course_to_fix,
        )
        turn_direction, turn_degrees = _total_turn_degrees(
            last_bearing, potential_intercept, turn_direction
        )
        additional_turn = _turn_arc(
            last_lat,
            last_lon,
            last_bearing,
            turn_degrees,
            turn_direction,
        )
        if additional_turn.last_bearing is not None:
            last_bearing = additional_turn.last_bearing
        next_coordinate = additional_turn.get_last_coordinate()
        next_values = _coordinate_to_tuple(next_coordinate)
        if next_values is not None:
            last_lat, last_lon = next_values
        print(f"LF: {last_lat},{last_lon},{last_bearing} at end of turn")
        coordinates.extend(additional_turn.coordinates)

    intersection = _intersection_from_bearings(
        last_lat,
        last_lon,
        last_bearing,
        fix_lat,
        fix_lon,
        bearing_2,
    )
    print(
        f"LF: {last_lat},{last_lon},{last_bearing} passed to intersection_from_bearings (to {bearing_2})"
    )

    if intersection is None:
        print(
            "FA: could not resolve intersection after fallback — using fix coordinate directly"
        )
        intersection_lat = fix_lat
        intersection_lon = fix_lon
    else:
        intersection_values = _lat_lon_dict_to_tuple(intersection)
        if intersection_values is None:
            print("FA: invalid intersection point — using fix coordinate directly")
            intersection_lat = fix_lat
            intersection_lon = fix_lon
        else:
            intersection_lat, intersection_lon = intersection_values
    snap_distance = haversine_great_circle_distance(
        last_lat,
        last_lon,
        intersection_lat,
        intersection_lon,
    )
    intercept_coordinate = Coordinate(intersection_lat, intersection_lon)
    if snap_distance > INTERCEPT_SNAP_NM:
        coordinates.append(intercept_coordinate)
    else:
        intersection_lat = last_lat
        intersection_lon = last_lon
        intercept_coordinate = Coordinate(intersection_lat, intersection_lon)

    altitude_distance = _altitudes_to_distance(
        last_altitude, joined_procedure_record.alt_1
    )
    end_of_climb = lat_lon_from_pbd(
        intersection_lat,
        intersection_lon,
        bearing_2,
        altitude_distance,
    )
    end_values = _lat_lon_dict_to_tuple(end_of_climb)
    if end_values is None:
        print("FA: unable to compute climb endpoint — skipping leg")
        return PathData(None, coordinates, [])
    coordinate = Coordinate(end_values[0], end_values[1])
    coordinates.append(coordinate)
    symbol_points = [
        SymbolPoint("CIRCLE_S", intercept_coordinate, 0),
        SymbolPoint("COMPUTED", coordinate, bearing_2),
    ]
    # Add symbol marker for named fixes
    fix_symbol = _get_fix_symbol(joined_procedure_record)
    if fix_symbol is not None:
        symbol_points.append(fix_symbol)
    result = PathData(bearing_2, coordinates, symbol_points)
    return result


def handle_fc(joined_procedure_record: JoinedProcedureRecord) -> PathData:
    # Course for a Distance
    if (
        joined_procedure_record.fix_lat is None
        or joined_procedure_record.fix_lon is None
    ):
        print("FC: fix coordinates missing — skipping leg")
        return PathData(None, [], [])
    if joined_procedure_record.dist_time is None:
        print("FC: distance/time missing — skipping leg")
        return PathData(None, [], [])
    bearing = _correct_course(joined_procedure_record)
    bearing = _validate_and_extract_bearing(bearing, "FC: bearing")
    if bearing is None:
        return PathData(None, [], [])
    end_of_course = lat_lon_from_pbd(
        joined_procedure_record.fix_lat,
        joined_procedure_record.fix_lon,
        bearing,
        joined_procedure_record.dist_time,
    )
    end_values = _lat_lon_dict_to_tuple(end_of_course)
    if end_values is None:
        print("FC: unable to compute endpoint — skipping leg")
        return PathData(None, [], [])
    coordinate = Coordinate(end_values[0], end_values[1])
    coordinates = [coordinate]
    symbol_points = [SymbolPoint("COMPUTED", coordinate, bearing)]
    result = PathData(bearing, coordinates, symbol_points)
    return result


def handle_fd(
    joined_procedure_record: JoinedProcedureRecord,
    last_coordinate: Coordinate,
) -> PathData:
    # Fix to DME
    coordinate_values = _validate_and_extract_coordinate(
        last_coordinate, "FD: last_coordinate"
    )
    if coordinate_values is None:
        return PathData(None, [], [])
    last_lat, last_lon = coordinate_values
    bearing = _correct_course(joined_procedure_record)
    bearing = _validate_and_extract_bearing(bearing, "FD: bearing")
    if bearing is None:
        return PathData(None, [], [])
    intersection_values = _dme_intersection_handler(
        last_lat,
        last_lon,
        bearing,
        joined_procedure_record.rec_vhf_dme_lat,
        joined_procedure_record.rec_vhf_dme_lon,
        joined_procedure_record.dist_time,
        "FD",
    )
    if intersection_values is None:
        return PathData(bearing, [], [])
    coordinate = Coordinate(intersection_values[0], intersection_values[1])
    coordinates = [coordinate]
    symbol_points = [SymbolPoint("COMPUTED", coordinate, bearing)]
    result = PathData(bearing, coordinates, symbol_points)
    return result


def handle_fm(
    joined_procedure_record: JoinedProcedureRecord,
    vector_length: float,
    buffer_length: float = 0.0,
) -> PathData:
    # Fix to Manual Termination
    if (
        joined_procedure_record.fix_lat is None
        or joined_procedure_record.fix_lon is None
    ):
        print("FM: fix coordinates missing — skipping leg")
        return PathData(None, [], [])
    bearing = _correct_course(joined_procedure_record)
    bearing = _validate_and_extract_bearing(bearing, "FM: bearing")
    if bearing is None:
        return PathData(None, [], [])
    line_string = draw_vector_lines(
        joined_procedure_record.fix_lat,
        joined_procedure_record.fix_lon,
        bearing,
        vector_length,
        buffer_length,
    )
    result = PathData(bearing, line_string.coordinates)
    return result


def handle_ha() -> PathData:
    # Hold to Altitude Termination
    ...


def handle_hf() -> PathData:
    # Hold to Fix Termination (Single Circuit Hold)
    ...


def handle_hm(joined_procedure_record: JoinedProcedureRecord) -> PathData:
    # Hold to Manual Termination
    if (
        joined_procedure_record.fix_lat is None
        or joined_procedure_record.fix_lon is None
    ):
        print("HM: fix coordinates missing — skipping leg")
        return PathData(None, [], [])
    hold_turn_degrees = 180.0
    bearing = _correct_course(joined_procedure_record)
    bearing = _validate_and_extract_bearing(bearing, "HM: bearing")
    if bearing is None:
        return PathData(None, [], [])
    if joined_procedure_record.turn_direction is None:
        print("HM: turn direction missing — skipping leg")
        return PathData(None, [], [])
    if joined_procedure_record.dist_time is None:
        print("HM: hold distance/time missing — skipping leg")
        return PathData(None, [], [])
    outbound_arc_data = _turn_arc(
        joined_procedure_record.fix_lat,
        joined_procedure_record.fix_lon,
        bearing,
        hold_turn_degrees,
        joined_procedure_record.turn_direction,
    )
    final_outbound_coordinate = outbound_arc_data.get_last_coordinate()
    final_outbound_values = _coordinate_to_tuple(final_outbound_coordinate)
    if final_outbound_values is None:
        print("HM: unable to compute outbound arc endpoint — skipping leg")
        return PathData(None, [], [])
    outbound_lat, outbound_lon = final_outbound_values
    distance = joined_procedure_record.dist_time
    if joined_procedure_record.time == 1:
        distance = joined_procedure_record.dist_time * (GROUND_SPEED / MINUTES_PER_HOUR)
    outbound_course = inverse_bearing(bearing)
    outbound_point = lat_lon_from_pbd(
        outbound_lat,
        outbound_lon,
        outbound_course,
        distance,
    )
    outbound_values = _lat_lon_dict_to_tuple(outbound_point)
    if outbound_values is None:
        print("HM: unable to compute outbound point — skipping leg")
        return PathData(None, [], [])
    outbound_coordinate = Coordinate(outbound_values[0], outbound_values[1])
    inbound_arc_data = _turn_arc(
        outbound_values[0],
        outbound_values[1],
        outbound_course,
        180.0,
        joined_procedure_record.turn_direction,
    )
    inbound_coordinate = Coordinate(
        joined_procedure_record.fix_lat, joined_procedure_record.fix_lon
    )

    coordinates = []
    coordinates.extend(outbound_arc_data.coordinates)
    coordinates.append(outbound_coordinate)
    coordinates.extend(inbound_arc_data.coordinates)
    coordinates.append(inbound_coordinate)
    symbol_points = [SymbolPoint("CHEVRON", outbound_coordinate, outbound_course)]

    result = PathData(bearing, coordinates, symbol_points)
    return result


def handle_if(joined_procedure_record: JoinedProcedureRecord) -> PathData:
    # Initial Fix
    if (
        joined_procedure_record.fix_lat is None
        or joined_procedure_record.fix_lon is None
    ):
        print("IF: fix coordinates missing — skipping leg")
        return PathData(None, [], [])
    coordinate = _return_coordinate(joined_procedure_record)
    if coordinate is None:
        print("IF: unable to build fix coordinate — skipping leg")
        return PathData(None, [], [])
    # Add symbol marker for named fixes
    symbol_points = []
    fix_symbol = _get_fix_symbol(joined_procedure_record)
    if fix_symbol is not None:
        symbol_points.append(fix_symbol)
    result = PathData(coordinates=[coordinate], symbol_points=symbol_points)
    return result


def handle_pi() -> PathData:
    # Procedure Turn to Intercept
    ...


def handle_rf() -> PathData:
    # Radius to Fix
    ...


def handle_tf(joined_procedure_record: JoinedProcedureRecord) -> PathData:
    # Track to Fix
    if (
        joined_procedure_record.fix_lat is None
        or joined_procedure_record.fix_lon is None
    ):
        print("TF: fix coordinates missing — skipping leg")
        return PathData(None, [], [])
    coordinate = _return_coordinate(joined_procedure_record)
    if coordinate is None:
        print("TF: unable to build fix coordinate — skipping leg")
        return PathData(None, [], [])
    # Add symbol marker for named fixes
    symbol_points = []
    fix_symbol = _get_fix_symbol(joined_procedure_record)
    if fix_symbol is not None:
        symbol_points.append(fix_symbol)
    result = PathData(coordinates=[coordinate], symbol_points=symbol_points)
    return result


def handle_va(
    joined_procedure_record: JoinedProcedureRecord,
    initial_coordinate: Coordinate,
    initial_altitude: float | None,
) -> PathData:
    # Vector to Altitude
    if initial_altitude is None:
        print("VA: initial altitude missing — skipping leg")
        return PathData(None, [], [])
    if joined_procedure_record.alt_1 is None:
        print("VA: target altitude missing — skipping leg")
        return PathData(None, [], [])
    coordinate_values = _validate_and_extract_coordinate(
        initial_coordinate, "VA: initial_coordinate"
    )
    if coordinate_values is None:
        return PathData(None, [], [])
    initial_lat, initial_lon = coordinate_values
    bearing = _correct_course(joined_procedure_record)
    bearing = _validate_and_extract_bearing(bearing, "VA: bearing")
    if bearing is None:
        return PathData(None, [], [])
    end_values = _altitude_endpoint_handler(
        initial_lat,
        initial_lon,
        bearing,
        initial_altitude,
        joined_procedure_record.alt_1,
        "VA",
    )
    if end_values is None:
        return PathData(None, [], [])
    coordinate = Coordinate(end_values[0], end_values[1])
    coordinates = [coordinate]
    symbol_points = [SymbolPoint("COMPUTED", coordinate, bearing)]
    result = PathData(bearing, coordinates, symbol_points)
    return result


def handle_vd(
    joined_procedure_record: JoinedProcedureRecord,
    last_coordinate: Coordinate,
) -> PathData:
    # Vector to DME
    coordinate_values = _validate_and_extract_coordinate(
        last_coordinate, "VD: last_coordinate"
    )
    if coordinate_values is None:
        return PathData(None, [], [])
    last_lat, last_lon = coordinate_values
    bearing = _correct_course(joined_procedure_record)
    bearing = _validate_and_extract_bearing(bearing, "VD: bearing")
    if bearing is None:
        return PathData(None, [], [])
    intersection_values = _dme_intersection_handler(
        last_lat,
        last_lon,
        bearing,
        joined_procedure_record.rec_vhf_dme_lat,
        joined_procedure_record.rec_vhf_dme_lon,
        joined_procedure_record.dist_time,
        "VD",
    )
    if intersection_values is None:
        return PathData(bearing, [], [])
    coordinate = Coordinate(intersection_values[0], intersection_values[1])
    coordinates = [coordinate]
    symbol_points = [SymbolPoint("COMPUTED", coordinate, bearing)]
    result = PathData(bearing, coordinates, symbol_points)
    return result


def handle_vi(
    joined_procedure_record: JoinedProcedureRecord,
    last_bearing: float | None,
    last_coordinate: Coordinate,
) -> PathData:
    # Vector to Intercept
    if not _validate_bearing(last_bearing, "last_bearing"):
        print("VI: invalid last bearing — skipping leg")
        return PathData(None, [], [])
    coordinate_values = _validate_and_extract_coordinate(
        last_coordinate, "VI: last_coordinate"
    )
    if coordinate_values is None:
        return PathData(None, [], [])
    last_lat, last_lon = coordinate_values
    start_bearing = last_bearing
    stop_bearing = _correct_course(joined_procedure_record)
    if start_bearing is None or stop_bearing is None:
        print("VI: invalid bearings — skipping leg")
        return PathData(None, [], [])
    should_plot_turn = _should_turn(
        start_bearing,
        stop_bearing,
    )

    if not should_plot_turn:
        result = PathData(stop_bearing, [last_coordinate])
        return result

    turn_direction, turn_degrees = _total_turn_degrees(
        start_bearing,
        stop_bearing,
        joined_procedure_record.turn_direction,
    )
    result = _turn_arc(
        last_lat,
        last_lon,
        start_bearing,
        turn_degrees,
        turn_direction,
    )
    # For vector-to-intercept flow, place the circle at the later computed
    # intercept point (FA/CF), not at the raw arc endpoint.
    result.symbol_points = []
    return result


def handle_vm(
    joined_procedure_record: JoinedProcedureRecord,
    last_coordinate: Coordinate,
    vector_length: float,
    buffer_length: float = 0.0,
) -> PathData:
    # Vector to Manual Termination
    coordinate_values = _validate_and_extract_coordinate(
        last_coordinate, "VM: last_coordinate"
    )
    if coordinate_values is None:
        return PathData(None, [], [])
    last_lat, last_lon = coordinate_values
    bearing = _correct_course(joined_procedure_record)
    bearing = _validate_and_extract_bearing(bearing, "VM: bearing")
    if bearing is None:
        return PathData(None, [], [])
    line_string = draw_vector_lines(
        last_lat,
        last_lon,
        bearing,
        vector_length,
        buffer_length,
    )
    result = PathData(bearing, line_string.coordinates)
    return result


def handle_vr() -> PathData:
    # Vector to Radial Termination
    ...
