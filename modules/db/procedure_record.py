class ProcedureRecord:
    SEGMENT_FIELD = "transition_id"

    st: str | None
    area: str | None
    sec_code: str | None
    fac_id: str | None
    fac_region: str | None
    fac_sub_code: str | None
    procedure_id: str | None
    procedure_type: str | None
    transition_id: str | None
    seq_no: int | None
    fix_id: str | None
    fix_region: str | None
    fix_sec_code: str | None
    fix_sub_code: str | None
    cont_rec_no: int | None
    desc_code: str | None
    turn_direction: str | None
    rnp: float | None
    path_term: str | None
    tdv: str | None
    rec_vhf: str | None
    rec_vhf_region: str | None
    arc_radius: float | None
    theta: float | None
    rho: float | None
    course: float | None
    dist_time: float | None
    time: float | None
    rec_vhf_sec_code: str | None
    rec_vhf_sub_code: str | None
    alt_desc: str | None
    atc: str | None
    alt_1: int | None
    fl_1: int | None
    alt_2: int | None
    fl_2: int | None
    trans_alt: int | None
    speed_limit: int | None
    vert_angle: int | None
    center_fix: str | None
    mult_code: str | None
    center_fix_region: str | None
    center_fix_sec_code: str | None
    center_fix_sub_code: str | None
    gns_fms_id: str | None
    speed_desc: str | None
    rte_qual_1: str | None
    rte_qual_2: str | None
    record_number: int | None
    cycle_data: str | None

    def __init__(self, db_record: dict):
        self.st = db_record.get("st")
        self.area = db_record.get("area")
        self.sec_code = db_record.get("sec_code")
        self.fac_id = db_record.get("fac_id")
        self.fac_region = db_record.get("fac_region")
        self.fac_sub_code = db_record.get("fac_sub_code")
        self.procedure_id = db_record.get("procedure_id")
        self.procedure_type = db_record.get("procedure_type")
        self.transition_id = db_record.get("transition_id")
        self.seq_no = db_record.get("seq_no")
        self.fix_id = db_record.get("fix_id")
        self.fix_region = db_record.get("fix_region")
        self.fix_sec_code = db_record.get("fix_sec_code")
        self.fix_sub_code = db_record.get("fix_sub_code")
        self.cont_rec_no = db_record.get("cont_rec_no")
        self.desc_code = db_record.get("desc_code")
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
        self.dist_time = db_record.get("dist_time")
        self.time = db_record.get("time")
        self.rec_vhf_sec_code = db_record.get("rec_vhf_sec_code")
        self.rec_vhf_sub_code = db_record.get("rec_vhf_sub_code")
        self.alt_desc = db_record.get("alt_desc")
        self.atc = db_record.get("atc")
        self.alt_1 = db_record.get("alt_1")
        self.fl_1 = db_record.get("fl_1")
        self.alt_2 = db_record.get("alt_2")
        self.fl_2 = db_record.get("fl_2")
        self.trans_alt = db_record.get("trans_alt")
        self.speed_limit = db_record.get("speed_limit")
        self.vert_angle = db_record.get("vert_angle")
        self.center_fix = db_record.get("center_fix")
        self.mult_code = db_record.get("mult_code")
        self.center_fix_region = db_record.get("center_fix_region")
        self.center_fix_sec_code = db_record.get("center_fix_sec_code")
        self.center_fix_sub_code = db_record.get("center_fix_sub_code")
        self.gns_fms_id = db_record.get("gns_fms_id")
        self.speed_desc = db_record.get("speed_desc")
        self.rte_qual_1 = db_record.get("rte_qual_1")
        self.rte_qual_2 = db_record.get("rte_qual_2")
        self.record_number = db_record.get("record_number")
        self.cycle_data = db_record.get("cycle_data")
