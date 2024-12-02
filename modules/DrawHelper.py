import math

ARC_MIN = 0.015  # 1 min of arc = 1/60, most facilities round this down to 0.015 resulting in 0.9nm tall letters
DEG_TO_MIN = 60
EARTH_RADIUS_NM = 3443.92


def correction_factor(latitude: float) -> float:
    latitude_radians = math.radians(latitude)
    result = math.cos(latitude_radians)
    return result


def correct_offsets(
    center_lat: float,
    center_lon: float,
    offsets: list[dict],
    plot_height: int,
    plot_width: int,
    rotation_deg: float = 0.0,
    scale_factor: float = 1.0,
) -> list[dict]:
    scale = scale_factor * ARC_MIN
    lon_correction_factor = correction_factor(center_lat)
    rotation_rad = math.radians(rotation_deg)

    cos_theta = math.cos(rotation_rad)
    sin_theta = math.sin(rotation_rad)

    result = []
    for offset in offsets:
        rotated_lat_offset = (
            offset["lat_offset"] * cos_theta - offset["lon_offset"] * sin_theta
        )
        rotated_lon_offset = (
            offset["lat_offset"] * sin_theta + offset["lon_offset"] * cos_theta
        )
        adjusted_lat = (rotated_lat_offset / plot_height) * scale
        adjusted_lat += center_lat
        adjusted_lon = (
            (rotated_lon_offset / plot_width) * scale
        ) / lon_correction_factor
        adjusted_lon += center_lon
        result.append({"lat": adjusted_lat, "lon": adjusted_lon})
    return result


def lat_lon_from_pbd(lat: float, lon: float, bearing: float, distance: float) -> dict:
    lat = math.radians(lat)
    lon = math.radians(lon)
    bearing = math.radians(bearing)
    end_lat = math.asin(
        math.sin(lat) * math.cos(distance / EARTH_RADIUS_NM)
        + math.cos(lat) * math.sin(distance / EARTH_RADIUS_NM) * math.cos(bearing)
    )
    end_lon = lon + math.atan2(
        math.sin(bearing) * math.sin(distance / EARTH_RADIUS_NM) * math.cos(lat),
        math.cos(distance / EARTH_RADIUS_NM) - math.sin(lat) * math.sin(end_lat),
    )

    end_lat = math.degrees(end_lat)
    end_lon = math.degrees(end_lon)

    result = {"lat": end_lat, "lon": end_lon}
    return result


def haversine_great_circle_distance(
    start_lat: float, start_lon: float, end_lat: float, end_lon: float
) -> float:
    theta = start_lon - end_lon
    arc = math.degrees(
        math.acos(
            (math.sin(math.radians(start_lat)) * math.sin(math.radians(end_lat)))
            + (
                math.cos(math.radians(start_lat))
                * math.cos(math.radians(end_lat))
                * math.cos(math.radians(theta))
            )
        )
    )
    distance = arc * DEG_TO_MIN
    return distance


def inverse_bearing(bearing: float) -> float:
    result = math.fmod(bearing + 180, 360)
    return result


def haversine_great_circle_bearing(
    start_lat: float, start_lon: float, end_lat: float, end_lon: float
) -> float:
    x = math.cos(math.radians(start_lat)) * math.sin(math.radians(end_lat)) - math.sin(
        math.radians(start_lat)
    ) * math.cos(math.radians(end_lat)) * math.cos(math.radians(end_lon - start_lon))
    y = math.sin(math.radians(end_lon - start_lon)) * math.cos(math.radians(end_lat))
    bearing = math.degrees(math.atan2(y, x))
    bearing = math.fmod(bearing + 360, 360)
    return bearing
