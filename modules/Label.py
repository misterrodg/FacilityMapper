from modules.ErrorHelper import print_top_level
from modules.GeoJSON import FeatureCollection, GeoJSON
from modules.TextDraw import TextDraw

ERROR_HEADER = "LABEL: "


class Label:
    def __init__(self, definition_dict: dict):
        self.map_type = "LABEL"
        self.lines: list[dict] = []
        self.file_name = None
        self.is_valid = False

        self._validate(definition_dict)

        if self.is_valid:
            self._to_file()

    def _validate(self, definition_dict: dict) -> None:
        lines = definition_dict.get("lines")
        if lines is None:
            print(
                f"{ERROR_HEADER}Missing `lines` in:\n{print_top_level(definition_dict)}."
            )
            return

        file_name = definition_dict.get("file_name")
        if file_name is None:
            print(
                f"{ERROR_HEADER}Missing `file_name` in:\n{print_top_level(definition_dict)}."
            )
            return

        self.lines = lines
        self.file_name = file_name
        self.is_valid = True
        return

    def _to_file(self) -> None:
        feature_collection = FeatureCollection()

        for line in self.lines:
            label_line = LabelLine(line)
            if label_line.is_valid:
                label = TextDraw(
                    label_line.line,
                    label_line.lat,
                    label_line.lon,
                    label_line.text_scale,
                )
                feature = label.get_feature()
                feature_collection.add_feature(feature)

        geo_json = GeoJSON(self.file_name)
        geo_json.add_feature_collection(feature_collection)
        geo_json.to_file()
        return


class LabelLine:
    def __init__(self, line_dict: dict):
        self.line = None
        self.lat = None
        self.lon = None
        self.text_scale = None
        self.is_valid = False

        self._validate(line_dict)

    def _validate(self, line_dict: dict) -> None:
        line = line_dict.get("line")
        if line is None:
            print(f"{ERROR_HEADER}Missing `line` in:\n{print_top_level(line_dict)}.")
            return

        lat = line_dict.get("lat")
        if lat is None:
            print(f"{ERROR_HEADER}Missing `lat` in:\n{print_top_level(line_dict)}.")
            return

        lon = line_dict.get("lon")
        if lon is None:
            print(f"{ERROR_HEADER}Missing `lon` in:\n{print_top_level(line_dict)}.")
            return

        text_scale = line_dict.get("text_scale", 1.0)

        self.line = line
        self.lat = lat
        self.lon = lon
        self.text_scale = text_scale
        self.is_valid = True
        return
