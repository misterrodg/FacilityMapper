from modules.error_helper import print_top_level
from modules.geo_json import FeatureCollection, GeoJSON

ERROR_HEADER = "COMPOSITE: "


class Composite:
    def __init__(self, definition_dict: dict):
        self.map_type = "COMPOSITE"
        self.file_names: list[dict] = []
        self.file_name = None
        self.delete_originals = False
        self.is_valid = False

        self._validate(definition_dict)

        if self.is_valid:
            self._to_file()

    def _validate(self, definition_dict: dict) -> None:
        file_names = definition_dict.get("file_names")
        if file_names is None:
            print(
                f"{ERROR_HEADER}Missing `file_names` in:\n{print_top_level(definition_dict)}."
            )
            return

        file_name = definition_dict.get("file_name")
        if file_name is None:
            print(
                f"{ERROR_HEADER}Missing `file_name` in:\n{print_top_level(definition_dict)}."
            )
            return

        delete_originals = definition_dict.get("delete_originals", False)

        self.file_names = file_names
        self.file_name = file_name
        self.delete_originals = delete_originals
        self.is_valid = True
        return

    def _to_file(self) -> None:
        composite_feature_collection = FeatureCollection()
        composite_file = GeoJSON(self.file_name)

        for file_name in self.file_names:
            geo_json = GeoJSON(file_name)
            geo_json.from_file(True)
            features = geo_json.pluck_features()
            for feature in features:
                composite_feature_collection.add_feature(feature)
            if self.delete_originals:
                geo_json.delete_file()

        composite_file.add_feature_collection(composite_feature_collection)
        composite_file.to_file(True)
        return
