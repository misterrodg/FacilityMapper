from modules.db.airspace_record import AirspaceRecord


class RestrictiveRecord(AirspaceRecord):
    SEGMENT_FIELD = "mult_code"

    st: str | None
    area: str | None
    sec_code: str | None
    sub_code: str | None
    region: str | None
    restrictive_type: str | None
    restrictive_id: str | None
    mult_code: str | None
    seq_no: int | None
    cont_rec_no: int | None
    level: str | None
    time_zone: str | None
    notam: str | None
    boundary_via: str | None
    lat: float | None
    lon: float | None
    arc_lat: float | None
    arc_lon: float | None
    arc_dist: float | None
    arc_bearing: float | None
    lower_limit: str | None
    lower_unit: str | None
    upper_limit: str | None
    upper_unit: str | None
    restrictive_name: str | None
    record_number: int | None
    cycle_data: str | None

    def __init__(self, db_record: dict):
        self.st = db_record.get("st")
        self.area = db_record.get("area")
        self.sec_code = db_record.get("sec_code")
        self.sub_code = db_record.get("sub_code")
        self.region = db_record.get("region")
        self.restrictive_type = db_record.get("restrictive_type")
        self.restrictive_id = db_record.get("restrictive_id")
        self.mult_code = db_record.get("mult_code")
        self.seq_no = db_record.get("seq_no")
        self.cont_rec_no = db_record.get("cont_rec_no")
        self.level = db_record.get("level")
        self.time_zone = db_record.get("time_zone")
        self.notam = db_record.get("notam")
        self.boundary_via = db_record.get("boundary_via")
        self.lat = db_record.get("lat")
        self.lon = db_record.get("lon")
        self.arc_lat = db_record.get("arc_lat")
        self.arc_lon = db_record.get("arc_lon")
        self.arc_dist = db_record.get("arc_dist")
        self.arc_bearing = db_record.get("arc_bearing")
        self.lower_limit = db_record.get("lower_limit")
        self.lower_unit = db_record.get("lower_unit")
        self.upper_limit = db_record.get("upper_limit")
        self.upper_unit = db_record.get("upper_unit")
        self.restrictive_name = db_record.get("restrictive_name")
        self.record_number = db_record.get("record_number")
        self.cycle_data = db_record.get("cycle_data")

        super().__init__(
            self.mult_code,
            self.boundary_via,
            self.lat,
            self.lon,
            self.arc_lat,
            self.arc_lon,
            self.arc_dist,
        )
