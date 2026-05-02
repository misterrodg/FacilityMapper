from modules.error_helper import print_top_level

ERROR_HEADER = "STARS DEFINITION: "


class STARSDefinition:
    map_id: int
    short_name: str
    name: str
    brightness_category: str
    is_tdm_only: bool
    is_always_visible: bool
    note: str
    is_valid: bool

    def __init__(self, stars_definition_dict: dict[str, object]):
        self.map_id = -1
        self.short_name = ""
        self.name = ""
        self.brightness_category = ""
        self.is_tdm_only = False
        self.is_always_visible = False
        self.note = ""
        self.is_valid = False

        self._validate(stars_definition_dict)

    def _validate(self, stars_definition_dict: dict[str, object]) -> None:
        map_id = stars_definition_dict.get("map_id")
        if not isinstance(map_id, int) or isinstance(map_id, bool) or map_id <= 0:
            map_id = -1

        name = stars_definition_dict.get("name")
        if not isinstance(name, str):
            print(
                f"{ERROR_HEADER}Invalid `name` in:\n{print_top_level(stars_definition_dict)}."
            )
            return

        short_name = stars_definition_dict.get("short_name")
        if not isinstance(short_name, str):
            short_name = name

        brightness_category = stars_definition_dict.get("brightness_category")
        if not isinstance(brightness_category, str):
            brightness_category = "A"

        is_tdm_only = stars_definition_dict.get("tdm_only")
        if not isinstance(is_tdm_only, bool):
            is_tdm_only = False

        is_always_visible = stars_definition_dict.get("always_visible")
        if not isinstance(is_always_visible, bool):
            is_always_visible = False

        note = stars_definition_dict.get("note")
        if not isinstance(note, str):
            note = ""

        self.map_id = map_id
        self.name = name
        self.short_name = short_name
        self.brightness_category = brightness_category
        self.is_tdm_only = is_tdm_only
        self.is_always_visible = is_always_visible
        self.note = note
        self.is_valid = True
        return

    def to_dict(self) -> dict[str, object]:
        if self.is_valid:
            return self._generate_dict()
        return {}

    def _generate_dict(self) -> dict[str, object]:
        result = {}
        result["number"] = self.map_id
        result["shortName"] = self.short_name
        result["longName"] = self.name
        result["briteGroup"] = self.brightness_category
        if self.is_tdm_only:
            result["isTdmOnly"] = self.is_tdm_only
        if self.is_always_visible:
            result["isAlwaysVisible"] = self.is_always_visible
        if self.note != "":
            result["note"] = self.note
        return result
