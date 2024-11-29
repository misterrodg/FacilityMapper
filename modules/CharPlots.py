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


def getPlotWidth(charPlot: list[list]) -> int:
    result = 0
    for line in charPlot:
        width = line[1]
        if width > result:
            result = width
    return result


def get_plot_from_char(textValue: str) -> list[list]:
    upperValue = textValue.capitalize()
    if upperValue == " ":
        return SPACE
    if upperValue == ".":
        return DOT
    if upperValue == "-":
        return MINUS
    if upperValue == "+":
        return PLUS
    if upperValue == "0":
        return ZERO
    if upperValue == "1":
        return ONE
    if upperValue == "2":
        return TWO
    if upperValue == "3":
        return THREE
    if upperValue == "4":
        return FOUR
    if upperValue == "5":
        return FIVE
    if upperValue == "6":
        return SIX
    if upperValue == "7":
        return SEVEN
    if upperValue == "8":
        return EIGHT
    if upperValue == "9":
        return NINE
    if upperValue == "A":
        return AA
    if upperValue == "B":
        return BB
    if upperValue == "C":
        return CC
    if upperValue == "D":
        return DD
    if upperValue == "E":
        return EE
    if upperValue == "F":
        return FF
    if upperValue == "G":
        return GG
    if upperValue == "H":
        return HH
    if upperValue == "I":
        return II
    if upperValue == "J":
        return JJ
    if upperValue == "K":
        return KK
    if upperValue == "L":
        return LL
    if upperValue == "M":
        return MM
    if upperValue == "N":
        return NN
    if upperValue == "O":
        return OO
    if upperValue == "P":
        return PP
    if upperValue == "Q":
        return QQ
    if upperValue == "R":
        return RR
    if upperValue == "S":
        return SS
    if upperValue == "T":
        return TT
    if upperValue == "U":
        return UU
    if upperValue == "V":
        return VV
    if upperValue == "W":
        return WW
    if upperValue == "X":
        return XX
    if upperValue == "Y":
        return YY
    if upperValue == "Z":
        return ZZ
    return UNRECOGNIZED
