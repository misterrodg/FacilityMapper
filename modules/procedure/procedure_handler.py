from .procedure_options import LineOptions, SymbolOptions, TextOptions
from modules.altitude import AltitudeData
from modules.db import JoinedProcedureRecord, JoinedProcedureRecords
from modules.draw.draw_handler import (
    draw_dashed_line,
    draw_truncated_arc,
    draw_truncated_line,
    draw_vector_lines,
)
from modules.draw.draw_helper import haversine_great_circle_distance
from modules.eram_draw import (
    get_symbol_feature as eram_symbol_feature,
    get_text_feature as eram_text_feature,
)
from modules.stars_draw import (
    get_symbol_features as stars_symbol_features,
    get_text_features as stars_text_features,
)
from modules.geo_json import (
    Coordinate,
    Feature,
    LineString,
    MultiLineString,
)
from modules.speed import SpeedData
from modules.v_nas import (
    LINE_STYLE_LONG_DASHED,
    LINE_STYLE_LONG_SHORT_DASHED,
    LINE_STYLE_SHORT_DASHED,
    LINE_STYLE_SOLID,
    SymbolStyle,
)


def get_symbol_features(
    joined_procedure_records_list: list[JoinedProcedureRecords],
    symbol_options: SymbolOptions,
) -> list[Feature]:
    result: list[Feature] = []
    fix_ids: list[str] = []
    for segment in joined_procedure_records_list:
        for record in segment.get_records():
            if record.fix_id not in fix_ids and record.fix_id[0:2] != "RW":
                fix_ids.append(record.fix_id)
                if symbol_options and symbol_options.as_lines:
                    features = stars_symbol_features(record, symbol_options.scale)
                    result.extend(features)
                else:
                    symbol_style = SymbolStyle.from_type(record.source, record.type)
                    feature = eram_symbol_feature(record.lat, record.lon, symbol_style)
                    result.append(feature)
    return result


def _generate_text(
    joined_procedure_record: JoinedProcedureRecord,
    draw_names: bool = False,
    draw_altitudes: bool = False,
    draw_speeds: bool = False,
) -> list[str]:
    result = []
    if draw_names:
        result.append(joined_procedure_record.fix_id)
    if draw_altitudes:
        altitude_data = AltitudeData(
            joined_procedure_record.alt_desc,
            joined_procedure_record.alt_1,
            joined_procedure_record.fl_1,
            joined_procedure_record.alt_2,
            joined_procedure_record.fl_2,
        )
        result.extend(altitude_data.to_list())
    if draw_speeds:
        speed_data = SpeedData(
            joined_procedure_record.speed_desc,
            joined_procedure_record.speed_limit,
        )
        result.extend(speed_data.to_list())
    return result


def get_text_features(
    joined_procedure_records_list: list[JoinedProcedureRecords],
    text_options: TextOptions,
) -> list[Feature]:
    result: list[Feature] = []
    fix_ids: list[str] = []
    for segment in joined_procedure_records_list:
        for record in segment.get_records():
            if record.fix_id not in fix_ids and record.fix_id[0:2] != "RW":
                fix_ids.append(record.fix_id)
                lat = record.lat
                lon = record.lon
                lines = _generate_text(
                    record,
                    text_options.draw_names,
                    text_options.draw_altitudes,
                    text_options.draw_speeds,
                )
                if text_options and text_options.as_lines:
                    features = stars_text_features(
                        lat,
                        lon,
                        lines,
                        text_options.x_offset,
                        text_options.y_offset,
                        text_options.scale,
                        text_options.line_height,
                    )
                    result.extend(features)
                else:
                    feature = eram_text_feature(lat, lon, lines)
                    result.append(feature)
    return result


def _get_line_coordinate(joined_procedure_record: JoinedProcedureRecord) -> Coordinate:
    return Coordinate(joined_procedure_record.lat, joined_procedure_record.lon)


def _get_line(joined_procedure_records: JoinedProcedureRecords) -> LineString:
    result = LineString()
    for record in joined_procedure_records.get_records():
        coordinate = _get_line_coordinate(record)
        result.add_coordinate(coordinate)
    return result


def _translate_pattern(line_style: str) -> list:
    if line_style == LINE_STYLE_LONG_DASHED:
        return [1.0]
    if line_style == LINE_STYLE_LONG_SHORT_DASHED:
        return [1.0, 0.5, 0.5, 0.5]
    if line_style == LINE_STYLE_SHORT_DASHED:
        return [0.5]
    return None


def _get_dashed_lines(
    multi_line_string: MultiLineString, line_style: str
) -> MultiLineString:
    result = MultiLineString()
    pattern = _translate_pattern(line_style)
    for line_string in multi_line_string.coordinates:
        from_point = line_string.coordinates[0]
        to_point = line_string.coordinates[1]
        line_string_list = draw_dashed_line(
            from_point.lat, from_point.lon, to_point.lat, to_point.lon, pattern
        )
        for item in line_string_list:
            line = LineString()
            line.add_coordinate(item[0])
            line.add_coordinate(item[1])
            result.add_line_string(line)
    return result


def _get_vector_lines(
    joined_procedure_records: JoinedProcedureRecords,
    vector_length: float,
    buffer_length: float,
) -> list[LineString]:
    result = []
    for record in joined_procedure_records.get_records():
        if record.path_term == "FM":
            vector_line = draw_vector_lines(
                record.lat,
                record.lon,
                record.course + record.mag_var,
                vector_length,
                buffer_length,
            )
            result.append(vector_line)
    return result


def _get_truncated_lines(
    joined_procedure_records: JoinedProcedureRecords, buffer_length: float
) -> list[LineString]:
    result = []
    for segment in joined_procedure_records.get_segmented_from_to():
        for from_point, to_point in segment:
            distance = haversine_great_circle_distance(
                from_point.lat, from_point.lon, to_point.lat, to_point.lon
            )
            if distance > (2 * buffer_length):
                if to_point.path_term == "RF" and to_point.center_fix is not None:
                    line_string = draw_truncated_arc(
                        to_point.center_lat,
                        to_point.center_lon,
                        to_point.arc_radius,
                        from_point.lat,
                        from_point.lon,
                        to_point.lat,
                        to_point.lon,
                        to_point.turn_direction,
                        buffer_length,
                    )
                    result.append(line_string)
                else:
                    line_string = draw_truncated_line(
                        from_point.lat,
                        from_point.lon,
                        to_point.lat,
                        to_point.lon,
                        buffer_length,
                    )
                    result.append(line_string)
    return result


def _get_unique_lines(
    joined_procedure_records: JoinedProcedureRecords,
) -> list[LineString]:
    result = []
    for segment in joined_procedure_records.get_unique_paths():
        line_string = LineString()
        for item in segment:
            coordinate = _get_line_coordinate(item)
            line_string.add_coordinate(coordinate)
        result.append(line_string)
    return result


def _get_truncated_unique_lines(
    joined_procedure_records: JoinedProcedureRecords, buffer_length: float
) -> list[LineString]:
    result = []
    for segment in joined_procedure_records.get_unique_paths_from_to():
        for from_point, to_point in segment:
            distance = haversine_great_circle_distance(
                from_point.lat, from_point.lon, to_point.lat, to_point.lon
            )
            if distance > (2 * buffer_length):
                if to_point.path_term == "RF" and to_point.center_fix is not None:
                    line_string = draw_truncated_arc(
                        to_point.center_lat,
                        to_point.center_lon,
                        to_point.arc_radius,
                        from_point.lat,
                        from_point.lon,
                        to_point.lat,
                        to_point.lon,
                        to_point.turn_direction,
                        buffer_length,
                    )
                    result.append(line_string)
                else:
                    line_string = draw_truncated_line(
                        from_point.lat,
                        from_point.lon,
                        to_point.lat,
                        to_point.lon,
                        buffer_length,
                    )
                    result.append(line_string)
    return result


def get_line_feature(
    joined_procedure_records_list: list[tuple[JoinedProcedureRecords, bool]],
    line_options: LineOptions = None,
) -> Feature:
    result = Feature()
    multi_line_string = MultiLineString()

    for segment in joined_procedure_records_list:
        if segment[1] == True:
            if line_options and line_options.buffer_length > 0.0:
                line_strings = _get_truncated_unique_lines(
                    segment[0], line_options.buffer_length
                )
                multi_line_string.add_line_strings(line_strings)
            else:
                line_strings = _get_unique_lines(segment[0])
                multi_line_string.add_line_strings(line_strings)
        else:
            if line_options and line_options.buffer_length > 0.0:
                line_strings = _get_truncated_lines(
                    segment[0], line_options.buffer_length
                )
                multi_line_string.add_line_strings(line_strings)
            else:
                line_string = _get_line(segment[0])
                multi_line_string.add_line_string(line_string)

    if line_options and line_options.style != LINE_STYLE_SOLID:
        multi_line_string = _get_dashed_lines(multi_line_string, line_options.style)

    if line_options and line_options.vector_length != 0.0:
        last_segment = joined_procedure_records_list[-1][0]
        line_strings = _get_vector_lines(
            last_segment, line_options.vector_length, line_options.buffer_length
        )
        for line_string in line_strings:
            multi_line_string.add_line_string(line_string)

    result.add_multi_line_string(multi_line_string)
    return result
