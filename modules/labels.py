from modules.draw import ARC_MIN
from modules.error_helper import print_top_level
from modules.geo_json import Feature, FeatureCollection, GeoJSON
from modules.text_data import TextData

ERROR_HEADER = "LABELS: "


class Labels:
    map_type: str
    labels: list[dict]
    file_name: str | None
    is_valid: bool

    def __init__(self, definition_dict: dict):
        self.map_type = "LABELS"
        self.labels = []
        self.file_name = None
        self.is_valid = False

        self._validate(definition_dict)

        if self.is_valid:
            self._to_file()

    def _validate(self, definition_dict: dict) -> None:
        labels = definition_dict.get("labels")
        if labels is None:
            print(
                f"{ERROR_HEADER}Missing `labels` in:\n{print_top_level(definition_dict)}."
            )
            return

        file_name = definition_dict.get("file_name")
        if file_name is None:
            print(
                f"{ERROR_HEADER}Missing `file_name` in:\n{print_top_level(definition_dict)}."
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
    def __init__(self, line_dict: dict):
        self.lines: list[str] = []
        self.lat = None
        self.lon = None
        self.x_offset = None
        self.y_offset = None
        self.text_scale = None
        self.line_height = None
        self.is_valid = False

        self._validate(line_dict)

    def _validate(self, line_dict: dict) -> None:
        lines = line_dict.get("lines")
        if lines is None:
            print(f"{ERROR_HEADER}Missing `lines` in:\n{print_top_level(line_dict)}.")
            return

        lat = line_dict.get("lat")
        if lat is None:
            print(f"{ERROR_HEADER}Missing `lat` in:\n{print_top_level(line_dict)}.")
            return

        lon = line_dict.get("lon")
        if lon is None:
            print(f"{ERROR_HEADER}Missing `lon` in:\n{print_top_level(line_dict)}.")
            return

        x_offset = line_dict.get("x_offset", 0) * ARC_MIN
        y_offset = line_dict.get("y_offset", 0) * ARC_MIN
        text_scale = line_dict.get("text_scale", 1.0)
        line_height = line_dict.get("line_height", 1.5 * text_scale)

        self.lines = lines
        self.lat = lat
        self.lon = lon
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.text_scale = text_scale
        self.line_height = line_height
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
