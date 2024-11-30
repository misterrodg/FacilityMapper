from modules.DirPaths import VIDMAP_DIR
from modules.vNAS import (
    ASDEX_STYLES,
    BCG_MIN,
    BCG_MAX,
    FILTER_MIN,
    FILTER_MAX,
    LINE_STYLES,
    LINE_THICKNESS_MIN,
    LINE_THICKNESS_MAX,
    SYMBOL_STYLES,
    SYMBOL_SIZE_MIN,
    SYMBOL_SIZE_MAX,
    TEXT_SIZE_MIN,
    TEXT_SIZE_MAX,
)

import json
import re


class Coordinate:
    def __init__(self, lat: float, lon: float):
        self.lat = None
        self.lon = None

        if self._valid_coordinates(lat, lon):
            self.lat = lat
            self.lon = lon

    def to_geo_json(self) -> list:
        return [self.lon, self.lat]

    def _valid_coordinates(self, lat, lon) -> bool:
        valid_lat = lat <= 90 and lat >= -90
        valid_lon = lon <= 180 and lon >= -180
        return valid_lat and valid_lon


class Properties:
    def __init__(self):
        self.asdex = None
        self.bcg = None
        self.color = None
        self.filters = None
        self.is_line_defaults = None
        self.is_symbol_defaults = None
        self.is_text_defaults = None
        self.opaque = None
        self.size = None
        self.style = None
        self.thickness = None
        self.underline = None
        self.x_offset = None
        self.y_offset = None

    def set_asdex(self, asdex_style: str) -> None:
        if asdex_style in ASDEX_STYLES:
            self.asdex = asdex_style
        return

    def set_bcg(self, bcg: int) -> None:
        if bcg >= BCG_MIN and bcg <= BCG_MAX:
            self.bcg = bcg
        return

    def set_color(self, hex_string: str) -> None:
        if self._is_hex_color(hex_string):
            self.color = hex_string
        return

    def set_filters(self, filter_list: list) -> None:
        filters = []
        for item in filter_list:
            if item >= FILTER_MIN and item <= FILTER_MAX:
                filters.append(item)
        if len(filters) > 0:
            self.filters = filters
        return

    def set_is_line_defaults(self, line_defaults: bool) -> None:
        self.is_line_defaults = line_defaults
        return

    def set_is_symbol_defaults(self, symbol_defaults: bool) -> None:
        self.is_symbol_defaults = symbol_defaults
        return

    def set_is_text_defaults(self, text_defaults: bool) -> None:
        self.is_text_defaults = text_defaults
        return

    def set_line_style(self, line_style: str) -> None:
        if line_style in LINE_STYLES:
            self.style = line_style
        return

    def set_line_thickness(self, line_thickness: int) -> None:
        if (
            line_thickness >= LINE_THICKNESS_MIN
            and line_thickness <= LINE_THICKNESS_MAX
        ):
            self.thickness = line_thickness
        return

    def set_symbol_style(self, symbol_style: str) -> None:
        if symbol_style in SYMBOL_STYLES:
            self.style = symbol_style
        return

    def set_symbol_size(self, symbol_size: int) -> None:
        if symbol_size >= SYMBOL_SIZE_MIN and symbol_size <= SYMBOL_SIZE_MAX:
            self.size = symbol_size
        return

    def set_text_size(self, text_size: int) -> None:
        if text_size >= TEXT_SIZE_MIN and text_size <= TEXT_SIZE_MAX:
            self.size = text_size
        return

    def set_text_opaque(self, text_opaque: bool) -> None:
        self.opaque = text_opaque
        return

    def set_text_underline(self, text_underline: bool) -> None:
        self.underline = text_underline
        return

    def set_text_offset(self, dimension: str, offset: int) -> None:
        is_positive = offset > 0
        if dimension == "x" and is_positive:
            self.x_offset = offset
        if dimension == "y" and is_positive:
            self.y_offset = offset
        return

    def to_dict(self) -> dict:
        result = {
            "asdex": self.asdex,
            "bcg": self.bcg,
            "color": self.color,
            "filters": self.filters,
            "isLineDefaults": self.is_line_defaults,
            "isSymbolDefaults": self.is_symbol_defaults,
            "isTextDefaults": self.is_text_defaults,
            "opaque": self.opaque,
            "size": self.size,
            "style": self.style,
            "thickness": self.thickness,
            "underline": self.underline,
            "xOffset": self.x_offset,
            "yOffset": self.y_offset,
        }
        result = {key: value for key, value in result.items() if value is not None}
        return result

    def _is_hex_color(hex_string: str) -> bool:
        pattern = r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$"
        return bool(re.match(pattern, hex_string))


class LineString:
    def __init__(self):
        self.type = "LineString"
        self.coordinates = []

    def add_coordinate(self, coordinate: Coordinate) -> None:
        self.coordinates.append(coordinate.to_geo_json())
        return

    def to_coordinates(self) -> list:
        return self.coordinates

    def is_empty(self) -> bool:
        result = len(self.coordinates) == 0
        return result

    def to_dict(self) -> dict:
        return {"type": self.type, "coordinates": self.coordinates}


class MultiLineString:
    def __init__(self):
        self.type = "MultiLineString"
        self.coordinates = []

    def add_line_string(self, line_string: LineString) -> None:
        self.coordinates.append(line_string.to_coordinates())
        return

    def to_dict(self) -> dict:
        return {"type": self.type, "coordinates": self.coordinates}


class Feature:
    def __init__(self):
        self.type = "Feature"
        self.geometry = None
        self.properties = None

    def add_line_string(self, line_string: LineString) -> None:
        self.geometry = line_string.to_dict()
        return

    def add_multi_line_string(self, multi_line_string: MultiLineString) -> None:
        self.geometry = multi_line_string.to_dict()
        return

    def add_properties(self, properties: Properties) -> None:
        self.properties = properties
        return

    def to_dict(self) -> dict:
        if self.properties is None:
            self.properties = {}
        return {
            "type": self.type,
            "geometry": self.geometry,
            "properties": self.properties,
        }


class FeatureCollection:
    def __init__(self):
        self.type = "FeatureCollection"
        self.features: list[Feature] = []

    def add_feature(self, feature: Feature) -> None:
        self.features.append(feature)
        return

    def to_dict(self) -> dict:
        features = []
        for feature in self.features:
            features.append(feature.to_dict())
        return {"type": self.type, "features": features}


class GeoJSON:
    def __init__(self, file_name: str) -> None:
        self.file_path = file_name
        self.feature_collection = None

    def add_feature_collection(self, feature_collection: FeatureCollection) -> None:
        self.feature_collection = feature_collection
        return

    def to_file(self) -> None:
        data_dictionary = self.feature_collection.to_dict()
        with open(f"{VIDMAP_DIR}/{self.file_path}.geojson", "w") as json_file:
            json.dump(data_dictionary, json_file)
        return
