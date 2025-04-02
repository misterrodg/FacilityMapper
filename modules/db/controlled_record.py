from modules.db.airspace_record import AirspaceRecord


class ControlledRecord(AirspaceRecord):
    SEGMENT_FIELD = "multiple_code"

    def __init__(self, db_record: dict):
        self.area: str = db_record.get("area")
        self.sec_code: str = db_record.get("sec_code")
        self.sub_code: str = db_record.get("sub_code")
        self.region: str = db_record.get("region")
        self.airspace_type: str = db_record.get("airspace_type")
        self.center_id: str = db_record.get("center_id")
        self.center_sec_code: str = db_record.get("center_sec_code")
        self.center_sub_code: str = db_record.get("center_sub_code")
        self.airspace_class: str = db_record.get("airspace_class")
        self.multiple_code: str = db_record.get("multiple_code")
        self.sequence_number: int = db_record.get("sequence_number")
        self.level: str = db_record.get("level")
        self.time_zone: str = db_record.get("time_zone")
        self.notam: str = db_record.get("notam")
        self.boundary_via: str = db_record.get("boundary_via")
        self.lat: float = db_record.get("lat")
        self.lon: float = db_record.get("lon")
        self.arc_lat: float = db_record.get("arc_lat")
        self.arc_lon: float = db_record.get("arc_lon")
        self.arc_dist: float = db_record.get("arc_dist")
        self.arc_bearing: float = db_record.get("arc_bearing")
        self.rnp: float = db_record.get("rnp")
        self.lower_limit: str = db_record.get("lower_limit")
        self.lower_unit: str = db_record.get("lower_unit")
        self.upper_limit: str = db_record.get("upper_limit")
        self.upper_unit: str = db_record.get("upper_unit")
        self.airspace_name: str = db_record.get("airspace_name")
        self.record_number: int = db_record.get("record_number")
        self.cycle_data: str = db_record.get("cycle_data")

        super().__init__(
            self.multiple_code,
            self.boundary_via,
            self.lat,
            self.lon,
            self.arc_lat,
            self.arc_lon,
            self.arc_dist,
        )
