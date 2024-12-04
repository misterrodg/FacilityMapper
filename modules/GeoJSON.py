from modules.DirPaths import VIDMAP_DIR
from modules.ErrorHelper import print_top_level
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

from os.path import isfile, getsize

import json
import os
import re

ERROR_HEADER = "GEOJSON: "
POINT_TYPE = "Point"
LINE_STRING_TYPE = "LineString"
MULTI_LINE_STRING_TYPE = "MultiLineString"
FEATURE_TYPE = "Feature"
FEATURE_COLLECTION_TYPE = "FeatureCollection"


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
        self.z_index = None

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
            "zIndex": self.z_index,
        }
        result = {key: value for key, value in result.items() if value is not None}
        return result

    def from_dict(self, properties_dict: dict) -> None:
        self.asdex = properties_dict.get("asdex")
        self.bcg = properties_dict.get("bcg")
        self.color = properties_dict.get("color")
        self.filters = properties_dict.get("filters")
        self.is_line_defaults = properties_dict.get("isLineDefaults")
        self.is_symbol_defaults = properties_dict.get("isSymbolDefaults")
        self.is_text_defaults = properties_dict.get("isTextDefaults")
        self.opaque = properties_dict.get("opaque")
        self.size = properties_dict.get("size")
        self.style = properties_dict.get("style")
        self.thickness = properties_dict.get("thickness")
        self.underline = properties_dict.get("underline")
        self.x_offset = properties_dict.get("xOffset")
        self.y_offset = properties_dict.get("yOffset")
        return

    def _set_asdex(self, asdex_style: str) -> None:
        if asdex_style in ASDEX_STYLES:
            self.asdex = asdex_style
        return

    def _set_bcg(self, bcg: int) -> None:
        if bcg >= BCG_MIN and bcg <= BCG_MAX:
            self.bcg = bcg
        return

    def _set_color(self, hex_string: str) -> None:
        if self._is_hex_color(hex_string):
            self.color = hex_string
        return

    def _set_filters(self, filter_list: list) -> None:
        filters = []
        for item in filter_list:
            if item >= FILTER_MIN and item <= FILTER_MAX:
                filters.append(item)
        if len(filters) > 0:
            self.filters = filters
        return

    def _set_is_line_defaults(self, line_defaults: bool) -> None:
        self.is_line_defaults = line_defaults
        return

    def _set_is_symbol_defaults(self, symbol_defaults: bool) -> None:
        self.is_symbol_defaults = symbol_defaults
        return

    def _set_is_text_defaults(self, text_defaults: bool) -> None:
        self.is_text_defaults = text_defaults
        return

    def _set_line_style(self, line_style: str) -> None:
        if line_style in LINE_STYLES:
            self.style = line_style
        return

    def _set_line_thickness(self, line_thickness: int) -> None:
        if (
            line_thickness >= LINE_THICKNESS_MIN
            and line_thickness <= LINE_THICKNESS_MAX
        ):
            self.thickness = line_thickness
        return

    def _set_symbol_style(self, symbol_style: str) -> None:
        if symbol_style in SYMBOL_STYLES:
            self.style = symbol_style
        return

    def _set_symbol_size(self, symbol_size: int) -> None:
        if symbol_size >= SYMBOL_SIZE_MIN and symbol_size <= SYMBOL_SIZE_MAX:
            self.size = symbol_size
        return

    def _set_text_size(self, text_size: int) -> None:
        if text_size >= TEXT_SIZE_MIN and text_size <= TEXT_SIZE_MAX:
            self.size = text_size
        return

    def _set_text_opaque(self, text_opaque: bool) -> None:
        self.opaque = text_opaque
        return

    def _set_text_underline(self, text_underline: bool) -> None:
        self.underline = text_underline
        return

    def _set_text_offset(self, dimension: str, offset: int) -> None:
        is_positive = offset > 0
        if dimension == "x" and is_positive:
            self.x_offset = offset
        if dimension == "y" and is_positive:
            self.y_offset = offset
        return

    def _set_z_index(self, z_index: int) -> None:
        if z_index > 0:
            self.z_index = z_index
        return

    def _is_hex_color(hex_string: str) -> bool:
        pattern = r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$"
        return bool(re.match(pattern, hex_string))


class Point:
    def __init__(self):
        self.type = POINT_TYPE
        self.coordinates: list[Coordinate] = []

    def set_coordinate(self, coordinate: Coordinate) -> None:
        self.coordinates.append(coordinate)
        return

    def to_dict(self) -> dict:
        coordinates = []
        for coordinate in self.coordinates:
            coordinates.append(coordinate.to_geo_json())
        return {"type": self.type, "coordinates": coordinates}

    def from_dict(self, point_dict: dict) -> None:
        coordinates = point_dict.get("coordinates")
        if coordinates is None:
            print(
                f"{ERROR_HEADER}Missing `coordinates` in:\n{print_top_level(point_dict)}."
            )
            return

        self.coordinates = coordinates
        return


class LineString:
    def __init__(self):
        self.type = LINE_STRING_TYPE
        self.coordinates: list[Coordinate] = []

    def add_coordinate(self, coordinate: Coordinate) -> None:
        self.coordinates.append(coordinate)
        return

    def add_coordinates(self, coordinates: list[Coordinate]) -> None:
        self.coordinates.extend(coordinates)
        return

    def close_line(self) -> None:
        first_coordinate = self.coordinates[0]
        self.coordinates.append(first_coordinate)
        return

    def to_coordinates(self) -> list[Coordinate]:
        result = []
        for coordinate in self.coordinates:
            result.append(coordinate.to_geo_json())
        return result

    def is_empty(self) -> bool:
        result = len(self.coordinates) == 0
        return result

    def to_dict(self) -> dict:
        coordinates = []
        for coordinate in self.coordinates:
            coordinates.append(coordinate.to_geo_json())
        return {"type": self.type, "coordinates": coordinates}

    def from_dict(self, line_string_dict: dict) -> None:
        coordinates = line_string_dict.get("coordinates")
        if coordinates is None:
            print(
                f"{ERROR_HEADER}Missing `coordinates` in:\n{print_top_level(line_string_dict)}."
            )
            return

        self.coordinates = coordinates
        return


class MultiLineString:
    def __init__(self):
        self.type = MULTI_LINE_STRING_TYPE
        self.coordinates: list[LineString] = []

    def add_line_string(self, line_string: LineString) -> None:
        self.coordinates.append(line_string)
        return

    def add_line_strings(self, line_strings: list[LineString]) -> None:
        self.coordinates.extend(line_strings)
        return

    def to_dict(self) -> dict:
        coordinates = []
        for line_string in self.coordinates:
            line_coordinates = line_string.to_coordinates()
            coordinates.append(line_coordinates)
        return {"type": self.type, "coordinates": coordinates}

    def from_dict(self, multi_line_string_dict: dict) -> None:
        coordinates = multi_line_string_dict.get("coordinates")
        if coordinates is None:
            print(
                f"{ERROR_HEADER}Missing `coordinates` in:\n{print_top_level(multi_line_string_dict)}."
            )
            return

        self.coordinates = coordinates
        return


class Feature:
    def __init__(self):
        self.type = FEATURE_TYPE
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
            properties = {}
        else:
            properties = self.properties.to_dict()
        return {
            "type": self.type,
            "geometry": self.geometry,
            "properties": properties,
        }

    def from_dict(self, feature_dict: dict) -> None:
        geometry_dict = feature_dict.get("geometry")
        if geometry_dict is None:
            print(
                f"{ERROR_HEADER}Missing `geometry` in:\n{print_top_level(feature_dict)}."
            )
            return

        properties = feature_dict.get("properties")
        if properties is None:
            print(
                f"{ERROR_HEADER}Missing `properties` in:\n{print_top_level(feature_dict)}."
            )
            return

        geometry_type = geometry_dict.get("type")
        if geometry_type is None:
            print(
                f"{ERROR_HEADER}Unable to read `type` in:\n{print_top_level(geometry)}."
            )
            return

        geometry = {}
        if geometry_type == POINT_TYPE:
            geometry = Point()
            geometry.from_dict(geometry_dict)
        if geometry_type == LINE_STRING_TYPE:
            geometry = LineString()
            geometry.from_dict(geometry_dict)
        if geometry_type == MULTI_LINE_STRING_TYPE:
            geometry = MultiLineString()
            geometry.from_dict(geometry_dict)

        self.geometry = geometry
        self.properties = properties
        return


class FeatureCollection:
    def __init__(self):
        self.type = FEATURE_COLLECTION_TYPE
        self.features: list[Feature] = []

    def add_feature(self, feature: Feature) -> None:
        self.features.append(feature)
        return

    def add_features(self, feature_list: list) -> None:
        self.features.extend(feature_list)
        return

    def get_features(self) -> list[Feature]:
        return self.features

    def to_dict(self, limit_to_features: bool = False) -> dict:
        features = []
        if limit_to_features:
            features.extend(self.features)
        else:
            for feature in self.features:
                features.append(feature.to_dict())
        features = self._deduplicate(features)
        return {"type": self.type, "features": features}

    def from_dict(
        self, feature_collection_dict: dict, limit_to_features: bool = False
    ) -> None:
        feature_list = feature_collection_dict.get("features")
        if feature_list is None:
            print(
                f"{ERROR_HEADER}Missing `features` in:\n{print_top_level(feature_collection_dict)}."
            )
            return

        if limit_to_features:
            self.features = feature_list
        else:
            for item in feature_list:
                feature = Feature()
                feature.from_dict(item)
                self.features.append(feature)
        return

    def _deduplicate(self, features_list: list[dict]) -> list[dict]:
        unique_features = {
            json.dumps(feature, sort_keys=True) for feature in features_list
        }
        result = [json.loads(feature) for feature in unique_features]
        return result


class GeoJSON:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.file_path = f"{VIDMAP_DIR}/{file_name}.geojson"
        self.feature_collection = None

    def add_feature_collection(self, feature_collection: FeatureCollection) -> None:
        self.feature_collection = feature_collection
        return

    def pluck_features(self) -> list[Feature]:
        result = []
        if self.feature_collection:
            result = self.feature_collection.get_features()
        return result

    def to_file(self, limit_to_features: bool = False) -> None:
        data_dictionary = self.feature_collection.to_dict(limit_to_features)
        with open(self.file_path, "w") as json_file:
            json.dump(data_dictionary, json_file)
        return

    def from_dict(self, json_dict: dict, limit_to_features: bool = False) -> None:
        json_dict_type = json_dict.get("type")
        if json_dict_type != FEATURE_COLLECTION_TYPE:
            print(
                f"{ERROR_HEADER}Missing `feature_collection` in:\n{print_top_level(json_dict)}."
            )
            return

        feature_collection_dict = json_dict
        feature_collection = FeatureCollection()
        feature_collection.from_dict(feature_collection_dict, limit_to_features)
        self.feature_collection = feature_collection
        return

    def from_file(self, limit_to_features: bool = False) -> None:
        try:
            if isfile(self.file_path) and getsize(self.file_path) > 0:
                with open(self.file_path, "r") as json_file:
                    json_dict = json.load(json_file)
                    self.from_dict(json_dict, limit_to_features)
            else:
                print(f"{ERROR_HEADER}Cannot find map json data at {self.file_path}.")
                print(
                    f"{ERROR_HEADER}This might be caused by placing the `COMPOSITE` object above the source map object."
                )
        except json.JSONDecodeError:
            print("Failed to decode JSON from the file.")
        return

    def delete_file(self) -> None:
        if isfile(self.file_path):
            os.remove(self.file_path)
        return
