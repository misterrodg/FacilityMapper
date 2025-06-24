from modules.definitions.serializable import Serializable
from modules.definitions.centerline import Centerline


class Centerlines(Serializable):
    airport_id: str
    file_name: str
    centerlines: list[Centerline]

    def __init__(self, airport_id: str):
        self.airport_id = airport_id
        self.file_name = f"{airport_id}_CENTERLINES"
        self.centerlines = []

    def add_centerline(self, centerline: Centerline) -> None:
        self.centerlines.append(centerline)

    def to_dict(self) -> dict:
        centerlines = []

        for centerline in self.centerlines:
            centerlines.append(centerline.to_dict())

        return {
            "airport_id": self.airport_id,
            "file_name": self.file_name,
            "centerlines": centerlines,
        }
