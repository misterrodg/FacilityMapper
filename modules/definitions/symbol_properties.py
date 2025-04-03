from modules.definitions.v_nas_properties import vNASProperties
from modules.v_nas import (
    SYMBOL_STYLES,
    SYMBOL_SIZE_MIN,
    SYMBOL_SIZE_MAX,
)


class SymbolProperties(vNASProperties):
    def __init__(self, properties_dict: dict, is_defaults: bool = False):
        bcg: int = properties_dict.get("bcg")
        filters: list[int] = properties_dict.get("filters")
        super().__init__(bcg, filters)

        self.size = self._verify_size(properties_dict.get("size"))
        self.style = self._verify_style(properties_dict.get("style"))
        self.is_defaults = is_defaults

    def _verify_style(self, symbol_style: str) -> str:
        if symbol_style in SYMBOL_STYLES:
            return symbol_style
        return None

    def _verify_size(self, symbol_size: int) -> int:
        if (
            symbol_size
            and symbol_size >= SYMBOL_SIZE_MIN
            and symbol_size <= SYMBOL_SIZE_MAX
        ):
            return symbol_size
        return None

    def to_dict(self) -> dict:
        result = super().to_dict()
        if self.is_defaults:
            result["isSymbolDefaults"] = True
        result["size"] = self.size
        result["style"] = self.style
        return result
