from modules.definitions.serializable import Serializable


class Composite(Serializable):
    def __init__(self, file_names: list, file_name: str):
        self.file_names: list = file_names
        self.file_name: str = file_name
        self.delete_originals: bool = False

    def to_dict(self) -> dict:
        return {
            "file_names": self.file_names,
            "file_name": self.file_name,
            "delete_originals": self.delete_originals,
        }
