class AirspaceRecord:
    def __init__(
        self,
        multiple_code: str,
        boundary_via: str,
        lat: float,
        lon: float,
        arc_lat: float,
        arc_lon: float,
        arc_dist: float,
    ):
        self.multiple_code = multiple_code
        self.boundary_via = boundary_via
        self.boundary_type = boundary_via[:1]
        self.end_marker = boundary_via[1:]
        self.lat = lat
        self.lon = lon
        self.arc_lat = arc_lat
        self.arc_lon = arc_lon
        self.arc_dist = arc_dist

    def __repr__(self):
        return f"AirspaceRecord(multiple_code={self.multiple_code}, boundary_via={self.boundary_via}, boundary_type={self.boundary_type}, end_marker={self.end_marker}, lat={self.lat}, lon={self.lon}, arc_lat={self.arc_lat}, arc_lon={self.arc_lon}, arc_dist={self.arc_dist})"

    def get_line_definition(self):
        return self
