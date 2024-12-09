from modules.altitude_data import AltitudeData
from modules.draw_helper import ARC_MIN
from modules.geo_json import Feature
from modules.query_helper import filter_query
from modules.speed_data import SpeedData
from modules.text_data import TextData


def get_text_features(
    db_rows: list,
    x_offset: float,
    y_offset: float,
    text_scale: float,
    line_height: float,
    draw_altitudes: bool = False,
    draw_speeds: bool = False,
) -> list[Feature]:
    filtered_rows = filter_query(db_rows, "fix_id")
    result = []
    for row in filtered_rows:
        lines_used = 0
        row_lat = row.get("lat")
        row_lon = row.get("lon")
        if not row_lat or not row_lon:
            continue
        offset_lat = y_offset + row_lat
        offset_lon = x_offset + row_lon
        scaled_line_height = line_height * ARC_MIN
        text_data = TextData(
            row["fix_id"],
            offset_lat,
            offset_lon,
            scaled_line_height,
            text_scale,
            lines_used,
        )
        text_feature = text_data.to_text_feature()
        result.append(text_feature)
        lines_used += 1

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
                    scaled_line_height,
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
                    scaled_line_height,
                    text_scale,
                    lines_used,
                )
                speed_feature = speed_data.to_text_feature()
                result.append(speed_feature)
    return result