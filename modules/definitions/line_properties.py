from modules.definitions.v_nas_properties import vNASProperties
from modules.v_nas import (
    LINE_STYLES,
    LINE_THICKNESS_MIN,
    LINE_THICKNESS_MAX,
)


class LineProperties(vNASProperties):
    def __init__(self, properties_dict: dict, is_defaults: bool = False):
        bcg = properties_dict.get("bcg")
        filters = properties_dict.get("filters")
        super().__init__(bcg, filters)

        self.style = self._verify_style(properties_dict.get("style"))
        self.thickness = self._verify_thickness(properties_dict.get("thickness"))
        self.is_defaults = is_defaults

    def _verify_style(self, line_style: str) -> None:
        if line_style in LINE_STYLES:
            return line_style
        return None

    def _verify_thickness(self, line_thickness: int) -> None:
        if line_thickness and (
            line_thickness >= LINE_THICKNESS_MIN
            and line_thickness <= LINE_THICKNESS_MAX
        ):
            return line_thickness
        return None

    def to_dict(self) -> dict:
        result = super().to_dict()
        if self.is_defaults:
            result["isLineDefaults"] = True
        result["style"] = self.style
        result["thickness"] = self.thickness
        return result
