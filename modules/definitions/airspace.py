from modules.definitions.serializable import Serializable


class Airspace(Serializable):
    file_name: str

    def __init__(self, file_name: str):
        self.file_name = file_name

    def to_dict(self) -> dict:
        return {
            "file_name": self.file_name,
        }
