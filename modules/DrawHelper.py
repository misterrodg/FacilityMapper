import math

ARC_MIN = 0.015  # 1 min of arc = 1/60, most facilities round this down to 0.015 resulting in 0.9nm tall letters


def correctOffsets(
    centerLat: float,
    centerLon: float,
    offsets: list[dict],
    plotHeight: int,
    plotWidth: int,
    rotationDeg: float = 0.0,
    scaleFactor: float = 1.0,
) -> list[dict]:
    scale = scaleFactor * ARC_MIN
    centerLatRad = math.radians(centerLat)
    lonCorrectionFactor = math.cos(centerLatRad)
    rotationRad = math.radians(rotationDeg)

    cosTheta = math.cos(rotationRad)
    sinTheta = math.sin(rotationRad)

    result = []
    for offset in offsets:
        rotatedLatOffset = (
            offset["lat_offset"] * cosTheta - offset["lon_offset"] * sinTheta
        )
        rotatedLonOffset = (
            offset["lat_offset"] * sinTheta + offset["lon_offset"] * cosTheta
        )
        adjustedLat = (rotatedLatOffset / plotHeight) * scale
        adjustedLat += centerLat
        adjustedLon = ((rotatedLonOffset / plotWidth) * scale) / lonCorrectionFactor
        adjustedLon += centerLon
        result.append({"lat": adjustedLat, "lon": adjustedLon})

    return result
