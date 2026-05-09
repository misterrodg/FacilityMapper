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

COMPUTED = [
    {"lat_offset": 3, "lon_offset": 3},
    {"lat_offset": -3, "lon_offset": -3},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": -3, "lon_offset": 3},
    {"lat_offset": 3, "lon_offset": -3},
]

CHEVRON = [
    {"lat_offset": -10, "lon_offset": -10},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": -10, "lon_offset": 10},
]


ARROW_HEAD_SYMBOL = "ARROW_HEAD"
ARROW_HEAD_HOLLOW_SYMBOL = "ARROW_HEAD_HOLLOW"
ARROW_TAIL_SYMBOL = "ARROW_TAIL"
TRIANGLE_SYMBOL = "TRIANGLE"
SQUARE_SYMBOL = "SQUARE"
HEXAGON_SYMBOL = "HEXAGON"
CHEVRON_SYMBOL = "CHEVRON"
CIRCLE_L_SYMBOL = "CIRCLE_L"
CIRCLE_S_SYMBOL = "CIRCLE_S"
CROSSBAR_SYMBOL = "CROSSBAR"
DME_BOX_SYMBOL = "DME_BOX"
RNAV_SYMBOL = "RNAV"
FAF_SYMBOL = "FAF"
COMPUTED_SYMBOL = "COMPUTED"
AVAILABLE_SYMBOLS = [
    ARROW_HEAD_SYMBOL,
    ARROW_HEAD_HOLLOW_SYMBOL,
    ARROW_TAIL_SYMBOL,
    TRIANGLE_SYMBOL,
    SQUARE_SYMBOL,
    HEXAGON_SYMBOL,
    CHEVRON_SYMBOL,
    CIRCLE_L_SYMBOL,
    CIRCLE_S_SYMBOL,
    CROSSBAR_SYMBOL,
    DME_BOX_SYMBOL,
    RNAV_SYMBOL,
    FAF_SYMBOL,
    COMPUTED_SYMBOL,
]

SYMBOL_PLOT_MAP: dict[str, list[dict]] = {
    ARROW_HEAD_SYMBOL: ARROW_HEAD,
    ARROW_HEAD_HOLLOW_SYMBOL: ARROW_HEAD_HOLLOW,
    ARROW_TAIL_SYMBOL: ARROW_TAIL,
    TRIANGLE_SYMBOL: TRIANGLE,
    SQUARE_SYMBOL: SQUARE,
    HEXAGON_SYMBOL: HEXAGON,
    CHEVRON_SYMBOL: CHEVRON,
    CIRCLE_L_SYMBOL: CIRCLE_L,
    CIRCLE_S_SYMBOL: CIRCLE_S,
    CROSSBAR_SYMBOL: CROSSBAR,
    DME_BOX_SYMBOL: DME_BOX,
    RNAV_SYMBOL: RNAV,
    FAF_SYMBOL: FAF,
    COMPUTED_SYMBOL: COMPUTED,
}


def get_plot(symbol: str) -> list[dict]:
    return SYMBOL_PLOT_MAP.get(symbol, UNRECOGNIZED)
