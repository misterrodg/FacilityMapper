from modules.definitions.v_nas_properties import vNASProperties
from modules.v_nas import (
    SYMBOL_STYLES,
    SYMBOL_SIZE_MIN,
    SYMBOL_SIZE_MAX,
)


class SymbolProperties(vNASProperties):
    size: int | None
    style: str | None
    is_defaults: bool

    def __init__(self, properties_dict: dict, is_defaults: bool = False) -> None:
        bcg = properties_dict.get("bcg")
        filters = properties_dict.get("filters")
        super().__init__(bcg, filters)

        self.size = self._verify_size(properties_dict.get("size"))
        self.style = self._verify_style(properties_dict.get("style"))
        self.is_defaults = is_defaults

    def _verify_style(self, symbol_style: str | None) -> str | None:
        if symbol_style is not None and symbol_style in SYMBOL_STYLES:
            return symbol_style
        return None

    def _verify_size(self, symbol_size: int | None) -> int | None:
        if symbol_size is not None and (
            symbol_size >= SYMBOL_SIZE_MIN and symbol_size <= SYMBOL_SIZE_MAX
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
