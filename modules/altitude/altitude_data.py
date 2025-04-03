class AltitudeData:
    def __init__(
        self,
        alt_desc: str,
        altitude: int,
        flight_level: int,
        altitude_2: int,
        flight_level_2: int,
    ):
        self.alt_desc: str = alt_desc
        self.altitude: int = altitude
        self.flight_level: int = flight_level
        self.altitude_2: int = altitude_2
        self.flight_level_2: int = flight_level_2

    def to_list(self) -> list[str]:
        result = []

        value_1 = str(self.altitude) if self.altitude else f"FL{self.flight_level}"
        value_2 = (
            str(self.altitude_2) if self.altitude_2 else f"FL{self.flight_level_2}"
        )
        alt_desc = self.alt_desc

        if alt_desc in ["+", "-"]:
            # +:AOA // -:AOB
            result.append(f"{alt_desc}{value_1}")
        if alt_desc == "B":
            # B:AOA value_1 and AOB value_2
            result.append(value_1)
            result.append(value_2)
        if alt_desc == "C":
            # C:AOA value_2
            result.append(f"+{value_2}")
        if alt_desc == "G":
            # G:AT in value_1 / GS in value_2
            result.append(value_1)
        if alt_desc == "H":
            # H:AOA in value_1 / GS in value_2
            result.append(f"+{value_1}")
        if alt_desc == "I":
            # I:AT in value_1 / GS Int in value_2
            result.append(value_1)
        if alt_desc == "J":
            # J:AOA in value_1 / GS Int in value_2
            result.append(f"+{value_1}")
        if alt_desc == "V":
            # V:AT Step Down in value_1 / AT in value_2
            # Says "AT" but charts display as AOA as a catchall, with value_2 used by aircraft systems
            result.append(f"+{value_1}")
        if alt_desc == "Y":
            # Y:AOB Step Down in value_1 / AT in value_2
            result.append(f"-{value_1}")

        return result
