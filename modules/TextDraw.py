from modules.CharPlots import PLOT_HEIGHT, PLOT_WIDTH, getPlotFromChar
from modules.GeoJSON import CoordinatePair, Feature, LineString, MultiLineString

# Returns coordinate offsets to draw numbers in lat/lon coordinates

ARC_MIN = 0.015
FONT_SCALE = ARC_MIN  # 1 min of arc = 1/60, most facilities round this down to 0.015 resulting in 0.9nm tall letters


class TextDraw:
    def __init__(
        self, displayText: str, lat: float, lon: float, textScale: float = FONT_SCALE
    ):
        self.displayText = displayText
        self.lat = lat
        self.lon = lon
        self.textScale = textScale
        self.feature = None

        self._toPointArray()

    def _toPointArray(self) -> None:
        charArray = list(self.displayText)
        count = 0
        multiLineString = MultiLineString()
        for char in charArray:
            charPlot = getPlotFromChar(char)
            lineString = LineString()
            for line in charPlot:
                latAdjust = (line[0] / PLOT_HEIGHT) * self.textScale
                latAdjust += self.lat
                lonAdjust = (
                    (line[1] + (count * PLOT_WIDTH)) / PLOT_WIDTH
                ) * self.textScale
                lonAdjust += self.lon
                coordinatePair = CoordinatePair(latAdjust, lonAdjust)
                lineString.addCoordinatePair(coordinatePair)
            multiLineString.addLineString(lineString)
            count += 1
        feature = Feature()
        feature.addMultiLineString(multiLineString)

        self.feature = feature

    def getFeature(self) -> Feature:
        return self.feature
