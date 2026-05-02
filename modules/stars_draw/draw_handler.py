from collections.abc import Sequence

from modules.db import JoinedProcedureRecord
from modules.draw import ARC_MIN
from modules.geo_json import Feature
from modules.stars_draw.symbol_draw import SymbolDraw
from modules.stars_draw.symbol_plots import (
    CIRCLE_L_SYMBOL,
    DME_BOX_SYMBOL,
    FAF_SYMBOL,
    HEXAGON_SYMBOL,
    RNAV_SYMBOL,
    TRIANGLE_SYMBOL,
)
from modules.stars_draw.text_data import TextData


def draw_symbol_features(
    symbol_names: Sequence[str], lat: float, lon: float, symbol_scale: float
) -> list[Feature]:
    result = []
    for symbol_name in symbol_names:
        symbol_draw = SymbolDraw(symbol_name, lat, lon, symbol_scale=symbol_scale)
        result.append(symbol_draw.get_feature())
    return result


def resolve_symbol_type(record: JoinedProcedureRecord) -> list[str]:
    result = []

    symbol_name = record.fix_type_to_symbol_name()

    if symbol_name is None:
        return result

    if symbol_name == "FAF":
        return [FAF_SYMBOL]

    if symbol_name == "RNAV_POINT":
        return [RNAV_SYMBOL]
    if symbol_name == "WAYPOINT":
        return [TRIANGLE_SYMBOL]

    if symbol_name in ["VORDME", "VORTAC"]:
        return [DME_BOX_SYMBOL, HEXAGON_SYMBOL]
    if symbol_name == "VOR":
        return [HEXAGON_SYMBOL]
    if symbol_name == "DME":
        return [DME_BOX_SYMBOL]

    if symbol_name == "NDB":
        return [CIRCLE_L_SYMBOL]

    return result


def get_symbol_features(
    record: JoinedProcedureRecord, symbol_scale: float
) -> list[Feature]:
    if record.fix_lat is None or record.fix_lon is None:
        return []
    symbol_names = resolve_symbol_type(record)
    return draw_symbol_features(
        symbol_names, record.fix_lat, record.fix_lon, symbol_scale
    )


def get_text_features(
    lat: float,
    lon: float,
    lines: Sequence[str],
    x_offset: float,
    y_offset: float,
    text_scale: float,
    line_height: float,
) -> list[Feature]:
    result = []
    for i, line in enumerate(lines):
        offset_lat = y_offset + lat
        offset_lon = x_offset + lon
        scaled_line_height = line_height * ARC_MIN
        text_data = TextData(
            line,
            offset_lat,
            offset_lon,
            scaled_line_height,
            text_scale,
            i,
        )
        text_feature = text_data.to_text_feature()
        result.append(text_feature)
    return result
