from modules.GeoJSON import Feature
from modules.TextDraw import TextDraw


class SpeedData:
    def __init__(
        self,
        speed_desc: str,
        speed: int,
        offset_lat: float,
        offset_lon: float,
        scaled_buffer: float,
        text_scale: float,
        start_line: int,
    ):
        self.speed_desc = speed_desc
        self.speed = speed
        self.offset_lat = offset_lat
        self.offset_lon = offset_lon
        self.scaled_buffer = scaled_buffer
        self.text_scale = text_scale

        self.SPEED_LINE_INDEX = start_line

    def to_text_feature(self) -> Feature:
        return self._draw_line(self.speed_desc, self.speed, self.SPEED_LINE_INDEX)

    def _draw_line(
        self, speed_desc: str, speed_value: str, line_number: int
    ) -> Feature:
        offset_lat = self.offset_lat - (self.scaled_buffer * line_number)
        speed_string = (
            f"{speed_desc}{speed_value}" if speed_desc is not None else f"{speed_value}"
        )
        text = TextDraw(speed_string, offset_lat, self.offset_lon, self.text_scale)
        result = text.get_feature()
        return result
