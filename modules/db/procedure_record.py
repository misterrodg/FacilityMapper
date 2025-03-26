class ProcedureRecord:
    SEGMENT_FIELDS = ["transition_id"]

    def __init__(self, db_record: dict):
        self.area = db_record.get("area")
        self.sec_code = db_record.get("sec_code")
        self.fac_id = db_record.get("fac_id")
        self.fac_region = db_record.get("fac_region")
        self.fac_sub_code = db_record.get("fac_sub_code")
        self.procedure_id = db_record.get("procedure_id")
        self.route_type = db_record.get("route_type")
        self.transition_id = db_record.get("transition_id")
        self.sequence_number = db_record.get("sequence_number")
        self.fix_id = db_record.get("fix_id")
        self.fix_region = db_record.get("fix_region")
        self.fix_sec_code = db_record.get("fix_sec_code")
        self.fix_sub_code = db_record.get("fix_sub_code")
        self.description_code = db_record.get("description_code")
        self.turn_direction = db_record.get("turn_direction")
        self.rnp = db_record.get("rnp")
        self.path_term = db_record.get("path_term")
        self.tdv = db_record.get("tdv")
        self.rec_vhf = db_record.get("rec_vhf")
        self.rec_vhf_region = db_record.get("rec_vhf_region")
        self.arc_radius = db_record.get("arc_radius")
        self.theta = db_record.get("theta")
        self.rho = db_record.get("rho")
        self.course = db_record.get("course")
        self.dist = db_record.get("dist")
        self.time = db_record.get("time")
        self.rec_vhf_sec_code = db_record.get("rec_vhf_sec_code")
        self.rec_vhf_sub_code = db_record.get("rec_vhf_sub_code")
        self.alt_desc = db_record.get("alt_desc")
        self.atc = db_record.get("atc")
        self.altitude = db_record.get("altitude")
        self.flight_level = db_record.get("flight_level")
        self.altitude_2 = db_record.get("altitude_2")
        self.flight_level_2 = db_record.get("flight_level_2")
        self.trans_alt = db_record.get("trans_alt")
        self.speed_limit = db_record.get("speed_limit")
        self.vert_angle = db_record.get("vert_angle")
        self.center_fix = db_record.get("center_fix")
        self.multiple_code = db_record.get("multiple_code")
        self.center_fix_region = db_record.get("center_fix_region")
        self.center_fix_sec_code = db_record.get("center_fix_sec_code")
        self.center_fix_sub_code = db_record.get("center_fix_sub_code")
        self.gns_fms_id = db_record.get("gns_fms_id")
        self.speed_limit_2 = db_record.get("speed_limit_2")
        self.rte_qual_1 = db_record.get("rte_qual_1")
        self.rte_qual_2 = db_record.get("rte_qual_2")
        self.record_number = db_record.get("record_number")
        self.cycle_data = db_record.get("cycle_data")


class JoinedProcedureRecord(ProcedureRecord):
    def __init__(self, db_record: dict):
        super().__init__(db_record)
        self.id = db_record.get("id")
        self.lat = db_record.get("lat")
        self.lon = db_record.get("lon")
        self.type = db_record.get("type")
