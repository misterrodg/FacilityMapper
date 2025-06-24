from modules.db.airspace_record import AirspaceRecord


class ControlledRecord(AirspaceRecord):
    SEGMENT_FIELD = "mult_code"

    st: str | None
    area: str | None
    sec_code: str | None
    sub_code: str | None
    center_region: str | None
    airspace_type: str | None
    center_id: str | None
    center_sec_code: str | None
    center_sub_code: str | None
    airspace_class: str | None
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
    rnp: float | None
    lower_limit: str | None
    lower_unit: str | None
    upper_limit: str | None
    upper_unit: str | None
    airspace_name: str | None
    record_number: int | None
    cycle_data: str | None

    def __init__(self, db_record: dict):
        self.st = db_record.get("st")
        self.area = db_record.get("area")
        self.sec_code = db_record.get("sec_code")
        self.sub_code = db_record.get("sub_code")
        self.center_region = db_record.get("center_region")
        self.airspace_type = db_record.get("airspace_type")
        self.center_id = db_record.get("center_id")
        self.center_sec_code = db_record.get("center_sec_code")
        self.center_sub_code = db_record.get("center_sub_code")
        self.airspace_class = db_record.get("airspace_class")
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
        self.rnp = db_record.get("rnp")
        self.lower_limit = db_record.get("lower_limit")
        self.lower_unit = db_record.get("lower_unit")
        self.upper_limit = db_record.get("upper_limit")
        self.upper_unit = db_record.get("upper_unit")
        self.airspace_name = db_record.get("airspace_name")
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
