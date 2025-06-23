from modules.definitions.procedure import Procedure
from modules.definitions.line_properties import LineProperties
from modules.definitions.symbol_properties import SymbolProperties
from modules.definitions.text_properties import TextProperties


class ERAMProcedure(Procedure):
    def __init__(self, airport_id: str, procedure_type: str, procedure_id: str):
        super().__init__(airport_id, procedure_type, procedure_id)
        self.draw_lines: bool = True
        self.suppress_core: bool = False
        self.truncation: float = 0.0
        self.line_defaults: LineProperties = {}
        self.symbol_defaults: SymbolProperties = {}
        self.text_defaults: TextProperties = {}

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        this_dict = {
            "draw_lines": self.draw_lines,
            "suppress_core": self.suppress_core,
            "truncation": self.truncation,
            "line_defaults": self.line_defaults,
            "symbol_defaults": self.symbol_defaults,
            "text_defaults": self.text_defaults,
        }
        return {**base_dict, **this_dict}
