from modules.DrawHelper import correctOffsets
from modules.GeoJSON import Coordinate, Feature, LineString, MultiLineString
from modules.SymbolPlots import PLOT_HEIGHT, PLOT_WIDTH, UNRECOGNIZED, getPlotFromString


class SymbolDraw:
    def __init__(
        self,
        symbolType: str,
        lat: float,
        lon: float,
        rotationDeg: float = 0.0,
        symbolScale: float = 1.0,
    ):
        self.symbolType = symbolType
        self.lat = lat
        self.lon = lon
        self.rotationDeg = rotationDeg
        self.symbolScale = symbolScale
        self.feature = Feature()

        self._toPointArray()

    def _toPointArray(self) -> None:
        multiLineString = MultiLineString()
        lineString = LineString()
        symbolPlot = getPlotFromString(self.symbolType)
        if symbolPlot != UNRECOGNIZED:
            correctedPlot = correctOffsets(
                self.lat,
                self.lon,
                symbolPlot,
                PLOT_HEIGHT,
                PLOT_WIDTH,
                self.rotationDeg,
                self.symbolScale,
            )

            for line in correctedPlot:
                coordinate = Coordinate(line["lat"], line["lon"])
                lineString.addCoordinate(coordinate)
            if not lineString.isEmpty():
                multiLineString.addLineString(lineString)
            self.feature.addMultiLineString(multiLineString)

    def getFeature(self) -> Feature:
        return self.feature
