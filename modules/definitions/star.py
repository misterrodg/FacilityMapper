from modules.definitions.procedure import Procedure


class STAR(Procedure):
    def __init__(self, airport_id: str, procedure_id):
        procedure_id = self._replace_trailing_number(procedure_id)
        super().__init__(airport_id, "STAR", procedure_id)
        self.vector_length: float = 2.5

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["vector_length"] = self.vector_length
        return result
