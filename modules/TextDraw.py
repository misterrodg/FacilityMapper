from modules.CharPlots import (
    PLOT_HEIGHT,
    PLOT_WIDTH,
    SPACE,
    UNRECOGNIZED,
    getPlotFromChar,
)
from modules.DrawHelper import ARC_MIN, correctOffsets
from modules.GeoJSON import CoordinatePair, Feature, LineString, MultiLineString


class TextDraw:
    def __init__(
        self, displayText: str, lat: float, lon: float, textScale: float = 1.0
    ):
        self.displayText = displayText
        self.lat = lat
        self.lon = lon
        self.textScale = textScale
        self.feature = Feature()

        self._toPointArray()

    def _toPointArray(self) -> None:
        charArray = list(self.displayText)
        charCount = 0
        multiLineString = MultiLineString()
        for char in charArray:
            lineString = LineString()
            charPlot = getPlotFromChar(char)
            if charPlot not in [UNRECOGNIZED, SPACE]:
                lon = self.lon + (charCount * self.textScale * ARC_MIN)
                correctedPlot = correctOffsets(
                    self.lat, lon, charPlot, PLOT_HEIGHT, PLOT_WIDTH, 0, self.textScale
                )

            for line in correctedPlot:
                coordinatePair = CoordinatePair(line["lat"], line["lon"])
                lineString.addCoordinatePair(coordinatePair)
            if not lineString.isEmpty():
                multiLineString.addLineString(lineString)
            self.feature.addMultiLineString(multiLineString)

            charCount += 1

    def getFeature(self) -> Feature:
        return self.feature
