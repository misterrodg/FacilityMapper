def select_loc_gs_by_airport_id_and_loc_id(airport_id: str, loc_id: str) -> str:
    result = f"""
    SELECT *
    FROM loc_gss
    WHERE airport_id = {airport_id} AND loc_id = {loc_id};
    """
    return result


class LOC_GS_Record:
    st: str | None
    area: str | None
    sec_code: str | None
    airport_id: str | None
    airport_region: str | None
    sub_code: str | None
    loc_id: str | None
    cat: str | None
    cont_rec_no: str | None
    frequency: float | None
    runway_id: str | None
    loc_lat: float | None
    loc_lon: float | None
    loc_bearing: float | None
    true: bool | None
    gs_lat: float | None
    gs_lon: float | None
    loc_dist: int | None
    plus_minus: str | None
    gs_thr_dist: int | None
    loc_width: float | None
    gs_angle: float | None
    mag_var: int | None
    tch: int | None
    gs_elevation: int | None
    support_fac: str | None
    support_region: str | None
    support_sec_code: str | None
    support_sub_code: str | None
    record_number: int | None
    cycle_data: str | None

    def __init__(self, db_record: dict):
        self.st = db_record.get("st")
        self.area = db_record.get("area")
        self.sec_code = db_record.get("sec_code")
        self.airport_id = db_record.get("airport_id")
        self.airport_region = db_record.get("airport_region")
        self.sub_code = db_record.get("sub_code")
        self.loc_id = db_record.get("loc_id")
        self.cat = db_record.get("cat")
        self.cont_rec_no = db_record.get("cont_rec_no")
        self.frequency = db_record.get("frequency")
        self.runway_id = db_record.get("runway_id")
        self.loc_lat = db_record.get("loc_lat")
        self.loc_lon = db_record.get("loc_lon")
        self.loc_bearing = db_record.get("loc_bearing")
        self.true = db_record.get("true")
        self.gs_lat = db_record.get("gs_lat")
        self.gs_lon = db_record.get("gs_lon")
        self.loc_dist = db_record.get("loc_dist")
        self.plus_minus = db_record.get("plus_minus")
        self.gs_thr_dist = db_record.get("gs_thr_dist")
        self.loc_width = db_record.get("loc_width")
        self.gs_angle = db_record.get("gs_angle")
        self.mag_var = db_record.get("mag_var")
        self.tch = db_record.get("tch")
        self.gs_elevation = db_record.get("gs_elevation")
        self.support_fac = db_record.get("support_fac")
        self.support_region = db_record.get("support_region")
        self.support_sec_code = db_record.get("support_sec_code")
        self.support_sub_code = db_record.get("support_sub_code")
        self.record_number = db_record.get("record_number")
        self.cycle_data = db_record.get("cycle_data")
