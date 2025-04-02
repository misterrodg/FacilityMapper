from modules.error_helper import print_top_level
from typing import TextIO

ERROR_HEADER = "STARS DEFINITION: "
DEFINITION_HEADER = (
    "map_id,short_name,name,brightness_category,is_tdm_only,is_always_visible,note\n"
)


class STARSDefinition:
    def __init__(self, stars_definition_dict: dict):
        self.map_id: int = None
        self.short_name: str = None
        self.name: str = None
        self.brightness_category: str = None
        self.is_tdm_only: bool = None
        self.is_always_visible: bool = None
        self.note: str = None
        self.is_valid: bool = False

        self._validate(stars_definition_dict)

    def _validate(self, stars_definition_dict: dict) -> None:
        map_id = stars_definition_dict.get("map_id")
        self.map_id = map_id

        name = stars_definition_dict.get("name")
        if name is None:
            print(
                f"{ERROR_HEADER}Missing `name` in:\n{print_top_level(stars_definition_dict)}."
            )
            return
        self.name = name

        short_name = stars_definition_dict.get("short_name")
        if short_name is None:
            short_name = name
        self.short_name = short_name

        brightness_category = stars_definition_dict.get("brightness_category")
        if brightness_category is None:
            brightness_category = "A"
        self.brightness_category = brightness_category

        is_tdm_only = stars_definition_dict.get("tdm_only")
        if is_tdm_only is None:
            is_tdm_only = False
        self.is_tdm_only = is_tdm_only

        is_always_visible = stars_definition_dict.get("always_visible")
        if is_always_visible is None:
            is_always_visible = False
        self.is_always_visible = is_always_visible

        note = stars_definition_dict.get("note")
        if note is None:
            note = ""
        self.note = note

        self.is_valid = True
        return

    def to_line(self) -> str:
        result = None
        if self.is_valid:
            result = f"{self.map_id},{self.short_name},{self.name},{self.brightness_category},{self.is_tdm_only},{self.is_always_visible},{self.note}\n"
        return result
