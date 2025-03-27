RUNWAY_PREFIX = "RW"


def inverse_runway(runway_id: str) -> str:
    bearing_component = int(runway_id[2:4])
    inverse_bearing = _handle_bearing_component(bearing_component)
    side_component = runway_id[4:]
    inverse_side = ""
    if side_component:
        inverse_side = _handle_side_component(side_component)
    result = f"{RUNWAY_PREFIX}{inverse_bearing:02}{inverse_side}"
    return result


def split_runway_id(runway_id: str) -> dict:
    bearing_component = runway_id[2:4]
    side_component = runway_id[4:]
    return {
        "prefix": RUNWAY_PREFIX,
        "bearing_component": bearing_component,
        "side_component": side_component,
    }


def _handle_bearing_component(bearing_component: int) -> int:
    if bearing_component == 18:
        return 36
    return (bearing_component + 18) % 36


def _handle_side_component(side_component: str) -> str:
    # Shortcut the edge cases where a runway is named like "RW212" (usually mil field tactical strips)
    if side_component.isnumeric():
        return side_component
    # Side-based Runways
    if side_component == "L":
        return "R"
    if side_component == "R":
        return "L"
    if side_component == "C":
        return "C"
    # Other oddities (surface types, generally)
    if side_component in ["G", "S", "U", "W"]:
        return side_component
    return ""
