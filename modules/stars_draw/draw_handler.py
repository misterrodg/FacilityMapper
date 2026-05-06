from collections.abc import Sequence

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
from modules.stars_draw.symbol_point import SymbolPoint
from modules.stars_draw.text_data import TextData

FAF_TYPE = "FAF"
RNAV_TYPE = "RNAV_POINT"
WAYPOINT_TYPE = "WAYPOINT"
VORDME_TYPE = "VORDME"
VORTAC_TYPE = "VORTAC"
VOR_TYPE = "VOR"
DME_TYPE = "DME"
NDB_TYPE = "NDB"


def draw_symbol_features(
    symbol_names: Sequence[str], lat: float, lon: float, symbol_scale: float
) -> list[Feature]:
    result = []
    for symbol_name in symbol_names:
        symbol_draw = SymbolDraw(symbol_name, lat, lon, symbol_scale=symbol_scale)
        result.append(symbol_draw.get_feature())
    return result


def resolve_symbol_type(record: SymbolPoint, use_faf_symbol: bool = False) -> list[str]:
    result = []

    if record.symbol_name is None:
        return result

    if record.symbol_name == FAF_TYPE:
        return [FAF_SYMBOL]

    if record.symbol_name == RNAV_TYPE:
        return [RNAV_SYMBOL]
    if record.symbol_name == WAYPOINT_TYPE:
        return [TRIANGLE_SYMBOL]

    if record.symbol_name in [VORDME_TYPE, VORTAC_TYPE]:
        return [DME_BOX_SYMBOL, HEXAGON_SYMBOL]
    if record.symbol_name == VOR_TYPE:
        return [HEXAGON_SYMBOL]
    if record.symbol_name == DME_TYPE:
        return [DME_BOX_SYMBOL]

    if record.symbol_name == NDB_TYPE:
        return [CIRCLE_L_SYMBOL]

    return result


def get_symbol_features(
    record: SymbolPoint,
    symbol_scale: float,
    use_faf_symbol: bool = False,
) -> list[Feature]:
    if record.symbol_lat is None or record.symbol_lon is None:
        return []
    symbol_names = resolve_symbol_type(record, use_faf_symbol)
    return draw_symbol_features(
        symbol_names, record.symbol_lat, record.symbol_lon, symbol_scale
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
