class SpeedData:
    speed_desc: str
    speed_limit: int

    def __init__(self, speed_desc: str, speed_limit: int):
        self.speed_desc = speed_desc
        self.speed_limit = speed_limit

    def to_list(self) -> list[str]:
        result = []
        if self.speed_limit is not None:
            result.append(
                f"{self.speed_desc}{self.speed_limit}"
                if self.speed_desc is not None
                else f"{self.speed_limit}"
            )
        return result
