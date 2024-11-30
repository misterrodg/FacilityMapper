from modules.GeoJSON import Feature
from modules.QueryHelper import filter_query
from modules.SymbolDraw import SymbolDraw


def get_symbol_features(db_rows: list, symbol_scale: float) -> list[Feature]:
    filtered_rows = filter_query(db_rows, "fix_id")
    result = []
    for row in filtered_rows:
        if row["type"] == "W":
            symbol_draw = SymbolDraw(
                "RNAV", row["lat"], row["lon"], symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
        if row["type"] in ["C", "R"]:
            symbol_draw = SymbolDraw(
                "TRIANGLE", row["lat"], row["lon"], symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
        if row["type"] == "VORDME":
            symbol_draw = SymbolDraw(
                "DME_BOX", row["lat"], row["lon"], symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
            symbol_draw = SymbolDraw(
                "HEXAGON", row["lat"], row["lon"], symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
        if row["type"] == "VOR":
            symbol_draw = SymbolDraw(
                "HEXAGON", row["lat"], row["lon"], symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
        if row["type"] == "DME":
            symbol_draw = SymbolDraw(
                "DME_BOX", row["lat"], row["lon"], symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
        if row["type"] == "NDB":
            symbol_draw = SymbolDraw(
                "CIRCLE_L", row["lat"], row["lon"], symbol_scale=symbol_scale
            )
            result.append(symbol_draw.get_feature())
    return result
