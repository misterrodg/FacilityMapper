from modules.definitions import SymbolProperties, TextProperties
from modules.geo_json import (
    Coordinate,
    Feature,
    Point,
    Properties,
)

from modules.v_nas import (
    SYMBOL_STYLE_AIRWAY_INTERSECTION,
    SYMBOL_STYLE_DME,
    SYMBOL_STYLE_NDB,
    SYMBOL_STYLE_OTHER_WAYPOINTS,
    SYMBOL_STYLE_RNAV_ONLY,
    SYMBOL_STYLE_TACAN,
    SYMBOL_STYLE_VOR,
)


def _translate_to_ERAM_symbol(symbol_type: str) -> str:
    if symbol_type == "W":
        return SYMBOL_STYLE_RNAV_ONLY
    if symbol_type in ["C", "R"]:
        return SYMBOL_STYLE_AIRWAY_INTERSECTION
    if symbol_type == "VORDME":
        return SYMBOL_STYLE_TACAN
    if symbol_type == "VOR":
        return SYMBOL_STYLE_VOR
    if symbol_type == "DME":
        return SYMBOL_STYLE_DME
    if symbol_type == "NDB":
        return SYMBOL_STYLE_NDB
    return SYMBOL_STYLE_OTHER_WAYPOINTS


def get_symbol_feature(lat: float, lon: float, symbol_type: str) -> Feature:
    result = Feature()
    point = Point()
    coordinate = Coordinate(lat, lon)
    point.set_coordinate(coordinate)

    symbol_style = _translate_to_ERAM_symbol(symbol_type)
    properties = Properties()
    symbol_properties = SymbolProperties({"style": symbol_style})
    properties.from_dict(symbol_properties.to_dict())

    result.add_point(point)
    result.add_properties(properties)

    return result


def get_text_feature(lat: float, lon: float, lines: list[str]) -> Feature:
    result = Feature()
    point = Point()
    coordinate = Coordinate(lat, lon)
    point.set_coordinate(coordinate)

    properties = Properties()
    text_properties = TextProperties({"text": lines})
    properties.from_dict(text_properties.to_dict())

    result.add_point(point)
    result.add_properties(properties)

    return result
