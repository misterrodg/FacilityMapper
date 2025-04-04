from modules.altitude import AltitudeData
from modules.db import JoinedProcedureRecord, JoinedProcedureRecords
from modules.definitions import SymbolProperties, TextProperties
from modules.geo_json import (
    Coordinate,
    Feature,
    LineString,
    MultiLineString,
    Point,
    Properties,
)
from modules.speed import SpeedData
from modules.v_nas import (
    SYMBOL_STYLE_AIRWAY_INTERSECTION,
    SYMBOL_STYLE_DME,
    SYMBOL_STYLE_NDB,
    SYMBOL_STYLE_OTHER_WAYPOINTS,
    SYMBOL_STYLE_RNAV_ONLY,
    SYMBOL_STYLE_TACAN,
    SYMBOL_STYLE_VOR,
)


def _translate_to_ERAM_symbol(type: str) -> str:
    if type == "W":
        return SYMBOL_STYLE_RNAV_ONLY
    if type in ["C", "R"]:
        return SYMBOL_STYLE_AIRWAY_INTERSECTION
    if type == "VORDME":
        return SYMBOL_STYLE_TACAN
    if type == "VOR":
        return SYMBOL_STYLE_VOR
    if type == "DME":
        return SYMBOL_STYLE_DME
    if type == "NDB":
        return SYMBOL_STYLE_NDB
    return SYMBOL_STYLE_OTHER_WAYPOINTS


def _get_symbol_feature(joined_procedure_record: JoinedProcedureRecord) -> Feature:
    result = Feature()
    point = Point()
    coordinate = Coordinate(joined_procedure_record.lat, joined_procedure_record.lon)
    point.set_coordinate(coordinate)

    symbol_style = _translate_to_ERAM_symbol(joined_procedure_record.type)
    properties = Properties()
    symbol_properties = SymbolProperties({"style": symbol_style})
    properties.from_dict(symbol_properties.to_dict())

    result.add_point(point)
    result.add_properties(properties)

    return result


def get_symbol_features(
    joined_procedure_records_list: list[JoinedProcedureRecords],
) -> list[Feature]:
    result: list[Feature] = []
    fix_ids: list[str] = []
    for segment in joined_procedure_records_list:
        for record in segment.get_records():
            if record.fix_id not in fix_ids and record.fix_id[0:2] != "RW":
                fix_ids.append(record.fix_id)
                feature = _get_symbol_feature(record)
                result.append(feature)
    return result


def _get_text_feature(
    joined_procedure_record: JoinedProcedureRecord,
    draw_names: bool = False,
    draw_altitudes: bool = False,
    draw_speeds: bool = False,
) -> Feature:
    result = Feature()
    point = Point()
    coordinate = Coordinate(joined_procedure_record.lat, joined_procedure_record.lon)
    point.set_coordinate(coordinate)

    text_list = []
    if draw_names:
        text_list.append(joined_procedure_record.fix_id)
    if draw_altitudes:
        altitude_data = AltitudeData(
            joined_procedure_record.alt_desc,
            joined_procedure_record.altitude,
            joined_procedure_record.flight_level,
            joined_procedure_record.altitude_2,
            joined_procedure_record.flight_level_2,
        )
        text_list.extend(altitude_data.to_list())
    if draw_speeds:
        speed_data = SpeedData(
            joined_procedure_record.speed_limit_2,
            joined_procedure_record.speed_limit,
        )
        text_list.extend(speed_data.to_list())

    properties = Properties()
    text_properties = TextProperties({"text": text_list})
    properties.from_dict(text_properties.to_dict())

    result.add_point(point)
    result.add_properties(properties)

    return result


def get_text_features(
    joined_procedure_records_list: list[JoinedProcedureRecords],
    draw_names: bool = False,
    draw_altitudes: bool = False,
    draw_speeds: bool = False,
) -> list[Feature]:
    result: list[Feature] = []
    fix_ids: list[str] = []
    for segment in joined_procedure_records_list:
        for record in segment.get_records():
            if record.fix_id not in fix_ids and record.fix_id[0:2] != "RW":
                fix_ids.append(record.fix_id)
                feature = _get_text_feature(
                    record, draw_names, draw_altitudes, draw_speeds
                )
                result.append(feature)
    return result


def _get_line_coordinate(joined_procedure_record: JoinedProcedureRecord) -> Coordinate:
    return Coordinate(joined_procedure_record.lat, joined_procedure_record.lon)


def _get_simple_line(joined_procedure_records: JoinedProcedureRecords) -> LineString:
    result = LineString()
    for record in joined_procedure_records.get_records():
        coordinate = _get_line_coordinate(record)
        result.add_coordinate(coordinate)
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


def get_line_feature(
    joined_procedure_records_list: list[tuple[JoinedProcedureRecords, bool]],
) -> Feature:
    result = Feature()
    multi_line_string = MultiLineString()

    for segment in joined_procedure_records_list:
        if segment[1] == True:
            line_strings = _get_unique_lines(segment[0])
            multi_line_string.add_line_strings(line_strings)
        else:
            line_string = _get_simple_line(segment[0])
            multi_line_string.add_line_string(line_string)

    result.add_multi_line_string(multi_line_string)
    return result
