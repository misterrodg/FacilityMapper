from modules.GeoJSON import Feature
from modules.TextDraw import TextDraw


class TextData:
    def __init__(
        self,
        text: str,
        offset_lat: float,
        offset_lon: float,
        scaled_buffer: float,
        text_scale: float,
        start_line: int,
    ):
        self.text = text
        self.offset_lat = offset_lat
        self.offset_lon = offset_lon
        self.scaled_buffer = scaled_buffer
        self.text_scale = text_scale
        self.start_line = start_line

    def to_text_feature(self) -> Feature:
        return self._draw_line()

    def _draw_line(self) -> Feature:
        offset_lat = self.offset_lat - (self.scaled_buffer * self.start_line)
        text_string = self.text
        text = TextDraw(text_string, offset_lat, self.offset_lon, self.text_scale)
        result = text.get_feature()
        return result
