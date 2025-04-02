from modules.draw_helper import (
    FEET_IN_NM,
    haversine_great_circle_bearing,
    inverse_bearing,
    lat_lon_from_pbd,
)


class RunwayPair:
    def __init__(
        self,
        airport_id: str,
        base_id: str,
        base_lat: float,
        base_lon: float,
        base_displaced: int,
        reciprocal_id: str,
        reciprocal_lat: float,
        reciprocal_lon: float,
        reciprocal_displaced: int,
    ):
        self.airport_id: str = airport_id
        self.base_id: str = base_id
        self.base_lat: float = None
        self.base_lon: float = None
        self.base_displaced: int = base_displaced
        self.base_bearing: float = None
        self.base_displaced_lat: float = base_lat
        self.base_displaced_lon: float = base_lon
        self.reciprocal_id: str = reciprocal_id
        self.reciprocal_lat: float = None
        self.reciprocal_lon: float = None
        self.reciprocal_displaced: int = reciprocal_displaced
        self.reciprocal_bearing: float = None
        self.reciprocal_displaced_lat: float = reciprocal_lat
        self.reciprocal_displaced_lon: float = reciprocal_lon
        self.is_valid: bool = False

        self._validate()

        if self.is_valid:
            self._process()

    def _validate(self) -> None:
        if (
            self.base_id
            and self.base_displaced_lat
            and self.base_displaced_lon
            and self.reciprocal_id
            and self.reciprocal_displaced_lat
            and self.reciprocal_displaced_lon
        ):
            self.is_valid = True

    def _process(self) -> None:
        self.base_bearing = haversine_great_circle_bearing(
            self.base_displaced_lat,
            self.base_displaced_lon,
            self.reciprocal_displaced_lat,
            self.reciprocal_displaced_lon,
        )
        self.reciprocal_bearing = inverse_bearing(self.base_bearing)

        if self.base_displaced > 0:
            new_base = lat_lon_from_pbd(
                self.base_displaced_lat,
                self.base_displaced_lon,
                self.reciprocal_bearing,
                self.base_displaced / FEET_IN_NM,
            )
            self.base_lat = new_base["lat"]
            self.base_lon = new_base["lon"]
        else:
            self.base_lat = self.base_displaced_lat
            self.base_lon = self.base_displaced_lon

        if self.reciprocal_displaced > 0:
            new_reciprocal = lat_lon_from_pbd(
                self.reciprocal_displaced_lat,
                self.reciprocal_displaced_lon,
                self.base_bearing,
                self.reciprocal_displaced / FEET_IN_NM,
            )
            self.reciprocal_lat = new_reciprocal["lat"]
            self.reciprocal_lon = new_reciprocal["lon"]
        else:
            self.reciprocal_lat = self.reciprocal_displaced_lat
            self.reciprocal_lon = self.reciprocal_displaced_lon
