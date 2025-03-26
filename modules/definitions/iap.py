from modules.definitions.procedure import Procedure


class IAP(Procedure):
    def __init__(self, airport_id: str, procedure_id):
        super().__init__(airport_id, "IAP", procedure_id)
        self.transition_ids: list[str] = ["ALL"]

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["transition_ids"] = self.transition_ids
        return result
