from modules.DrawHelper import haversine_great_circle_bearing
from modules.GeoJSON import Feature
from modules.QueryHelper import filter_query, segment_query
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


def get_arrow_line_symbol_features(
    db_rows: list, selected_route_types: list, symbol_scale: float
) -> list[Feature]:
    start_types = selected_route_types[:2]
    end_types = selected_route_types[-2:]
    segment_list = segment_query(db_rows, "transition_id")
    result = []
    for segment_item in segment_list:
        if len(segment_item) > 1:
            for index, (from_point, to_point) in enumerate(
                zip(segment_item, segment_item[1:])
            ):
                bearing = haversine_great_circle_bearing(
                    from_point.get("lat"),
                    from_point.get("lon"),
                    to_point.get("lat"),
                    to_point.get("lon"),
                )
                arrow_head = SymbolDraw(
                    "ARROW_HEAD",
                    from_point.get("lat"),
                    from_point.get("lon"),
                    bearing,
                    symbol_scale,
                )
                result.append(arrow_head.get_feature())
                arrow_tail = SymbolDraw(
                    "ARROW_TAIL",
                    to_point.get("lat"),
                    to_point.get("lon"),
                    bearing,
                    symbol_scale,
                )
                result.append(arrow_tail.get_feature())
                if index == 0 and from_point.get("route_type") in start_types:
                    circle = SymbolDraw(
                        "CIRCLE_S",
                        from_point.get("lat"),
                        from_point.get("lon"),
                        0,
                        symbol_scale,
                    )
                    result.append(circle.get_feature())
                if (
                    index == len(segment_item) - 2
                    and to_point.get("route_type") in end_types
                ):
                    arrow_head = SymbolDraw(
                        "ARROW_HEAD_HOLLOW",
                        to_point.get("lat"),
                        to_point.get("lon"),
                        bearing,
                        symbol_scale,
                    )
                    result.append(arrow_head.get_feature())
    return result
