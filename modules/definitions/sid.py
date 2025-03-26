from modules.definitions.procedure import Procedure


class SID(Procedure):
    def __init__(self, airport_id: str, procedure_id):
        procedure_id = self._replace_trailing_number(procedure_id)
        super().__init__(airport_id, "SID", procedure_id)

    def to_dict(self) -> dict:
        result = super().to_dict()
        return result
