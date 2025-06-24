class AltitudeData:
    alt_desc: str
    alt_1: int
    fl_1: int
    alt_2: int
    fl_2: int

    def __init__(
        self,
        alt_desc: str,
        alt_1: int,
        fl_1: int,
        alt_2: int,
        fl_2: int,
    ):
        self.alt_desc = alt_desc
        self.alt_1 = alt_1
        self.fl_1 = fl_1
        self.alt_2 = alt_2
        self.fl_2 = fl_2

    def to_list(self) -> list[str]:
        result = []

        alt_desc = self.alt_desc

        value_1 = None
        if self.alt_1 is not None:
            value_1 = f"FL{self.alt_1}" if self.fl_1 else str(self.alt_1)

        value_2 = None
        if self.alt_2 is not None:
            value_2 = f"FL{self.alt_2}" if self.fl_2 else str(self.alt_2)

        if alt_desc is None and value_1 is not None:
            # [Blank]: AT
            result.append(value_1)
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
