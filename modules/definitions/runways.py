from modules.definitions.serializable import Serializable


class Runways(Serializable):
    airport_ids: list[str]
    file_name: str

    def __init__(self, airport_ids: list[str], file_name: str):
        self.airport_ids = airport_ids
        self.file_name = file_name

    def to_dict(self) -> dict:
        return {
            "airport_ids": self.airport_ids,
            "file_name": self.file_name,
        }
