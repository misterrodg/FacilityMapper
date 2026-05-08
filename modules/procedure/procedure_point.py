class ProcedurePoint:
    SEGMENT_FIELD = "transition_id"

    fix_id: str | None = None
    fix_lat: float | None = None
    fix_lon: float | None = None
    fix_source: str | None = None
    fix_type: str | None = None
    fix_mag_var: float | None = None
    symbol_name: str | None = None
    procedure_id: str | None = None
    procedure_type: str | None = None
    fac_sub_code: str | None = None
    transition_id: str | None = None
    seq_no: int | None = None
    path_term: str | None = None
    course: float | None = None
    center_fix: str | None = None
    center_lat: float | None = None
    center_lon: float | None = None
    arc_radius: float | None = None
    turn_direction: str | None = None
    desc_code: str | None = None
    alt_desc: str | None = None
    alt_1: int | None = None
    fl_1: bool | None = None
    alt_2: int | None = None
    fl_2: bool | None = None
    speed_desc: str | None = None
    speed_limit: int | None = None

    def __init__(
        self,
        fix_id: str | None = None,
        fix_lat: float | None = None,
        fix_lon: float | None = None,
        fix_source: str | None = None,
        fix_type: str | None = None,
        fix_mag_var: float | None = None,
        symbol_name: str | None = None,
        procedure_id: str | None = None,
        procedure_type: str | None = None,
        fac_sub_code: str | None = None,
        transition_id: str | None = None,
        seq_no: int | None = None,
        path_term: str | None = None,
        course: float | None = None,
        center_fix: str | None = None,
        center_lat: float | None = None,
        center_lon: float | None = None,
        arc_radius: float | None = None,
        turn_direction: str | None = None,
        desc_code: str | None = None,
        alt_desc: str | None = None,
        alt_1: int | None = None,
        fl_1: bool | None = None,
        alt_2: int | None = None,
        fl_2: bool | None = None,
        speed_desc: str | None = None,
        speed_limit: int | None = None,
    ) -> None:
        self.fix_id = fix_id
        self.fix_lat = fix_lat
        self.fix_lon = fix_lon
        self.fix_source = fix_source
        self.fix_type = fix_type
        self.fix_mag_var = fix_mag_var
        self.symbol_name = symbol_name
        self.procedure_id = procedure_id
        self.procedure_type = procedure_type
        self.fac_sub_code = fac_sub_code
        self.transition_id = transition_id
        self.seq_no = seq_no
        self.path_term = path_term
        self.course = course
        self.center_fix = center_fix
        self.center_lat = center_lat
        self.center_lon = center_lon
        self.arc_radius = arc_radius
        self.turn_direction = turn_direction
        self.desc_code = desc_code
        self.alt_desc = alt_desc
        self.alt_1 = alt_1
        self.fl_1 = fl_1
        self.alt_2 = alt_2
        self.fl_2 = fl_2
        self.speed_desc = speed_desc
        self.speed_limit = speed_limit

    def fix_type_to_symbol_name(self, use_faf_symbol: bool = False) -> str | None:
        if use_faf_symbol and self.desc_code is not None and self.desc_code.endswith("F"):
            return "FAF"
        return self.symbol_name
