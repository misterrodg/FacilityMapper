DE_LEADING_PROCEDURE_TYPES = ["1", "4"]
DE_CORE_PROCEDURE_TYPES = ["2", "5"]
DE_TRAILING_PROCEDURE_TYPES = ["3", "6"]
F_LEADING_PROCEDURE_TYPES = ["A"]


def translate_map_type(map_type: str) -> str:
    if map_type == "SID":
        return "D"
    if map_type == "STAR":
        return "E"
    if map_type == "IAP":
        return "F"
    return ""
