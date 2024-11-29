from modules.ErrorHelper import print_top_level
from modules.GeoJSON import FeatureCollection, GeoJSON
from modules.TextDraw import TextDraw

ERROR_HEADER = "LABEL: "


class Label:
    def __init__(self, definitionDict: dict):
        self.mapType = "LABEL"
        self.lines: list[dict] = []
        self.fileName = None
        self.isValid = False

        self._validate(definitionDict)

        if self.isValid:
            self._toFile()

    def _validate(self, definitionDict: dict) -> None:
        lines = definitionDict.get("lines")
        if lines is None:
            print(
                f"{ERROR_HEADER}Missing `lines` in:\n{print_top_level(definitionDict)}."
            )
            return

        fileName = definitionDict.get("file_name")
        if fileName is None:
            print(
                f"{ERROR_HEADER}Missing `file_name` in:\n{print_top_level(definitionDict)}."
            )
            return

        self.lines = lines
        self.fileName = fileName
        self.isValid = True

    def _toFile(self) -> None:
        featureCollection = FeatureCollection()

        for line in self.lines:
            labelLine = LabelLine(line)
            if labelLine.isValid:
                label = TextDraw(
                    labelLine.line, labelLine.lat, labelLine.lon, labelLine.textScale
                )
                feature = label.getFeature()
                featureCollection.addFeature(feature)

        geoJSON = GeoJSON(self.fileName)
        geoJSON.addFeatureCollection(featureCollection)
        geoJSON.toFile()


class LabelLine:
    def __init__(self, lineDict: dict):
        self.line = None
        self.lat = None
        self.lon = None
        self.textScale = None
        self.isValid = False

        self._validate(lineDict)

    def _validate(self, lineDict: dict) -> None:
        line = lineDict.get("line")
        if line is None:
            print(f"{ERROR_HEADER}Missing `line` in:\n{print_top_level(lineDict)}.")
            return

        lat = lineDict.get("lat")
        if lat is None:
            print(f"{ERROR_HEADER}Missing `lat` in:\n{print_top_level(lineDict)}.")
            return

        lon = lineDict.get("lon")
        if lon is None:
            print(f"{ERROR_HEADER}Missing `lon` in:\n{print_top_level(lineDict)}.")
            return

        textScale = lineDict.get("text_scale", 1.0)

        self.line = line
        self.lat = lat
        self.lon = lon
        self.textScale = textScale
        self.isValid = True

        return
