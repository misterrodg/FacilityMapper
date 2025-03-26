from modules.db.airspace_record import AirspaceRecord


class RestrictiveRecord(AirspaceRecord):
    SEGMENT_FIELDS = ["multiple_code"]

    def __init__(self, db_record: dict):
        self.area = db_record.get("area")
        self.sec_code = db_record.get("sec_code")
        self.sub_code = db_record.get("sub_code")
        self.region = db_record.get("region")
        self.restrictive_type = db_record.get("restrictive_type")
        self.restrictive_designation = db_record.get("restrictive_designation")
        self.multiple_code = db_record.get("multiple_code")
        self.sequence_number = db_record.get("sequence_number")
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
            self.multiple_code,
            self.boundary_via,
            self.lat,
            self.lon,
            self.arc_lat,
            self.arc_lon,
            self.arc_dist,
        )
