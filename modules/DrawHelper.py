import math

ARC_MIN = 0.015  # 1 min of arc = 1/60, most facilities round this down to 0.015 resulting in 0.9nm tall letters
DEG_TO_MIN = 60
EARTH_RADIUS_NM = 3443.92


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


def latLonFromPBD(lat: float, lon: float, bearing: float, distance: float) -> dict:
    lat = math.radians(lat)
    lon = math.radians(lon)
    bearing = math.radians(bearing)
    endLat = math.asin(
        math.sin(lat) * math.cos(distance / EARTH_RADIUS_NM)
        + math.cos(lat) * math.sin(distance / EARTH_RADIUS_NM) * math.cos(bearing)
    )
    endLon = lon + math.atan2(
        math.sin(bearing) * math.sin(distance / EARTH_RADIUS_NM) * math.cos(lat),
        math.cos(distance / EARTH_RADIUS_NM) - math.sin(lat) * math.sin(endLat),
    )

    endLat = math.degrees(endLat)
    endLon = math.degrees(endLon)

    result = {"lat": endLat, "lon": endLon}
    return result


def haversineGreatCircleDistance(
    startLat: float, startLon: float, endLat: float, endLon: float
) -> float:
    theta = startLon - endLon
    arc = math.degrees(
        math.acos(
            (math.sin(math.radians(startLat)) * math.sin(math.radians(endLat)))
            + (
                math.cos(math.radians(startLat))
                * math.cos(math.radians(endLat))
                * math.cos(math.radians(theta))
            )
        )
    )
    distance = arc * DEG_TO_MIN
    return distance


def inverseBearing(bearing: float) -> float:
    result = math.fmod(bearing + 180, 360)
    return result


def haversineGreatCircleBearing(
    startLat: float, startLon: float, endLat: float, endLon: float
) -> float:
    x = math.cos(math.radians(startLat)) * math.sin(math.radians(endLat)) - math.sin(
        math.radians(startLat)
    ) * math.cos(math.radians(endLat)) * math.cos(math.radians(endLon - startLon))
    y = math.sin(math.radians(endLon - startLon)) * math.cos(math.radians(endLat))
    bearing = math.degrees(math.atan2(y, x))
    bearing = math.fmod(bearing + 360, 360)
    return bearing
