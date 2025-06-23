from modules.definitions.procedure import Procedure


class STARSProcedure(Procedure):
    def __init__(self, airport_id: str, procedure_type: str, procedure_id: str):
        super().__init__(airport_id, procedure_type, procedure_id)
        self.line_type: str = "solid"
        self.x_offset: float = 0.0
        self.y_offset: float = 0.0
        self.symbol_scale: float = 1.0
        self.text_scale: float = 1.0
        self.line_height: float = 1.5
        self.draw_missed: bool = False
        self.vector_length: float = 2.5

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        this_dict = {
            "line_type": self.line_type,
            "x_offset": self.x_offset,
            "y_offset": self.y_offset,
            "symbol_scale": self.symbol_scale,
            "text_scale": self.text_scale,
            "line_height": self.line_height,
            "draw_missed": self.draw_missed,
            "vector_length": self.vector_length,
        }
        return {**base_dict, **this_dict}
