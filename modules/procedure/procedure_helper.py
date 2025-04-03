DE_LEADING_ROUTE_TYPES = ["1", "4"]
DE_TRAILING_ROUTE_TYPES = ["3", "6"]


def translate_map_type(map_type: str) -> str:
    if map_type == "SID":
        return "D"
    if map_type == "STAR":
        return "E"
    if map_type == "IAP":
        return "F"
    return ""
