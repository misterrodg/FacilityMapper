from modules.AltitudeData import AltitudeData
from modules.DrawHelper import ARC_MIN
from modules.GeoJSON import Feature
from modules.QueryHelper import filter_query
from modules.SpeedData import SpeedData
from modules.TextDraw import TextDraw


def get_text_features(
    db_rows: list,
    x_offset: float,
    y_offset: float,
    text_scale: float,
    line_buffer: float,
    draw_altitudes: bool = False,
    draw_speeds: bool = False,
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
        scaled_buffer = line_buffer * ARC_MIN
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
                altitude_data = AltitudeData(
                    alt_desc,
                    altitude,
                    flight_level,
                    altitude_2,
                    flight_level_2,
                    offset_lat,
                    offset_lon,
                    scaled_buffer,
                    text_scale,
                    lines_used,
                )
                altitude_features = altitude_data.to_text_features()
                result.extend(altitude_features)
                lines_used += len(altitude_features)

        if draw_speeds:
            speed_desc = row.get("speed_limit_2")
            speed_limit = row.get("speed_limit")
            if speed_limit:
                speed_data = SpeedData(
                    speed_desc,
                    speed_limit,
                    offset_lat,
                    offset_lon,
                    scaled_buffer,
                    text_scale,
                    lines_used,
                )
                speed_feature = speed_data.to_text_feature()
                result.append(speed_feature)
    return result
