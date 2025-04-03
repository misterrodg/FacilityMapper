from modules.definitions.v_nas_properties import vNASProperties
from modules.v_nas import (
    TEXT_SIZE_MIN,
    TEXT_SIZE_MAX,
)

ERROR_HEADER = "TEXT PROPERTIES: "


class TextProperties(vNASProperties):
    def __init__(self, properties_dict: dict, is_defaults: bool = False):
        bcg: int = properties_dict.get("bcg")
        filters: list[int] = properties_dict.get("filters")
        super().__init__(bcg, filters)

        self.text: list[str] = self._verify_text(properties_dict.get("text"))
        self.size: int = self._verify_size(properties_dict.get("size"))
        self.underline: bool = self._verify_underline(properties_dict.get("underline"))
        self.x_offset: int = self._verify_offset(properties_dict.get("x_offset"))
        self.y_offset: int = self._verify_offset(properties_dict.get("y_offset"))
        self.opaque: bool = self._verify_opaque(properties_dict.get("opaque"))
        self.is_defaults: bool = is_defaults

    def _verify_text(self, text_list: list[str]) -> list[str]:
        if text_list is not None and (
            isinstance(text_list, list)
            or all(isinstance(item, str) for item in text_list)
        ):
            return text_list
        return None

    def _verify_size(self, text_size: int) -> int:
        if text_size is not None and (
            text_size >= TEXT_SIZE_MIN and text_size <= TEXT_SIZE_MAX
        ):
            return text_size
        return None

    def _verify_underline(self, text_underline: bool) -> bool:
        if text_underline is not None and isinstance(text_underline, bool):
            return text_underline
        return None

    def _verify_offset(self, text_offset: int) -> None:
        if text_offset is not None and isinstance(text_offset, (int, float)):
            return int(text_offset)
        return None

    def _verify_opaque(self, text_opaque: bool) -> bool:
        if text_opaque is not None and isinstance(text_opaque, bool):
            return text_opaque
        return None

    def to_dict(self) -> dict:
        result = super().to_dict()
        if self.is_defaults:
            result["isTextDefaults"] = True
        result["text"] = self.text
        result["size"] = self.size
        result["underline"] = self.underline
        result["xOffset"] = self.x_offset
        result["yOffset"] = self.y_offset
        result["opaque"] = self.opaque
        return result
