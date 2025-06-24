from modules.definitions.serializable import Serializable


class Composite(Serializable):
    file_names: list[str]
    file_name: str
    delete_originals: bool

    def __init__(self, file_names: list[str], file_name: str):
        self.file_names = file_names
        self.file_name = file_name
        self.delete_originals = False

    def to_dict(self) -> dict:
        return {
            "file_names": self.file_names,
            "file_name": self.file_name,
            "delete_originals": self.delete_originals,
        }
