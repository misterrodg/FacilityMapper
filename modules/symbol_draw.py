from modules.draw import correct_offsets
from modules.geo_json import Coordinate, Feature, LineString, MultiLineString
from modules.symbol_plots import (
    PLOT_HEIGHT,
    PLOT_WIDTH,
    UNRECOGNIZED,
    get_plot_from_string,
)


class SymbolDraw:
    symbol_type: str
    lat: float
    lon: float
    rotation_deg: float
    symbol_scale: float
    line_strings: list[LineString]

    def __init__(
        self,
        symbol_type: str,
        lat: float,
        lon: float,
        rotation_deg: float = 0.0,
        symbol_scale: float = 1.0,
    ):
        self.symbol_type = symbol_type
        self.lat = lat
        self.lon = lon
        self.rotation_deg = rotation_deg
        self.symbol_scale = symbol_scale
        self.line_strings = []

        self._to_point_array()

    def _to_point_array(self) -> None:
        line_string = LineString()
        symbol_plot = get_plot_from_string(self.symbol_type)
        if symbol_plot != UNRECOGNIZED:
            corrected_plot = correct_offsets(
                self.lat,
                self.lon,
                symbol_plot,
                PLOT_HEIGHT,
                PLOT_WIDTH,
                self.rotation_deg,
                self.symbol_scale,
            )

            for line in corrected_plot:
                coordinate = Coordinate(line["lat"], line["lon"])
                line_string.add_coordinate(coordinate)
            if not line_string.is_empty():
                self.line_strings.append(line_string)
        return

    def get_feature(self) -> Feature:
        feature = Feature()
        multi_line_string = MultiLineString()
        multi_line_string.add_line_strings(self.line_strings)
        feature.add_multi_line_string(multi_line_string)
        return feature

    def get_lines(self) -> list[LineString]:
        return self.line_strings
