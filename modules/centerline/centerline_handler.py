from modules.draw import lat_lon_from_pbd
from modules.geo_json import LineString
from modules.draw.draw_handler import draw_dashed_line


def get_line_strings(
    initial_lat: float,
    initial_lon: float,
    bearing: float,
    length: float,
) -> list[LineString]:
    end_coordinate = lat_lon_from_pbd(initial_lat, initial_lon, bearing, length)

    list_list_coord = draw_dashed_line(
        initial_lat,
        initial_lon,
        end_coordinate.get("lat"),
        end_coordinate.get("lon"),
        shift=True,
    )

    result = []
    for item in list_list_coord:
        line_string = LineString()
        line_string.add_coordinates(item)
        result.append(line_string)

    return result
