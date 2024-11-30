# Points are given in Lat/Lon Offsets: (0,0) is bottom left of character; (21,21) top right

PLOT_HEIGHT = 21
PLOT_WIDTH = 21

UNRECOGNIZED = [{"lat_offset": 0, "lon_offset": 0}]

SPACE = []

DOT = [
    {"lat_offset": 0, "lon_offset": 6},
    {"lat_offset": 2, "lon_offset": 6},
    {"lat_offset": 2, "lon_offset": 8},
    {"lat_offset": 0, "lon_offset": 8},
    {"lat_offset": 0, "lon_offset": 6},
]

MINUS = [
    {"lat_offset": 10, "lon_offset": 4},
    {"lat_offset": 10, "lon_offset": 14},
]

PLUS = [
    {"lat_offset": 10, "lon_offset": 4},
    {"lat_offset": 10, "lon_offset": 14},
    {"lat_offset": 10, "lon_offset": 9},
    {"lat_offset": 15, "lon_offset": 9},
    {"lat_offset": 5, "lon_offset": 9},
]

ZERO = [
    {"lat_offset": 4, "lon_offset": 1},
    {"lat_offset": 1, "lon_offset": 3},
    {"lat_offset": 0, "lon_offset": 6},
    {"lat_offset": 0, "lon_offset": 8},
    {"lat_offset": 1, "lon_offset": 11},
    {"lat_offset": 4, "lon_offset": 13},
    {"lat_offset": 9, "lon_offset": 14},
    {"lat_offset": 12, "lon_offset": 14},
    {"lat_offset": 17, "lon_offset": 13},
    {"lat_offset": 20, "lon_offset": 11},
    {"lat_offset": 21, "lon_offset": 8},
    {"lat_offset": 21, "lon_offset": 6},
    {"lat_offset": 20, "lon_offset": 3},
    {"lat_offset": 17, "lon_offset": 1},
    {"lat_offset": 12, "lon_offset": 0},
    {"lat_offset": 9, "lon_offset": 0},
    {"lat_offset": 4, "lon_offset": 1},
    {"lat_offset": 17, "lon_offset": 13},
]

ONE = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 3},
    {"lat_offset": 0, "lon_offset": 3},
]

TWO = [
    {"lat_offset": 16, "lon_offset": 0},
    {"lat_offset": 17, "lon_offset": 0},
    {"lat_offset": 19, "lon_offset": 1},
    {"lat_offset": 20, "lon_offset": 2},
    {"lat_offset": 21, "lon_offset": 4},
    {"lat_offset": 21, "lon_offset": 8},
    {"lat_offset": 20, "lon_offset": 10},
    {"lat_offset": 19, "lon_offset": 11},
    {"lat_offset": 17, "lon_offset": 12},
    {"lat_offset": 15, "lon_offset": 12},
    {"lat_offset": 13, "lon_offset": 11},
    {"lat_offset": 10, "lon_offset": 9},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 12},
]

THREE = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 11},
    {"lat_offset": 13, "lon_offset": 5},
    {"lat_offset": 13, "lon_offset": 8},
    {"lat_offset": 11, "lon_offset": 11},
    {"lat_offset": 8, "lon_offset": 12},
    {"lat_offset": 6, "lon_offset": 12},
    {"lat_offset": 3, "lon_offset": 11},
    {"lat_offset": 1, "lon_offset": 9},
    {"lat_offset": 0, "lon_offset": 6},
    {"lat_offset": 0, "lon_offset": 3},
    {"lat_offset": 1, "lon_offset": 0},
]

FOUR = [
    {"lat_offset": 0, "lon_offset": 8},
    {"lat_offset": 21, "lon_offset": 8},
    {"lat_offset": 7, "lon_offset": 0},
    {"lat_offset": 7, "lon_offset": 13},
]

FIVE = [
    {"lat_offset": 21, "lon_offset": 11},
    {"lat_offset": 21, "lon_offset": 1},
    {"lat_offset": 12, "lon_offset": 0},
    {"lat_offset": 13, "lon_offset": 1},
    {"lat_offset": 14, "lon_offset": 4},
    {"lat_offset": 14, "lon_offset": 7},
    {"lat_offset": 13, "lon_offset": 10},
    {"lat_offset": 11, "lon_offset": 12},
    {"lat_offset": 8, "lon_offset": 13},
    {"lat_offset": 6, "lon_offset": 13},
    {"lat_offset": 3, "lon_offset": 12},
    {"lat_offset": 1, "lon_offset": 10},
    {"lat_offset": 0, "lon_offset": 7},
    {"lat_offset": 0, "lon_offset": 4},
    {"lat_offset": 1, "lon_offset": 1},
    {"lat_offset": 2, "lon_offset": 0},
]

SIX = [
    {"lat_offset": 18, "lon_offset": 12},
    {"lat_offset": 20, "lon_offset": 11},
    {"lat_offset": 21, "lon_offset": 8},
    {"lat_offset": 21, "lon_offset": 6},
    {"lat_offset": 20, "lon_offset": 3},
    {"lat_offset": 17, "lon_offset": 1},
    {"lat_offset": 12, "lon_offset": 0},
    {"lat_offset": 7, "lon_offset": 0},
    {"lat_offset": 3, "lon_offset": 1},
    {"lat_offset": 1, "lon_offset": 3},
    {"lat_offset": 0, "lon_offset": 6},
    {"lat_offset": 0, "lon_offset": 7},
    {"lat_offset": 1, "lon_offset": 10},
    {"lat_offset": 3, "lon_offset": 12},
    {"lat_offset": 6, "lon_offset": 13},
    {"lat_offset": 7, "lon_offset": 13},
    {"lat_offset": 10, "lon_offset": 12},
    {"lat_offset": 12, "lon_offset": 10},
    {"lat_offset": 13, "lon_offset": 7},
    {"lat_offset": 13, "lon_offset": 6},
    {"lat_offset": 12, "lon_offset": 3},
    {"lat_offset": 10, "lon_offset": 1},
    {"lat_offset": 7, "lon_offset": 0},
]

SEVEN = [
    {"lat_offset": 0, "lon_offset": 4},
    {"lat_offset": 21, "lon_offset": 13},
    {"lat_offset": 21, "lon_offset": 0},
]

EIGHT = [
    {"lat_offset": 21, "lon_offset": 5},
    {"lat_offset": 20, "lon_offset": 2},
    {"lat_offset": 18, "lon_offset": 1},
    {"lat_offset": 16, "lon_offset": 1},
    {"lat_offset": 14, "lon_offset": 2},
    {"lat_offset": 13, "lon_offset": 4},
    {"lat_offset": 12, "lon_offset": 7},
    {"lat_offset": 11, "lon_offset": 10},
    {"lat_offset": 9, "lon_offset": 12},
    {"lat_offset": 7, "lon_offset": 13},
    {"lat_offset": 4, "lon_offset": 13},
    {"lat_offset": 2, "lon_offset": 12},
    {"lat_offset": 1, "lon_offset": 11},
    {"lat_offset": 0, "lon_offset": 8},
    {"lat_offset": 0, "lon_offset": 5},
    {"lat_offset": 1, "lon_offset": 2},
    {"lat_offset": 2, "lon_offset": 1},
    {"lat_offset": 4, "lon_offset": 0},
    {"lat_offset": 7, "lon_offset": 0},
    {"lat_offset": 9, "lon_offset": 1},
    {"lat_offset": 11, "lon_offset": 3},
    {"lat_offset": 12, "lon_offset": 6},
    {"lat_offset": 13, "lon_offset": 9},
    {"lat_offset": 14, "lon_offset": 11},
    {"lat_offset": 16, "lon_offset": 12},
    {"lat_offset": 18, "lon_offset": 12},
    {"lat_offset": 20, "lon_offset": 11},
    {"lat_offset": 21, "lon_offset": 8},
    {"lat_offset": 21, "lon_offset": 5},
]

NINE = [
    {"lat_offset": 14, "lon_offset": 13},
    {"lat_offset": 11, "lon_offset": 12},
    {"lat_offset": 9, "lon_offset": 10},
    {"lat_offset": 8, "lon_offset": 7},
    {"lat_offset": 8, "lon_offset": 6},
    {"lat_offset": 9, "lon_offset": 3},
    {"lat_offset": 11, "lon_offset": 1},
    {"lat_offset": 14, "lon_offset": 0},
    {"lat_offset": 15, "lon_offset": 0},
    {"lat_offset": 18, "lon_offset": 1},
    {"lat_offset": 20, "lon_offset": 3},
    {"lat_offset": 21, "lon_offset": 6},
    {"lat_offset": 21, "lon_offset": 7},
    {"lat_offset": 20, "lon_offset": 10},
    {"lat_offset": 18, "lon_offset": 12},
    {"lat_offset": 14, "lon_offset": 13},
    {"lat_offset": 9, "lon_offset": 13},
    {"lat_offset": 4, "lon_offset": 12},
    {"lat_offset": 1, "lon_offset": 10},
    {"lat_offset": 0, "lon_offset": 7},
    {"lat_offset": 0, "lon_offset": 5},
    {"lat_offset": 1, "lon_offset": 2},
    {"lat_offset": 3, "lon_offset": 1},
]

AA = [
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 7, "lon_offset": 2},
    {"lat_offset": 21, "lon_offset": 6},
    {"lat_offset": 21, "lon_offset": 7},
    {"lat_offset": 7, "lon_offset": 11},
    {"lat_offset": 0, "lon_offset": 13},
    {"lat_offset": 7, "lon_offset": 11},
    {"lat_offset": 7, "lon_offset": 2},
]

BB = [
    {"lat_offset": 11, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": 9},
    {"lat_offset": 10, "lon_offset": 11},
    {"lat_offset": 6, "lon_offset": 13},
    {"lat_offset": 5, "lon_offset": 13},
    {"lat_offset": 1, "lon_offset": 11},
    {"lat_offset": 0, "lon_offset": 9},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 9},
    {"lat_offset": 20, "lon_offset": 11},
    {"lat_offset": 17, "lon_offset": 13},
    {"lat_offset": 16, "lon_offset": 13},
    {"lat_offset": 12, "lon_offset": 11},
    {"lat_offset": 11, "lon_offset": 9},
]

CC = [
    {"lat_offset": 1, "lon_offset": 13},
    {"lat_offset": 0, "lon_offset": 10},
    {"lat_offset": 0, "lon_offset": 7},
    {"lat_offset": 1, "lon_offset": 4},
    {"lat_offset": 4, "lon_offset": 1},
    {"lat_offset": 9, "lon_offset": 0},
    {"lat_offset": 13, "lon_offset": 0},
    {"lat_offset": 18, "lon_offset": 1},
    {"lat_offset": 20, "lon_offset": 4},
    {"lat_offset": 21, "lon_offset": 7},
    {"lat_offset": 21, "lon_offset": 10},
    {"lat_offset": 20, "lon_offset": 13},
]

DD = [
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 6},
    {"lat_offset": 1, "lon_offset": 9},
    {"lat_offset": 4, "lon_offset": 12},
    {"lat_offset": 9, "lon_offset": 13},
    {"lat_offset": 13, "lon_offset": 13},
    {"lat_offset": 18, "lon_offset": 12},
    {"lat_offset": 20, "lon_offset": 9},
    {"lat_offset": 21, "lon_offset": 6},
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 0},
]

EE = [
    {"lat_offset": 21, "lon_offset": 13},
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 12, "lon_offset": 0},
    {"lat_offset": 12, "lon_offset": 8},
    {"lat_offset": 12, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 13},
]

FF = [
    {"lat_offset": 21, "lon_offset": 13},
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 12, "lon_offset": 0},
    {"lat_offset": 12, "lon_offset": 8},
    {"lat_offset": 12, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 0},
]

GG = [
    {"lat_offset": 20, "lon_offset": 13},
    {"lat_offset": 21, "lon_offset": 10},
    {"lat_offset": 21, "lon_offset": 7},
    {"lat_offset": 20, "lon_offset": 4},
    {"lat_offset": 18, "lon_offset": 1},
    {"lat_offset": 13, "lon_offset": 0},
    {"lat_offset": 9, "lon_offset": 0},
    {"lat_offset": 4, "lon_offset": 1},
    {"lat_offset": 1, "lon_offset": 4},
    {"lat_offset": 0, "lon_offset": 7},
    {"lat_offset": 0, "lon_offset": 10},
    {"lat_offset": 1, "lon_offset": 13},
    {"lat_offset": 10, "lon_offset": 13},
    {"lat_offset": 10, "lon_offset": 10},
]

HH = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 12, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 12, "lon_offset": 0},
    {"lat_offset": 12, "lon_offset": 13},
    {"lat_offset": 0, "lon_offset": 13},
    {"lat_offset": 12, "lon_offset": 13},
    {"lat_offset": 21, "lon_offset": 13},
]

II = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 5},
    {"lat_offset": 21, "lon_offset": 10},
    {"lat_offset": 21, "lon_offset": 5},
    {"lat_offset": 0, "lon_offset": 5},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 5},
    {"lat_offset": 0, "lon_offset": 10},
]

JJ = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 9},
    {"lat_offset": 21, "lon_offset": 13},
    {"lat_offset": 21, "lon_offset": 9},
    {"lat_offset": 3, "lon_offset": 9},
    {"lat_offset": 1, "lon_offset": 8},
    {"lat_offset": 0, "lon_offset": 6},
    {"lat_offset": 0, "lon_offset": 3},
    {"lat_offset": 1, "lon_offset": 1},
    {"lat_offset": 3, "lon_offset": 0},
]

KK = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": 0},
    {"lat_offset": 13, "lon_offset": 3},
    {"lat_offset": 21, "lon_offset": 10},
    {"lat_offset": 13, "lon_offset": 3},
    {"lat_offset": 0, "lon_offset": 13},
]

LL = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 14},
]

MM = [
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 1},
    {"lat_offset": 13, "lon_offset": 6},
    {"lat_offset": 13, "lon_offset": 7},
    {"lat_offset": 21, "lon_offset": 12},
    {"lat_offset": 21, "lon_offset": 13},
    {"lat_offset": 0, "lon_offset": 13},
]

NN = [
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 1},
    {"lat_offset": 0, "lon_offset": 12},
    {"lat_offset": 0, "lon_offset": 13},
    {"lat_offset": 21, "lon_offset": 13},
]

OO = [
    {"lat_offset": 4, "lon_offset": 1},
    {"lat_offset": 1, "lon_offset": 3},
    {"lat_offset": 0, "lon_offset": 6},
    {"lat_offset": 0, "lon_offset": 8},
    {"lat_offset": 1, "lon_offset": 11},
    {"lat_offset": 4, "lon_offset": 13},
    {"lat_offset": 9, "lon_offset": 14},
    {"lat_offset": 12, "lon_offset": 14},
    {"lat_offset": 17, "lon_offset": 13},
    {"lat_offset": 20, "lon_offset": 11},
    {"lat_offset": 21, "lon_offset": 8},
    {"lat_offset": 21, "lon_offset": 6},
    {"lat_offset": 20, "lon_offset": 3},
    {"lat_offset": 17, "lon_offset": 1},
    {"lat_offset": 12, "lon_offset": 0},
    {"lat_offset": 9, "lon_offset": 0},
    {"lat_offset": 4, "lon_offset": 1},
]

PP = [
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 9},
    {"lat_offset": 20, "lon_offset": 11},
    {"lat_offset": 17, "lon_offset": 13},
    {"lat_offset": 16, "lon_offset": 13},
    {"lat_offset": 12, "lon_offset": 11},
    {"lat_offset": 11, "lon_offset": 9},
    {"lat_offset": 11, "lon_offset": 0},
]

QQ = [
    {"lat_offset": 1, "lon_offset": 11},
    {"lat_offset": 4, "lon_offset": 13},
    {"lat_offset": 9, "lon_offset": 14},
    {"lat_offset": 12, "lon_offset": 14},
    {"lat_offset": 17, "lon_offset": 13},
    {"lat_offset": 20, "lon_offset": 11},
    {"lat_offset": 21, "lon_offset": 8},
    {"lat_offset": 21, "lon_offset": 6},
    {"lat_offset": 20, "lon_offset": 3},
    {"lat_offset": 17, "lon_offset": 1},
    {"lat_offset": 12, "lon_offset": 0},
    {"lat_offset": 9, "lon_offset": 0},
    {"lat_offset": 4, "lon_offset": 1},
    {"lat_offset": 1, "lon_offset": 3},
    {"lat_offset": 0, "lon_offset": 6},
    {"lat_offset": 0, "lon_offset": 8},
    {"lat_offset": 1, "lon_offset": 11},
    {"lat_offset": 4, "lon_offset": 8},
    {"lat_offset": 1, "lon_offset": 11},
    {"lat_offset": 0, "lon_offset": 12},
]

RR = [
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 9},
    {"lat_offset": 20, "lon_offset": 11},
    {"lat_offset": 17, "lon_offset": 13},
    {"lat_offset": 16, "lon_offset": 13},
    {"lat_offset": 12, "lon_offset": 11},
    {"lat_offset": 11, "lon_offset": 9},
    {"lat_offset": 11, "lon_offset": 0},
    {"lat_offset": 11, "lon_offset": 9},
    {"lat_offset": 0, "lon_offset": 13},
]

SS = [
    {"lat_offset": 17, "lon_offset": 12},
    {"lat_offset": 19, "lon_offset": 11},
    {"lat_offset": 20, "lon_offset": 10},
    {"lat_offset": 21, "lon_offset": 8},
    {"lat_offset": 21, "lon_offset": 4},
    {"lat_offset": 20, "lon_offset": 2},
    {"lat_offset": 19, "lon_offset": 1},
    {"lat_offset": 17, "lon_offset": 0},
    {"lat_offset": 15, "lon_offset": 0},
    {"lat_offset": 13, "lon_offset": 1},
    {"lat_offset": 11, "lon_offset": 6},
    {"lat_offset": 8, "lon_offset": 11},
    {"lat_offset": 6, "lon_offset": 12},
    {"lat_offset": 4, "lon_offset": 12},
    {"lat_offset": 2, "lon_offset": 11},
    {"lat_offset": 1, "lon_offset": 10},
    {"lat_offset": 0, "lon_offset": 8},
    {"lat_offset": 0, "lon_offset": 4},
    {"lat_offset": 1, "lon_offset": 2},
    {"lat_offset": 2, "lon_offset": 1},
    {"lat_offset": 4, "lon_offset": 0},
]

TT = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 7},
    {"lat_offset": 21, "lon_offset": 14},
    {"lat_offset": 21, "lon_offset": 7},
    {"lat_offset": 0, "lon_offset": 7},
]

UU = [
    {"lat_offset": 21, "lon_offset": 12},
    {"lat_offset": 4, "lon_offset": 12},
    {"lat_offset": 2, "lon_offset": 11},
    {"lat_offset": 1, "lon_offset": 10},
    {"lat_offset": 0, "lon_offset": 8},
    {"lat_offset": 0, "lon_offset": 4},
    {"lat_offset": 1, "lon_offset": 2},
    {"lat_offset": 2, "lon_offset": 1},
    {"lat_offset": 4, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 0},
]

VV = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 6},
    {"lat_offset": 21, "lon_offset": 12},
]

WW = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 1},
    {"lat_offset": 8, "lon_offset": 6},
    {"lat_offset": 8, "lon_offset": 7},
    {"lat_offset": 0, "lon_offset": 12},
    {"lat_offset": 0, "lon_offset": 13},
    {"lat_offset": 21, "lon_offset": 13},
]

XX = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 10, "lon_offset": 7},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 10, "lon_offset": 7},
    {"lat_offset": 0, "lon_offset": 14},
    {"lat_offset": 10, "lon_offset": 7},
    {"lat_offset": 21, "lon_offset": 14},
]

YY = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 10, "lon_offset": 7},
    {"lat_offset": 0, "lon_offset": 7},
    {"lat_offset": 10, "lon_offset": 7},
    {"lat_offset": 21, "lon_offset": 14},
]

ZZ = [
    {"lat_offset": 21, "lon_offset": 0},
    {"lat_offset": 21, "lon_offset": 14},
    {"lat_offset": 0, "lon_offset": 0},
    {"lat_offset": 0, "lon_offset": 14},
]


def get_plot_from_char(text_value: str) -> list[list]:
    upper_value = text_value.capitalize()
    if upper_value == " ":
        return SPACE
    if upper_value == ".":
        return DOT
    if upper_value == "-":
        return MINUS
    if upper_value == "+":
        return PLUS
    if upper_value == "0":
        return ZERO
    if upper_value == "1":
        return ONE
    if upper_value == "2":
        return TWO
    if upper_value == "3":
        return THREE
    if upper_value == "4":
        return FOUR
    if upper_value == "5":
        return FIVE
    if upper_value == "6":
        return SIX
    if upper_value == "7":
        return SEVEN
    if upper_value == "8":
        return EIGHT
    if upper_value == "9":
        return NINE
    if upper_value == "A":
        return AA
    if upper_value == "B":
        return BB
    if upper_value == "C":
        return CC
    if upper_value == "D":
        return DD
    if upper_value == "E":
        return EE
    if upper_value == "F":
        return FF
    if upper_value == "G":
        return GG
    if upper_value == "H":
        return HH
    if upper_value == "I":
        return II
    if upper_value == "J":
        return JJ
    if upper_value == "K":
        return KK
    if upper_value == "L":
        return LL
    if upper_value == "M":
        return MM
    if upper_value == "N":
        return NN
    if upper_value == "O":
        return OO
    if upper_value == "P":
        return PP
    if upper_value == "Q":
        return QQ
    if upper_value == "R":
        return RR
    if upper_value == "S":
        return SS
    if upper_value == "T":
        return TT
    if upper_value == "U":
        return UU
    if upper_value == "V":
        return VV
    if upper_value == "W":
        return WW
    if upper_value == "X":
        return XX
    if upper_value == "Y":
        return YY
    if upper_value == "Z":
        return ZZ
    return UNRECOGNIZED
