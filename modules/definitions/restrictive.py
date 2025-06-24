from modules.definitions.airspace import Airspace


class Restrictive(Airspace):
    restrictive_id: str

    def __init__(self, restrictive_id: str, restrictive_type: str):
        self.restrictive_id = restrictive_id
        file_name = f"{restrictive_type}_{restrictive_id}"
        super().__init__(file_name)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["restrictive_id"] = self.restrictive_id
        return result
