from modules.geo_json import Feature
from modules.text_draw import TextDraw


class SpeedData:
    def __init__(
        self,
        speed_desc: str,
        speed: int,
        offset_lat: float,
        offset_lon: float,
        scaled_line_height: float,
        text_scale: float,
        start_line: int,
    ):
        self.speed_desc: str = speed_desc
        self.speed: int = speed
        self.offset_lat: float = offset_lat
        self.offset_lon: float = offset_lon
        self.scaled_line_height: float = scaled_line_height
        self.text_scale: float = text_scale
        self.start_line: int = start_line

    def to_text_feature(self) -> Feature:
        return self._draw_line()

    def _draw_line(self) -> Feature:
        offset_lat = self.offset_lat - (self.scaled_line_height * self.start_line)
        speed_string = (
            f"{self.speed_desc}{self.speed}"
            if self.speed_desc is not None
            else f"{self.speed}"
        )
        text = TextDraw(speed_string, offset_lat, self.offset_lon, self.text_scale)
        result = text.get_feature()
        return result
