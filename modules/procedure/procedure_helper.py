DE_LEADING_ROUTE_TYPES = ["1", "4"]
DE_CORE_ROUTE_TYPES = ["2", "5"]
DE_TRAILING_ROUTE_TYPES = ["3", "6"]
F_LEADING_ROUTE_TYPES = ["A"]


def translate_map_type(map_type: str) -> str:
    if map_type == "SID":
        return "D"
    if map_type == "STAR":
        return "E"
    if map_type == "IAP":
        return "F"
    return ""
