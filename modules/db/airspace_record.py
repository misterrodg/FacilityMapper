class AirspaceRecord:
    mult_code: str | None
    boundary_via: str | None
    boundary_type: str | None
    end_marker: str | None
    lat: float | None
    lon: float | None
    arc_lat: float | None
    arc_lon: float | None
    arc_dist: float | None

    def __init__(
        self,
        mult_code: str,
        boundary_via: str,
        lat: float,
        lon: float,
        arc_lat: float,
        arc_lon: float,
        arc_dist: float,
    ):
        self.mult_code = mult_code
        self.boundary_via = boundary_via
        self.boundary_type = boundary_via[:1]
        self.end_marker = boundary_via[1:]
        self.lat = lat
        self.lon = lon
        self.arc_lat = arc_lat
        self.arc_lon = arc_lon
        self.arc_dist = arc_dist

    def __repr__(self):
        return f"AirspaceRecord(mult_code={self.mult_code}, boundary_via={self.boundary_via}, boundary_type={self.boundary_type}, end_marker={self.end_marker}, lat={self.lat}, lon={self.lon}, arc_lat={self.arc_lat}, arc_lon={self.arc_lon}, arc_dist={self.arc_dist})"

    def get_line_definition(self):
        return self
