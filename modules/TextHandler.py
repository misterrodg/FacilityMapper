from modules.DrawHelper import ARC_MIN
from modules.GeoJSON import Feature
from modules.QueryHelper import filter_query
from modules.TextDraw import TextDraw


def get_text_features(
    db_rows: list,
    x_offset: float,
    y_offset: float,
    text_scale: float,
    line_buffer: float,
    draw_altitudes: bool,
    draw_speeds: bool,
) -> list[Feature]:
    filtered_rows = filter_query(db_rows, "fix_id")
    result = []
    for row in filtered_rows:
        row_lat = row.get("lat")
        row_lon = row.get("lon")
        if not row_lat or not row_lon:
            continue
        offset_lat = y_offset + row_lat
        offset_lon = x_offset + row_lon
        text_draw = TextDraw(row["fix_id"], offset_lat, offset_lon, text_scale)
        result.append(text_draw.get_feature())
        lines_used = 1

        if draw_altitudes:
            alt_desc = row.get("alt_desc")
            altitude = row.get("altitude")
            altitude_2 = row.get("altitude_2")
            flight_level = row.get("flight_level")
            flight_level_2 = row.get("flight_level_2")
            if altitude or flight_level or altitude_2 or flight_level_2:
                if altitude or flight_level:
                    offset_lat = (
                        y_offset + row_lat - (line_buffer * lines_used * ARC_MIN)
                    )
                    offset_lon = x_offset + row_lon
                    altitude_value = altitude if altitude else f"FL{flight_level}"
                    altitude_value = (
                        f"{alt_desc}{altitude_value}"
                        if alt_desc in ["+", "-"]
                        else altitude_value
                    )
                    text_draw = TextDraw(
                        str(altitude_value), offset_lat, offset_lon, text_scale
                    )
                    result.append(text_draw.get_feature())
                    lines_used += 1
                if altitude_2 or flight_level_2:
                    offset_lat = (
                        y_offset + row_lat - (line_buffer * lines_used * ARC_MIN)
                    )
                    offset_lon = x_offset + row_lon
                    altitude_value_2 = (
                        altitude_2 if altitude_2 else f"FL{flight_level_2}"
                    )
                    text_draw = TextDraw(
                        str(altitude_value_2), offset_lat, offset_lon, text_scale
                    )
                    if altitude_value != altitude_value_2:
                        result.append(text_draw.get_feature())
                        lines_used += 1

        if draw_speeds:
            speed_limit = row.get("speed_limit")
            if speed_limit:
                offset_lat = y_offset + row_lat - (line_buffer * lines_used * ARC_MIN)
                offset_lon = x_offset + row_lon
                text_draw = TextDraw(
                    str(speed_limit),
                    offset_lat,
                    offset_lon,
                    text_scale,
                )
                result.append(text_draw.get_feature())
    return result
