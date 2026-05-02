class AltitudeData:
    alt_desc: str | None
    alt_1: int | None
    fl_1: bool
    alt_2: int | None
    fl_2: bool

    def __init__(
        self,
        alt_desc: str | None,
        alt_1: int | None,
        fl_1: bool,
        alt_2: int | None,
        fl_2: bool,
    ):
        self.alt_desc = alt_desc
        self.alt_1 = alt_1
        self.fl_1 = fl_1
        self.alt_2 = alt_2
        self.fl_2 = fl_2

    def to_list(self) -> list[str]:
        result = []

        alt_desc = self.alt_desc

        value_1: str | None = None
        if self.alt_1 is not None:
            value_1 = f"FL{self.alt_1}" if self.fl_1 else str(self.alt_1)

        value_2: str | None = None
        if self.alt_2 is not None:
            value_2 = f"FL{self.alt_2}" if self.fl_2 else str(self.alt_2)

        if alt_desc is None:
            # [Blank]: AT
            if value_1 is not None:
                result.append(value_1)
        elif alt_desc in ["+", "-"]:
            # +:AOA // -:AOB
            if value_1 is not None:
                result.append(f"{alt_desc}{value_1}")
        elif alt_desc == "B":
            # B:AOA value_1 and AOB value_2
            if value_1 is not None:
                result.append(value_1)
            if value_2 is not None:
                result.append(value_2)
        elif alt_desc == "C":
            # C:AOA value_2
            if value_2 is not None:
                result.append(f"+{value_2}")
        elif alt_desc == "G":
            # G:AT in value_1 / GS in value_2
            if value_1 is not None:
                result.append(value_1)
        elif alt_desc == "H":
            # H:AOA in value_1 / GS in value_2
            if value_1 is not None:
                result.append(f"+{value_1}")
        elif alt_desc == "I":
            # I:AT in value_1 / GS Int in value_2
            if value_1 is not None:
                result.append(value_1)
        elif alt_desc == "J":
            # J:AOA in value_1 / GS Int in value_2
            if value_1 is not None:
                result.append(f"+{value_1}")
        elif alt_desc == "V":
            # V:AT Step Down in value_1 / AT in value_2
            # Says "AT" but charts display as AOA as a catchall, with value_2 used by aircraft systems
            if value_1 is not None:
                result.append(f"+{value_1}")
        elif alt_desc == "Y":
            # Y:AOB Step Down in value_1 / AT in value_2
            if value_1 is not None:
                result.append(f"-{value_1}")

        return result
