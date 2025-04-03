class SpeedData:
    def __init__(self, speed_desc: str, speed: int):
        self.speed_desc: str = speed_desc
        self.speed: int = speed

    def to_list(self) -> list[str]:
        result = []
        if self.speed is not None:
            result.append(
                f"{self.speed_desc}{self.speed}"
                if self.speed_desc is not None
                else f"{self.speed}"
            )
        return result
