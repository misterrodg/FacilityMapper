class AirspaceRecord:
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
        self.mult_code: str = mult_code
        self.boundary_via: str = boundary_via
        self.boundary_type: str = boundary_via[:1]
        self.end_marker: str = boundary_via[1:]
        self.lat: float = lat
        self.lon: float = lon
        self.arc_lat: float = arc_lat
        self.arc_lon: float = arc_lon
        self.arc_dist: float = arc_dist

    def __repr__(self):
        return f"AirspaceRecord(mult_code={self.mult_code}, boundary_via={self.boundary_via}, boundary_type={self.boundary_type}, end_marker={self.end_marker}, lat={self.lat}, lon={self.lon}, arc_lat={self.arc_lat}, arc_lon={self.arc_lon}, arc_dist={self.arc_dist})"

    def get_line_definition(self):
        return self
