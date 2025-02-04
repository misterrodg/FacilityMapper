import math

ARC_MIN = 0.015  # 1 min of arc = 1/60, most facilities round this down to 0.015 resulting in 0.9nm tall letters
DEG_TO_MIN = 60
EARTH_RADIUS_NM = 3440.065
FEET_IN_NM = 6076.12


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
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    bearing_rad = math.radians(bearing)
    angular_distance = distance / EARTH_RADIUS_NM
    end_lat_rad = math.asin(
        math.sin(lat_rad) * math.cos(angular_distance)
        + math.cos(lat_rad) * math.sin(angular_distance) * math.cos(bearing_rad)
    )
    end_lon_rad = lon_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(angular_distance) * math.cos(lat_rad),
        math.cos(angular_distance) - math.sin(lat_rad) * math.sin(end_lat_rad),
    )

    end_lat = math.degrees(end_lat_rad)
    end_lon = math.degrees(end_lon_rad)

    end_lon = (end_lon + 180) % 360 - 180

    result = {"lat": end_lat, "lon": end_lon}
    return result


def haversine_great_circle_distance(
    start_lat: float, start_lon: float, end_lat: float, end_lon: float
) -> float:
    start_lat_rad = math.radians(start_lat)
    start_lon_rad = math.radians(start_lon)
    end_lat_rad = math.radians(end_lat)
    end_lon_rad = math.radians(end_lon)

    delta_lon = end_lon_rad - start_lon_rad
    cos_c = math.sin(start_lat_rad) * math.sin(end_lat_rad) + math.cos(
        start_lat_rad
    ) * math.cos(end_lat_rad) * math.cos(delta_lon)
    cos_c = min(1.0, max(-1.0, cos_c))
    angular_distance_rad = math.acos(cos_c)

    distance_nm = angular_distance_rad * EARTH_RADIUS_NM
    return distance_nm


def normalize_bearing(bearing: float) -> float:
    result = math.fmod(bearing + 360, 360)
    return result


def inverse_bearing(bearing: float) -> float:
    result = math.fmod(bearing + 180, 360)
    return result


def haversine_great_circle_bearing(
    start_lat: float, start_lon: float, end_lat: float, end_lon: float
) -> float:
    start_lat_rad = math.radians(start_lat)
    start_lon_rad = math.radians(start_lon)
    end_lat_rad = math.radians(end_lat)
    end_lon_rad = math.radians(end_lon)

    delta_lon = end_lon_rad - start_lon_rad

    x = math.cos(end_lat_rad) * math.sin(delta_lon)
    y = math.cos(start_lat_rad) * math.sin(end_lat_rad) - math.sin(
        start_lat_rad
    ) * math.cos(end_lat_rad) * math.cos(delta_lon)
    bearing_rad = math.atan2(x, y)
    bearing_deg = (math.degrees(bearing_rad) + 360) % 360
    return bearing_deg
