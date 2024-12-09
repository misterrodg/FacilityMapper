from modules.geo_json import Feature
from modules.text_draw import TextDraw


class AltitudeData:
    def __init__(
        self,
        alt_desc: str,
        altitude: int,
        flight_level: int,
        altitude_2: int,
        flight_level_2: int,
        offset_lat: float,
        offset_lon: float,
        scaled_line_height: float,
        text_scale: float,
        start_line: int,
    ):
        self.alt_desc = alt_desc
        self.altitude = altitude
        self.flight_level = flight_level
        self.altitude_2 = altitude_2
        self.flight_level_2 = flight_level_2
        self.offset_lat = offset_lat
        self.offset_lon = offset_lon
        self.scaled_line_height = scaled_line_height
        self.text_scale = text_scale

        self.ALT_1_LINE_INDEX = start_line
        self.ALT_2_LINE_INDEX = self.ALT_1_LINE_INDEX + 1

    def to_text_features(self) -> list[Feature]:
        result = []

        value_1 = str(self.altitude) if self.altitude else f"FL{self.flight_level}"
        value_2 = (
            str(self.altitude_2) if self.altitude_2 else f"FL{self.flight_level_2}"
        )
        alt_desc = self.alt_desc

        if alt_desc == "+" or alt_desc == "-":
            # +:AOA // -:AOB
            feature = self._draw_line(alt_desc, value_1, self.ALT_1_LINE_INDEX)
            result.append(feature)
        if alt_desc == "B":
            # B:AOA value_1 and AOB value_2
            feature = self._draw_line(None, value_1, self.ALT_1_LINE_INDEX)
            result.append(feature)
            feature = self._draw_line(None, value_2, self.ALT_2_LINE_INDEX)
            result.append(feature)
        if alt_desc == "C":
            # C:AOA value_2
            feature = self._draw_line("+", value_2, self.ALT_1_LINE_INDEX)
            result.append(feature)
        if alt_desc == "G":
            # G:AT in value_1 / GS in value_2
            feature = self._draw_line(None, value_1, self.ALT_1_LINE_INDEX)
            result.append(feature)
        if alt_desc == "H":
            # H:AOA in value_1 / GS in value_2
            feature = self._draw_line("+", value_1, self.ALT_1_LINE_INDEX)
            result.append(feature)
        if alt_desc == "I":
            # I:AT in value_1 / GS Int in value_2
            feature = self._draw_line(None, value_1, self.ALT_1_LINE_INDEX)
            result.append(feature)
        if alt_desc == "J":
            # J:AOA in value_1 / GS Int in value_2
            feature = self._draw_line("+", value_1, self.ALT_1_LINE_INDEX)
            result.append(feature)
        if alt_desc == "V":
            # V:AT Step Down in value_1 / AT in value_2
            # Says "AT" but charts display as AOA as a catchall, with value_2 used by aircraft systems
            feature = self._draw_line("+", value_1, self.ALT_1_LINE_INDEX)
            result.append(feature)
        if alt_desc == "Y":
            # Y:AOB Step Down in value_1 / AT in value_2
            feature = self._draw_line("-", value_1, self.ALT_1_LINE_INDEX)
            result.append(feature)

        return result

    def _draw_line(
        self, alt_desc: str, altitude_value: str, line_number: int
    ) -> Feature:
        offset_lat = self.offset_lat - (self.scaled_line_height * line_number)
        altitude_string = (
            f"{alt_desc}{altitude_value}"
            if alt_desc is not None
            else f"{altitude_value}"
        )
        text = TextDraw(altitude_string, offset_lat, self.offset_lon, self.text_scale)
        result = text.get_feature()
        return result
