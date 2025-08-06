from modules.definitions import SymbolProperties, TextProperties
from modules.geo_json import (
    Coordinate,
    Feature,
    Point,
    Properties,
)

from modules.v_nas import SymbolStyle


def get_symbol_feature(
    lat: float, lon: float, symbol_style: SymbolStyle = None
) -> Feature:
    result = Feature()
    point = Point()
    coordinate = Coordinate(lat, lon)
    point.set_coordinate(coordinate)

    properties = Properties()
    if symbol_style is not None:
        symbol_properties = SymbolProperties({"style": symbol_style.value})
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
