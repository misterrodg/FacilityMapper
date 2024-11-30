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
            if (
                row["altitude"]
                or row["flight_level"]
                or row["altitude_2"]
                or row["flight_level_2"]
            ):
                alt_desc = row["alt_desc"]
                if row["altitude"] or row["flight_level"]:
                    offset_lat = (
                        y_offset + row_lat - (line_buffer * lines_used * ARC_MIN)
                    )
                    offset_lon = x_offset + row_lon
                    altitude_value = (
                        row["altitude"]
                        if row["altitude"]
                        else f"FL{row["flight_level"]}"
                    )
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
                if row["altitude_2"] or row["flight_level_2"]:
                    offset_lat = (
                        y_offset + row_lat - (line_buffer * lines_used * ARC_MIN)
                    )
                    offset_lon = x_offset + row_lon
                    altitude_value = (
                        row["altitude_2"]
                        if row["altitude_2"]
                        else f"FL{row["flight_level_2"]}"
                    )
                    text_draw = TextDraw(
                        str(altitude_value), offset_lat, offset_lon, text_scale
                    )
                    result.append(text_draw.get_feature())
                    lines_used += 1

        if draw_speeds:
            if row["speed_limit"]:
                offset_lat = y_offset + row_lat - (line_buffer * lines_used * ARC_MIN)
                offset_lon = x_offset + row_lon
                text_draw = TextDraw(
                    str(row["speed_limit"]),
                    offset_lat,
                    offset_lon,
                    text_scale,
                )
                result.append(text_draw.get_feature())
    return result
