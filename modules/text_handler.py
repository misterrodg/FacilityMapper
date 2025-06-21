from modules.db import filter_query
from modules.altitude import AltitudeData
from modules.draw_helper import ARC_MIN
from modules.geo_json import Feature
from modules.speed import SpeedData
from modules.text_data import TextData
from modules.text_draw import TextDraw


def _draw_line(
    text_string: str,
    offset_lat: float,
    offset_lon: float,
    scaled_line_height: float,
    text_scale: float,
    line_number: int,
) -> Feature:
    offset_lat = offset_lat - (scaled_line_height * line_number)
    text = TextDraw(text_string, offset_lat, offset_lon, text_scale)
    result = text.get_feature()
    return result


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
        row_type = row.get("type")
        if not row_lat or not row_lon or row_type == "AIRPORT":
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
            fl_1 = row.get("fl_1")
            alt_1 = row.get("alt_1")
            fl_2 = row.get("fl_2")
            alt_2 = row.get("alt_2")
            if alt_1 or fl_1 or alt_2 or fl_2:
                altitude_data = AltitudeData(alt_desc, alt_1, fl_1, alt_2, fl_2)
                altitudes = altitude_data.to_list()
                for altitude in altitudes:
                    altitude_feature = _draw_line(
                        altitude,
                        offset_lat,
                        offset_lon,
                        scaled_line_height,
                        text_scale,
                        lines_used,
                    )
                    result.append(altitude_feature)
                    lines_used += 1

        if draw_speeds:
            speed_desc = row.get("speed_desc")
            speed_limit = row.get("speed_limit")
            if speed_limit:
                speed_data = SpeedData(speed_desc, speed_limit)
                speeds = speed_data.to_list()
                for speed in speeds:
                    speed_feature = _draw_line(
                        speed,
                        offset_lat,
                        offset_lon,
                        scaled_line_height,
                        text_scale,
                        lines_used,
                    )
                    result.append(speed_feature)
                    lines_used += 1

    return result
