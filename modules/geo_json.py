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


def _verify_coordinates(coordinates: object) -> bool:
    if (
        not isinstance(coordinates, list)
        or len(coordinates) != 2
        or not isinstance(coordinates[0], (int, float))
        or not isinstance(coordinates[1], (int, float))
    ):
        return False
    return True


class Coordinate:
    lat: float | None
    lon: float | None

    def __init__(self, lat: float, lon: float):
        self.lat = None
        self.lon = None

        if self._valid_coordinates(lat, lon):
            self.lat = lat
            self.lon = lon

    def to_geo_json(self) -> list[float] | None:
        if self.lat is None or self.lon is None:
            return None
        return [self.lon, self.lat]

    def _valid_coordinates(self, lat, lon) -> bool:
        valid_lat = lat <= 90 and lat >= -90
        valid_lon = lon <= 180 and lon >= -180
        return valid_lat and valid_lon


class Properties:
    properties: dict[str, object]

    def __init__(self):
        self.properties = {}

    def to_dict(self) -> dict[str, object]:
        result = {
            key: value for key, value in self.properties.items() if value is not None
        }
        return result

    def from_dict(self, properties_dict: dict[str, object]) -> None:
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

    def to_dict(self) -> dict[str, object]:
        if self.coordinates is None:
            print(f"{ERROR_HEADER}Point has no coordinate.")
            return {}
        coordinate = self.coordinates.to_geo_json()
        if coordinate is None:
            print(f"{ERROR_HEADER}Point coordinate is invalid.")
            return {}
        return {"type": self.type, "coordinates": coordinate}

    def from_dict(self, point_dict: dict[str, object]) -> None:
        coordinates = point_dict.get("coordinates")
        if coordinates is None:
            print(
                f"{ERROR_HEADER}Missing `coordinates` in:\n{print_top_level(point_dict)}."
            )
            return

        if not _verify_coordinates(coordinates):
            print(
                f"{ERROR_HEADER}Invalid `coordinates` in:\n{print_top_level(point_dict)}."
            )
            return

        assert isinstance(coordinates, list)
        self.coordinates = Coordinate(coordinates[1], coordinates[0])
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

    def to_coordinates(self) -> list[list[float]]:
        result = []
        for coordinate in self.coordinates:
            geo_json = coordinate.to_geo_json()
            if geo_json is not None:
                result.append(geo_json)
        return result

    def is_empty(self) -> bool:
        result = len(self.coordinates) == 0
        return result

    def to_dict(self) -> dict[str, object]:
        coordinates = []
        for coordinate in self.coordinates:
            geo_json = coordinate.to_geo_json()
            if geo_json is not None:
                coordinates.append(geo_json)
        return {"type": self.type, "coordinates": coordinates}

    def from_dict(self, line_string_dict: dict[str, object]) -> None:
        coordinates = line_string_dict.get("coordinates")
        if coordinates is None:
            print(
                f"{ERROR_HEADER}Missing `coordinates` in:\n{print_top_level(line_string_dict)}."
            )
            return

        if not isinstance(coordinates, list):
            print(
                f"{ERROR_HEADER}Invalid `coordinates` in:\n{print_top_level(line_string_dict)}."
            )
            return

        parsed_coordinates: list[Coordinate] = []
        for item in coordinates:
            if not _verify_coordinates(item):
                print(
                    f"{ERROR_HEADER}Invalid `coordinates` in:\n{print_top_level(line_string_dict)}."
                )
                return
            parsed_coordinates.append(Coordinate(item[1], item[0]))

        self.coordinates = parsed_coordinates
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

    def to_dict(self) -> dict[str, object]:
        coordinates = []
        for line_string in self.coordinates:
            line_coordinates = line_string.to_coordinates()
            coordinates.append(line_coordinates)
        return {"type": self.type, "coordinates": coordinates}

    def from_dict(self, multi_line_string_dict: dict[str, object]) -> None:
        coordinates = multi_line_string_dict.get("coordinates")
        if coordinates is None:
            print(
                f"{ERROR_HEADER}Missing `coordinates` in:\n{print_top_level(multi_line_string_dict)}."
            )
            return

        if not isinstance(coordinates, list):
            print(
                f"{ERROR_HEADER}Invalid `coordinates` in:\n{print_top_level(multi_line_string_dict)}."
            )
            return

        parsed_coordinates: list[LineString] = []
        for item in coordinates:
            if not isinstance(item, list):
                print(
                    f"{ERROR_HEADER}Invalid `coordinates` in:\n{print_top_level(multi_line_string_dict)}."
                )
                return
            line_string = LineString()
            line_string.from_dict({"coordinates": item})
            parsed_coordinates.append(line_string)

        self.coordinates = parsed_coordinates
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
        self.geometry = line_string
        return

    def add_multi_line_string(self, multi_line_string: MultiLineString) -> None:
        self.geometry = multi_line_string
        return

    def add_point(self, point: Point) -> None:
        self.geometry = point

    def add_properties(self, properties: Properties) -> None:
        self.properties = properties
        return

    def to_dict(self) -> dict[str, object]:
        if self.properties is None:
            properties: dict[str, object] = {}
        else:
            properties = self.properties.to_dict()
        return {
            "type": self.type,
            "geometry": self.geometry.to_dict() if self.geometry else None,
            "properties": properties,
        }

    def from_dict(self, feature_dict: dict[str, object]) -> None:
        geometry_value = feature_dict.get("geometry")
        if not isinstance(geometry_value, dict):
            print(
                f"{ERROR_HEADER}Missing or invalid `geometry` in:\n{print_top_level(feature_dict)}."
            )
            return
        geometry_dict: dict[str, object] = geometry_value

        geometry_type_value = geometry_dict.get("type")
        if not isinstance(geometry_type_value, str):
            print(
                f"{ERROR_HEADER}Missing or invalid `type` in:\n{print_top_level(geometry_dict)}."
            )
            return
        geometry_type = geometry_type_value

        properties = feature_dict.get("properties")
        if properties is None:
            print(
                f"{ERROR_HEADER}Missing `properties` in:\n{print_top_level(feature_dict)}."
            )
            return

        if not isinstance(properties, dict):
            print(
                f"{ERROR_HEADER}Invalid `properties` in:\n{print_top_level(feature_dict)}."
            )
            return

        if geometry_type == POINT_TYPE:
            point = Point()
            point.from_dict(geometry_dict)
            self.geometry = point
        elif geometry_type == LINE_STRING_TYPE:
            line_string = LineString()
            line_string.from_dict(geometry_dict)
            self.geometry = line_string
        elif geometry_type == MULTI_LINE_STRING_TYPE:
            multi_line_string = MultiLineString()
            multi_line_string.from_dict(geometry_dict)
            self.geometry = multi_line_string
        else:
            print(
                f"{ERROR_HEADER}Unknown geometry type `{geometry_type}`."
            )
            return

        parsed_properties = Properties()
        parsed_properties.from_dict(properties)
        self.properties = parsed_properties
        return


class FeatureCollection:
    type: str
    features: list[Feature]
    raw_features: list[dict[str, object]]

    def __init__(self):
        self.type = FEATURE_COLLECTION_TYPE
        self.features = []
        self.raw_features = []

    def add_feature(self, feature: Feature) -> None:
        self.features.append(feature)
        return

    def add_features(self, feature_list: list[Feature]) -> None:
        self.features.extend(feature_list)
        return

    def add_raw_features(self, feature_list: list[dict[str, object]]) -> None:
        self.raw_features.extend(feature_list)
        return

    def get_features(self) -> list[Feature]:
        return self.features

    def get_raw_features(self) -> list[dict[str, object]]:
        return self.raw_features

    def to_dict(self, limit_to_features: bool = False) -> dict[str, object]:
        if limit_to_features:
            features = self._deduplicate(self.raw_features)
        else:
            features = self._deduplicate(
                [feature.to_dict() for feature in self.features]
            )
        return {"type": self.type, "features": features}

    def from_dict(
        self, feature_collection_dict: dict[str, object], limit_to_features: bool = False
    ) -> None:
        feature_list = feature_collection_dict.get("features")
        if feature_list is None:
            print(
                f"{ERROR_HEADER}Missing `features` in:\n{print_top_level(feature_collection_dict)}."
            )
            return

        if not isinstance(feature_list, list):
            print(
                f"{ERROR_HEADER}Invalid `features` in:\n{print_top_level(feature_collection_dict)}."
            )
            return

        if limit_to_features:
            self.raw_features = feature_list
        else:
            for item in feature_list:
                feature = Feature()
                feature.from_dict(item)
                self.features.append(feature)
        return

    def _deduplicate(self, features_list: list[dict[str, object]]) -> list[dict[str, object]]:
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

    def pluck_raw_features(self) -> list[dict]:
        result = []
        if self.feature_collection:
            result = self.feature_collection.get_raw_features()
        return result

    def to_file(self, limit_to_features: bool = False) -> None:
        if self.feature_collection is None:
            print(f"{ERROR_HEADER}No feature collection to write to file.")
            return

        data_dictionary = self.feature_collection.to_dict(limit_to_features)
        with open(self.file_path, "w") as json_file:
            json.dump(data_dictionary, json_file)
        return

    def from_dict(self, json_dict: dict[str, object], limit_to_features: bool = False) -> None:
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
