from modules.db import JoinedProcedureRecord
from modules.draw import ARC_MIN
from modules.geo_json import Feature
from modules.symbol_draw import SymbolDraw
from modules.text_data import TextData


def get_symbol_features(
    record: JoinedProcedureRecord, symbol_scale: float
) -> list[Feature]:
    result = []

    if record.desc_code[-1] == "F":
        symbol_draw = SymbolDraw(
            "FAF", record.lat, record.lon, symbol_scale=symbol_scale
        )
        result.append(symbol_draw.get_feature())
        return result

    source = record.source
    row_type = record.type

    if source and source in ["ENR", "TRM"]:
        row_type = row_type[0:1]

        if row_type == "W":
            symbol_draw = SymbolDraw(
                "RNAV", record.lat, record.lon, symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
        if row_type in ["C", "R"]:
            symbol_draw = SymbolDraw(
                "TRIANGLE", record.lat, record.lon, symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())

    if source and source == "VHF":
        row_type = row_type[0:2]

        if row_type in ["VD", "VT"]:
            symbol_draw = SymbolDraw(
                "DME_BOX", record.lat, record.lon, symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
            symbol_draw = SymbolDraw(
                "HEXAGON", record.lat, record.lon, symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
        if row_type == "V ":
            symbol_draw = SymbolDraw(
                "HEXAGON", record.lat, record.lon, symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
        if row_type == " D":
            symbol_draw = SymbolDraw(
                "DME_BOX", record.lat, record.lon, symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())

    if source and source == "NDB":
        row_type = row_type[0:1]

        if row_type == "H":
            symbol_draw = SymbolDraw(
                "CIRCLE_L", record.lat, record.lon, symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
    return result


def get_text_features(
    lat: float,
    lon: float,
    lines: list[str],
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
