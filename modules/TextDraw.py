from modules.CharPlots import (
    PLOT_HEIGHT,
    PLOT_WIDTH,
    SPACE,
    UNRECOGNIZED,
    get_plot_from_char,
)
from modules.DrawHelper import ARC_MIN, correct_offsets
from modules.GeoJSON import Coordinate, Feature, LineString, MultiLineString


class TextDraw:
    def __init__(
        self, display_text: str, lat: float, lon: float, text_scale: float = 1.0
    ):
        self.display_text = display_text
        self.lat = lat
        self.lon = lon
        self.text_scale = text_scale
        self.feature = Feature()

        self._to_point_array()

    def _to_point_array(self) -> None:
        char_array = list(self.display_text)
        char_count = 0
        multi_line_string = MultiLineString()
        for char in char_array:
            line_string = LineString()
            char_plot = get_plot_from_char(char)
            if char_plot not in [UNRECOGNIZED, SPACE]:
                lon = self.lon + (char_count * self.text_scale * ARC_MIN)
                corrected_plot = correct_offsets(
                    self.lat,
                    lon,
                    char_plot,
                    PLOT_HEIGHT,
                    PLOT_WIDTH,
                    0,
                    self.text_scale,
                )

            for line in corrected_plot:
                coordinate = Coordinate(line["lat"], line["lon"])
                line_string.add_coordinate(coordinate)
            if not line_string.is_empty():
                multi_line_string.add_line_string(line_string)
            self.feature.add_multi_line_string(multi_line_string)
            char_count += 1
        return

    def get_feature(self) -> Feature:
        return self.feature
