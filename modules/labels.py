from modules.draw import ARC_MIN
from modules.error_helper import print_top_level
from modules.geo_json import Feature, FeatureCollection, GeoJSON
from modules.stars_draw.text_data import TextData

ERROR_HEADER = "LABELS: "


class Labels:
    map_type: str
    labels: list[dict[str, object]]
    file_name: str
    is_valid: bool

    def __init__(self, definition_dict: dict[str, object]):
        self.map_type = "LABELS"
        self.labels = []
        self.file_name = ""
        self.is_valid = False

        self._validate(definition_dict)

        if self.is_valid:
            self._to_file()

    def _validate(self, definition_dict: dict[str, object]) -> None:
        labels = definition_dict.get("labels")
        if not isinstance(labels, list):
            print(
                f"{ERROR_HEADER}Invalid `labels` in:\n{print_top_level(definition_dict)}."
            )
            return
        for item in labels:
            if not isinstance(item, dict):
                print(
                    f"{ERROR_HEADER}Invalid item in `labels` in:\n{print_top_level(definition_dict)}."
                )
                return

        file_name = definition_dict.get("file_name")
        if not isinstance(file_name, str):
            print(
                f"{ERROR_HEADER}Invalid `file_name` in:\n{print_top_level(definition_dict)}."
            )
            return

        self.labels = labels
        self.file_name = file_name
        self.is_valid = True
        return

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        for label in self.labels:
            label_lines = LabelLines(label)
            if label_lines.is_valid:
                features = label_lines.get_features()
                feature_collection.add_features(features)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return


class LabelLines:
    lines: list[str]
    lat: float
    lon: float
    x_offset: float
    y_offset: float
    text_scale: float
    line_height: float
    is_valid: bool

    def __init__(self, line_dict: dict[str, object]):
        self.lines: list[str] = []
        self.lat = 0.0
        self.lon = 0.0
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.text_scale = 1.0
        self.line_height = 1.5
        self.is_valid = False

        self._validate(line_dict)

    def _validate(self, line_dict: dict[str, object]) -> None:
        lines = line_dict.get("lines")
        if not isinstance(lines, list):
            print(f"{ERROR_HEADER}Invalid `lines` in:\n{print_top_level(line_dict)}.")
            return
        for item in lines:
            if not isinstance(item, str):
                print(
                    f"{ERROR_HEADER}Invalid `lines` in:\n{print_top_level(line_dict)}."
                )
                return

        lat = line_dict.get("lat")
        if not isinstance(lat, (int, float)):
            print(f"{ERROR_HEADER}Invalid `lat` in:\n{print_top_level(line_dict)}.")
            return

        lon = line_dict.get("lon")
        if not isinstance(lon, (int, float)):
            print(f"{ERROR_HEADER}Invalid `lon` in:\n{print_top_level(line_dict)}.")
            return

        x_offset = line_dict.get("x_offset", 0)
        if not isinstance(x_offset, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `x_offset` in:\n{print_top_level(line_dict)}."
            )
            return

        y_offset = line_dict.get("y_offset", 0)
        if not isinstance(y_offset, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `y_offset` in:\n{print_top_level(line_dict)}."
            )
            return

        text_scale = line_dict.get("text_scale", 1.0)
        if not isinstance(text_scale, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `text_scale` in:\n{print_top_level(line_dict)}."
            )
            return

        line_height = line_dict.get("line_height", 1.5 * text_scale)
        if not isinstance(line_height, (int, float)):
            print(
                f"{ERROR_HEADER}Invalid `line_height` in:\n{print_top_level(line_dict)}."
            )
            return

        self.lines = lines
        self.lat = float(lat)
        self.lon = float(lon)
        self.x_offset = float(x_offset) * ARC_MIN
        self.y_offset = float(y_offset) * ARC_MIN
        self.text_scale = float(text_scale)
        self.line_height = float(line_height)
        self.is_valid = True
        return

    def get_features(self) -> list[Feature]:
        result = []

        lines_used = 0

        offset_lat = self.y_offset + self.lat
        offset_lon = self.x_offset + self.lon
        scaled_line_height = self.line_height * ARC_MIN

        for line in self.lines:
            label = TextData(
                line,
                offset_lat,
                offset_lon,
                scaled_line_height,
                self.text_scale,
                lines_used,
            )
            text_feature = label.to_text_feature()
            result.append(text_feature)
            lines_used += 1

        return result
