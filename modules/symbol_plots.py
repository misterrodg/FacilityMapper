# Points are given in Lat/Lon Offsets: (0,0) is middle of symbol; (10,10) top right; (-10,-10) bottom left

PLOT_HEIGHT = 21
PLOT_WIDTH = 21

UNRECOGNIZED = [{"lat_offset": 0, "lon_offset": 0}]

ARROW_HEAD = [
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": -9},
    {"lat_offset": 20, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": 9},
    {"lat_offset": 11, "lon_offset": -8},
    {"lat_offset": 19, "lon_offset": 0},
    {"lat_offset": 12, "lon_offset": 7},
    {"lat_offset": 12, "lon_offset": -6},
    {"lat_offset": 18, "lon_offset": 0},
    {"lat_offset": 13, "lon_offset": 5},
    {"lat_offset": 13, "lon_offset": -4},
    {"lat_offset": 17, "lon_offset": 0},
    {"lat_offset": 14, "lon_offset": 3},
    {"lat_offset": 14, "lon_offset": -2},
    {"lat_offset": 16, "lon_offset": 0},
    {"lat_offset": 15, "lon_offset": 1},
    {"lat_offset": 15, "lon_offset": 0},
]

ARROW_HEAD_HOLLOW = [
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": -9},
    {"lat_offset": 20, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": 9},
    {"lat_offset": 11, "lon_offset": 0},
]

ARROW_TAIL = [
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": -20, "lon_offset": 0},
]

TRIANGLE = [
    {"lat_offset": 9, "lon_offset": 0},
    {"lat_offset": -8, "lon_offset": 10},
    {"lat_offset": -8, "lon_offset": -10},
    {"lat_offset": 9, "lon_offset": 0},
]

SQUARE = [
    {"lat_offset": 10, "lon_offset": -10},
    {"lat_offset": 10, "lon_offset": 10},
    {"lat_offset": -10, "lon_offset": 10},
    {"lat_offset": -10, "lon_offset": -10},
    {"lat_offset": 10, "lon_offset": -10},
]

HEXAGON = [
    {"lat_offset": 0, "lon_offset": -10},
    {"lat_offset": 9, "lon_offset": -5},
    {"lat_offset": 9, "lon_offset": 5},
    {"lat_offset": 0, "lon_offset": 10},
    {"lat_offset": -9, "lon_offset": 5},
    {"lat_offset": -9, "lon_offset": -5},
    {"lat_offset": 0, "lon_offset": -10},
]

CIRCLE_L = [
    {"lat_offset": 10, "lon_offset": 0},
    {"lat_offset": 9, "lon_offset": 4},
    {"lat_offset": 7, "lon_offset": 7},
    {"lat_offset": 4, "lon_offset": 9},
    {"lat_offset": 0, "lon_offset": 10},
    {"lat_offset": -4, "lon_offset": 9},
    {"lat_offset": -7, "lon_offset": 7},
    {"lat_offset": -9, "lon_offset": 4},
    {"lat_offset": -10, "lon_offset": 0},
    {"lat_offset": -9, "lon_offset": -4},
    {"lat_offset": -7, "lon_offset": -7},
    {"lat_offset": -4, "lon_offset": -9},
    {"lat_offset": 0, "lon_offset": -10},
    {"lat_offset": 4, "lon_offset": -9},
    {"lat_offset": 7, "lon_offset": -7},
    {"lat_offset": 9, "lon_offset": -4},
    {"lat_offset": 10, "lon_offset": 0},
]

CIRCLE_S = [
    {"lat_offset": 3, "lon_offset": 0},
    {"lat_offset": 2, "lon_offset": 2},
    {"lat_offset": 0, "lon_offset": 3},
    {"lat_offset": -2, "lon_offset": 2},
    {"lat_offset": -3, "lon_offset": 0},
    {"lat_offset": -2, "lon_offset": -2},
    {"lat_offset": 0, "lon_offset": -3},
    {"lat_offset": 2, "lon_offset": -2},
    {"lat_offset": 3, "lon_offset": 0},
]

CROSSBAR = [
    {"lat_offset": 0, "lon_offset": -10},
    {"lat_offset": 0, "lon_offset": 10},
]

DME_BOX = [
    {"lat_offset": 9, "lon_offset": -10},
    {"lat_offset": 9, "lon_offset": 10},
    {"lat_offset": -9, "lon_offset": 10},
    {"lat_offset": -9, "lon_offset": -10},
    {"lat_offset": 9, "lon_offset": -10},
]

RNAV = [
    {"lat_offset": 3, "lon_offset": -3},
    {"lat_offset": 4, "lon_offset": 0},
    {"lat_offset": 3, "lon_offset": 3},
    {"lat_offset": 0, "lon_offset": 4},
    {"lat_offset": -3, "lon_offset": 3},
    {"lat_offset": -4, "lon_offset": 0},
    {"lat_offset": -3, "lon_offset": -3},
    {"lat_offset": 0, "lon_offset": -4},
    {"lat_offset": 3, "lon_offset": -3},
    {"lat_offset": 5, "lon_offset": -2},
    {"lat_offset": 10, "lon_offset": 0},
    {"lat_offset": 5, "lon_offset": 2},
    {"lat_offset": 3, "lon_offset": 3},
    {"lat_offset": 2, "lon_offset": 5},
    {"lat_offset": 0, "lon_offset": 10},
    {"lat_offset": -2, "lon_offset": 5},
    {"lat_offset": -3, "lon_offset": 3},
    {"lat_offset": -5, "lon_offset": 2},
    {"lat_offset": -10, "lon_offset": 0},
    {"lat_offset": -5, "lon_offset": -2},
    {"lat_offset": -3, "lon_offset": -3},
    {"lat_offset": -2, "lon_offset": -5},
    {"lat_offset": 0, "lon_offset": -10},
    {"lat_offset": 2, "lon_offset": -5},
    {"lat_offset": 3, "lon_offset": -3},
]

FAF = [
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 10, "lon_offset": 4},
    {"lat_offset": 4, "lon_offset": 10},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": -4, "lon_offset": 10},
    {"lat_offset": -10, "lon_offset": 4},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": -10, "lon_offset": -4},
    {"lat_offset": -4, "lon_offset": -10},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 4, "lon_offset": -10},
    {"lat_offset": 10, "lon_offset": -4},
    {"lat_offset": 0, "lon_offset": 0},
]


def get_plot_from_string(textValue: str) -> list[dict]:
    upperValue = textValue.upper()
    if upperValue == "ARROW_HEAD":
        return ARROW_HEAD
    if upperValue == "ARROW_HEAD_HOLLOW":
        return ARROW_HEAD_HOLLOW
    if upperValue == "ARROW_TAIL":
        return ARROW_TAIL
    if upperValue == "TRIANGLE":
        return TRIANGLE
    if upperValue == "SQUARE":
        return SQUARE
    if upperValue == "HEXAGON":
        return HEXAGON
    if upperValue == "CIRCLE_L":
        return CIRCLE_L
    if upperValue == "CIRCLE_S":
        return CIRCLE_S
    if upperValue == "CROSSBAR":
        return CROSSBAR
    if upperValue == "DME_BOX":
        return DME_BOX
    if upperValue == "RNAV":
        return RNAV
    if upperValue == "FAF":
        return FAF
    return UNRECOGNIZED
