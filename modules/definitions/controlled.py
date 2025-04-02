from modules.definitions.airspace import Airspace


class Controlled(Airspace):
    def __init__(self, airport_id: str, airspace_class: str):
        self.airport_id: str = airport_id
        file_name = f"{airport_id}_CLASS_{airspace_class}"
        super().__init__(file_name)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["airport_id"] = self.airport_id
        return result
