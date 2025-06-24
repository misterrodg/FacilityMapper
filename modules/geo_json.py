from modules.dir_paths import VIDMAP_DIR
from modules.error_helper import print_top_level

from os.path import isfile, getsize

import json
import os

ERROR_HEADER = "GEOJSON: "
POINT_TYPE = "Point"
LINE_STRING_TYPE = "LineString"
MULTI_LINE_STRING_TYPE = "MultiLineString"
FEATURE_TYPE = "Feature"
FEATURE_COLLECTION_TYPE = "FeatureCollection"


class Coordinate:
    lat: float | None
    lon: float | None

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
    properties: dict | None

    def __init__(self):
        self.properties = None

    def to_dict(self) -> dict:
        result = {
            key: value for key, value in self.properties.items() if value is not None
        }
        return result

    def from_dict(self, properties_dict: dict) -> None:
        self.properties = properties_dict


class Point:
    type: str
    coordinates: Coordinate | None

    def __init__(self):
        self.type = POINT_TYPE
        self.coordinates = None

    def set_coordinate(self, coordinate: Coordinate) -> None:
        self.coordinates = coordinate
        return

    def to_dict(self) -> dict:
        coordinate = self.coordinates.to_geo_json()
        return {"type": self.type, "coordinates": coordinate}

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
    type: str
    coordinates: list[Coordinate]

    def __init__(self):
        self.type = LINE_STRING_TYPE
        self.coordinates = []

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
    type: str
    coordinates: list[LineString]

    def __init__(self):
        self.type = MULTI_LINE_STRING_TYPE
        self.coordinates = []

    def add_line_string(self, line_string: LineString) -> None:
        if not line_string.is_empty():
            self.coordinates.append(line_string)
        return

    def add_line_strings(self, line_strings: list[LineString]) -> None:
        for line in line_strings:
            if not line.is_empty():
                self.coordinates.append(line)
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
    type: str
    geometry: LineString | MultiLineString | Point | None
    properties: Properties | None

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

    def add_point(self, point: Point) -> None:
        self.geometry = point.to_dict()

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
    type: str
    features: list[Feature]

    def __init__(self):
        self.type = FEATURE_COLLECTION_TYPE
        self.features = []

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
    file_name: str
    file_path: str
    feature_collection: FeatureCollection | None

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
