from modules.definitions.procedure import Procedure
from modules.definitions.line_properties import LineProperties
from modules.definitions.symbol_properties import SymbolProperties
from modules.definitions.text_properties import TextProperties


class ERAMProcedure(Procedure):
    draw_lines: bool
    suppress_core: bool
    truncation: float
    line_defaults: LineProperties | object
    symbol_defaults: SymbolProperties | object
    text_defaults: TextProperties | object

    def __init__(self, airport_id: str, procedure_type: str, procedure_id: str):
        super().__init__(airport_id, procedure_type, procedure_id)
        self.draw_lines = True
        self.suppress_core = False
        self.truncation = 0.0
        self.line_defaults = {}
        self.symbol_defaults = {}
        self.text_defaults = {}

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
