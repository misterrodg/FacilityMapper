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

OUTPUT_DIR = "./vidmaps"


class CoordinatePair:
    def __init__(self, lat: float, lon: float):
        self.lat = None
        self.lon = None

        if self._validCoordinates(lat, lon):
            self.lat = lat
            self.lon = lon

    def toGeoJSON(self) -> list:
        return [self.lon, self.lat]

    def _validCoordinates(self, lat, lon) -> bool:
        validLat = lat <= 90 and lat >= -90
        validLon = lon <= 180 and lon >= -180
        return validLat and validLon


class Properties:
    def __init__(self):
        self.asdex = None
        self.bcg = None
        self.color = None
        self.filters = None
        self.isLineDefaults = None
        self.isSymbolDefaults = None
        self.isTextDefaults = None
        self.opaque = None
        self.size = None
        self.style = None
        self.thickness = None
        self.underline = None
        self.xOffset = None
        self.yOffset = None

    def setASDEX(self, asdexStyle: str) -> None:
        if asdexStyle in ASDEX_STYLES:
            self.asdex = asdexStyle

    def setBCG(self, bcg: int) -> None:
        if bcg >= BCG_MIN and bcg <= BCG_MAX:
            self.bcg = bcg

    def setColor(self, hexString: str) -> None:
        if self._isHexColor(hexString):
            self.color = hexString

    def setFilters(self, filterList: list) -> None:
        filters = []
        for item in filterList:
            if item >= FILTER_MIN and item <= FILTER_MAX:
                filters.append(item)
        if len(filters) > 0:
            self.filters = filters

    def setIsLineDefaults(self, lineDefaults: bool) -> None:
        self.isLineDefaults = lineDefaults

    def setIsSymbolDefaults(self, symbolDefaults: bool) -> None:
        self.isSymbolDefaults = symbolDefaults

    def setIsTextDefaults(self, textDefaults: bool) -> None:
        self.isTextDefaults = textDefaults

    def setLineStyle(self, lineStyle: str) -> None:
        if lineStyle in LINE_STYLES:
            self.style = lineStyle

    def setLineThickness(self, lineThickness: int) -> None:
        if lineThickness >= LINE_THICKNESS_MIN and lineThickness <= LINE_THICKNESS_MAX:
            self.thickness = lineThickness

    def setSymbolStyle(self, symbolStyle: str) -> None:
        if symbolStyle in SYMBOL_STYLES:
            self.style = symbolStyle

    def setSymbolSize(self, symbolSize: int) -> None:
        if symbolSize >= SYMBOL_SIZE_MIN and symbolSize <= SYMBOL_SIZE_MAX:
            self.size = symbolSize

    def setTextSize(self, textSize: int) -> None:
        if textSize >= TEXT_SIZE_MIN and textSize <= TEXT_SIZE_MAX:
            self.size = textSize

    def setTextOpaque(self, textOpaque: bool) -> None:
        self.opaque = textOpaque

    def setTextUnderline(self, textUnderline: bool) -> None:
        self.underline = textUnderline

    def setTextOffset(self, dimension: str, offset: int) -> None:
        isPositive = offset > 0
        if dimension == "x" and isPositive:
            self.xOffset = offset
        if dimension == "y" and isPositive:
            self.yOffset = offset

    def toDict(self) -> dict:
        result = {
            "asdex": self.asdex,
            "bcg": self.bcg,
            "color": self.color,
            "filters": self.filters,
            "isLineDefaults": self.isLineDefaults,
            "isSymbolDefaults": self.isSymbolDefaults,
            "isTextDefaults": self.isTextDefaults,
            "opaque": self.opaque,
            "size": self.size,
            "style": self.style,
            "thickness": self.thickness,
            "underline": self.underline,
            "xOffset": self.xOffset,
            "yOffset": self.yOffset,
        }

        result = {key: value for key, value in result.items() if value is not None}
        return result

    def _isHexColor(hexString: str) -> bool:
        pattern = r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$"
        return bool(re.match(pattern, hexString))


class LineString:
    def __init__(self):
        self.type = "LineString"
        self.coordinates = []

    def addCoordinatePair(self, coordinatePair: CoordinatePair) -> None:
        self.coordinates.append(coordinatePair.toGeoJSON())

    def toCoordinates(self) -> list:
        return self.coordinates

    def toDict(self) -> dict:
        return {"type": self.type, "coordinates": self.coordinates}


class MultiLineString:
    def __init__(self):
        self.type = "MultiLineString"
        self.coordinates = []

    def addLineString(self, lineString: LineString) -> None:
        self.coordinates.append(lineString.toCoordinates())

    def toDict(self) -> dict:
        return {"type": self.type, "coordinates": self.coordinates}


class Feature:
    def __init__(self):
        self.type = "Feature"
        self.geometry = None
        self.properties = None

    def addLineString(self, lineString: LineString) -> None:
        self.geometry = lineString.toDict()

    def addMultiLineString(self, multiLineString: MultiLineString) -> None:
        self.geometry = multiLineString.toDict()

    def addProperties(self, properties: Properties) -> None:
        self.properties = properties

    def toDict(self) -> dict:
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

    def addFeature(self, feature: Feature) -> None:
        self.features.append(feature)

    def toDict(self) -> dict:
        features = []
        for feature in self.features:
            features.append(feature.toDict())

        return {"type": self.type, "features": features}


class GeoJSON:
    def __init__(self, fileName: str) -> None:
        self.filePath = fileName
        self.featureCollection = None

    def addFeatureCollection(self, featureCollection: FeatureCollection) -> None:
        self.featureCollection = featureCollection

    def toFile(self) -> None:
        dataDictionary = self.featureCollection.toDict()

        with open(f"{OUTPUT_DIR}/{self.filePath}.geojson", "w") as jsonFile:
            json.dump(dataDictionary, jsonFile)
