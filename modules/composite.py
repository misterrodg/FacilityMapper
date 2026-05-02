from modules.error_helper import print_top_level
from modules.geo_json import FeatureCollection, GeoJSON

ERROR_HEADER = "COMPOSITE: "


class Composite:
    map_type: str
    file_names: list[str]
    file_name: str
    delete_originals: bool
    is_valid: bool

    def __init__(self, definition_dict: dict[str, object]):
        self.map_type = "COMPOSITE"
        self.file_names = []
        self.file_name = ""
        self.delete_originals = False
        self.is_valid = False

        self._validate(definition_dict)

        if self.is_valid:
            self._to_file()

    def _validate(self, definition_dict: dict[str, object]) -> None:
        file_names = definition_dict.get("file_names")
        if not isinstance(file_names, list):
            print(
                f"{ERROR_HEADER}Invalid `file_names` in:\n{print_top_level(definition_dict)}."
            )
            return
        for item in file_names:
            if not isinstance(item, str):
                print(
                    f"{ERROR_HEADER}Invalid item in `file_names` in:\n{print_top_level(definition_dict)}."
                )
                return

        file_name = definition_dict.get("file_name")
        if not isinstance(file_name, str):
            print(
                f"{ERROR_HEADER}Invalid `file_name` in:\n{print_top_level(definition_dict)}."
            )
            return

        delete_originals = definition_dict.get("delete_originals", False)
        if not isinstance(delete_originals, bool):
            print(
                f"{ERROR_HEADER}Invalid `delete_originals` in:\n{print_top_level(definition_dict)}."
            )
            return

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
            raw_features = geo_json.pluck_raw_features()
            composite_feature_collection.add_raw_features(raw_features)
            if self.delete_originals:
                geo_json.delete_file()

        composite_file.add_feature_collection(composite_feature_collection)
        composite_file.to_file(True)
        return
