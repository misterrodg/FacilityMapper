def _handle_bearing_component(bearing_component: int) -> int:
    return (bearing_component + 18) % 36


def _handle_side_component(side_component: str) -> str:
    if side_component == "L":
        return "R"
    if side_component == "R":
        return "L"
    return "C"


def inverse_runway(runway_id: str) -> str:
    runway_prefix = "RW"
    bearing_component = int(runway_id[2:4])
    inverse_bearing = _handle_bearing_component(bearing_component)
    side_component = runway_id[4:]
    inverse_side = ""
    if side_component:
        inverse_side = _handle_side_component(side_component)
    result = f"{runway_prefix}{inverse_bearing:02}{inverse_side}"
    return result


def translate_runway_b(runway_id: str) -> list:
    without_b = runway_id[:-1]
    with_l = f"{without_b}L"
    with_c = f"{without_b}C"
    with_r = f"{without_b}R"
    result = [with_l, with_c, with_r]
    return result
