from modules.altitude import AltitudeData
from modules.db import JoinedProcedureRecord, JoinedProcedureRecords
from modules.draw.draw_handler import draw_truncated_line
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


def get_symbol_features(
    joined_procedure_records_list: list[JoinedProcedureRecords],
    as_lines: bool = False,
    symbol_scale: float = 1.0,
) -> list[Feature]:
    result: list[Feature] = []
    fix_ids: list[str] = []
    for segment in joined_procedure_records_list:
        for record in segment.get_records():
            if record.fix_id not in fix_ids and record.fix_id[0:2] != "RW":
                fix_ids.append(record.fix_id)
                if as_lines:
                    features = stars_symbol_features(record, symbol_scale)
                    result.extend(features)
                else:
                    feature = eram_symbol_feature(record.lat, record.lon, record.type)
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
    draw_names: bool = False,
    draw_altitudes: bool = False,
    draw_speeds: bool = False,
    as_lines: bool = False,
    x_offset: float = 0.0,
    y_offset: float = 0.0,
    text_scale: float = 1.0,
    line_height: float = 1.0,
) -> list[Feature]:
    result: list[Feature] = []
    fix_ids: list[str] = []
    for segment in joined_procedure_records_list:
        for record in segment.get_records():
            if record.fix_id not in fix_ids and record.fix_id[0:2] != "RW":
                fix_ids.append(record.fix_id)
                lat = record.lat
                lon = record.lon
                lines = _generate_text(record, draw_names, draw_altitudes, draw_speeds)
                if as_lines:
                    features = stars_text_features(
                        lat, lon, lines, x_offset, y_offset, text_scale, line_height
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


def _get_truncated_lines(
    joined_procedure_records: JoinedProcedureRecords, buffer_length: float
) -> list[LineString]:
    result = []
    for segment in joined_procedure_records.get_segmented_from_to():
        for from_point, to_point in segment:
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
    buffer_length: float = 0.0,
) -> Feature:
    result = Feature()
    multi_line_string = MultiLineString()

    for segment in joined_procedure_records_list:
        if segment[1] == True:
            if buffer_length > 0.0:
                line_strings = _get_truncated_unique_lines(segment[0], buffer_length)
                multi_line_string.add_line_strings(line_strings)
            else:
                line_strings = _get_unique_lines(segment[0])
                multi_line_string.add_line_strings(line_strings)
        else:
            if buffer_length > 0.0:
                line_strings = _get_truncated_lines(segment[0], buffer_length)
                multi_line_string.add_line_strings(line_strings)
            else:
                line_string = _get_line(segment[0])
                multi_line_string.add_line_string(line_string)

    result.add_multi_line_string(multi_line_string)
    return result
