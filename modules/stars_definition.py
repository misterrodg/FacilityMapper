from modules.error_helper import print_top_level

ERROR_HEADER = "STARS DEFINITION: "


class STARSDefinition:
    map_id: int | None
    short_name: str | None
    name: str | None
    brightness_category: str | None
    is_tdm_only: bool | None
    is_always_visible: bool | None
    note: str | None
    is_valid: bool | False

    def __init__(self, stars_definition_dict: dict):
        self.map_id = None
        self.short_name = None
        self.name = None
        self.brightness_category = None
        self.is_tdm_only = None
        self.is_always_visible = None
        self.note = None
        self.is_valid = False

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

    def to_dict(self) -> dict:
        result = None
        if self.is_valid:
            result = self._generate_dict()
        return result

    def _generate_dict(self) -> dict:
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
