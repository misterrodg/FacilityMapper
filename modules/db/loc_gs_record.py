def select_loc_gs_by_airport_id_and_loc_id(airport_id: str, loc_id: str) -> str:
    result = f"""
    SELECT *
    FROM loc_gs
    WHERE airport_id = {airport_id} AND loc_id = {loc_id};
    """
    return result


class LOC_GS_Record:
    def __init__(self, db_record: dict):
        self.area: str = db_record.get("area")
        self.sec_code: str = db_record.get("sec_code")
        self.airport_id: str = db_record.get("airport_id")
        self.airport_region: str = db_record.get("airport_region")
        self.sub_code: str = db_record.get("sub_code")
        self.loc_id: str = db_record.get("loc_id")
        self.cat: str = db_record.get("cat")
        self.frequency: float = db_record.get("frequency")
        self.runway_id: str = db_record.get("runway_id")
        self.loc_lat: float = db_record.get("loc_lat")
        self.loc_lon: float = db_record.get("loc_lon")
        self.loc_bearing: float = db_record.get("loc_bearing")
        self.gs_lat: float = db_record.get("gs_lat")
        self.gs_lon: float = db_record.get("gs_lon")
        self.loc_dist: int = db_record.get("loc_dist")
        self.plus_minus: str = db_record.get("plus_minus")
        self.gs_thr_dist: int = db_record.get("gs_thr_dist")
        self.loc_width: float = db_record.get("loc_width")
        self.gs_angle: float = db_record.get("gs_angle")
        self.mag_var: int = db_record.get("mag_var")
        self.tch: int = db_record.get("tch")
        self.gs_elevation: int = db_record.get("gs_elevation")
        self.support_fac: str = db_record.get("support_fac")
        self.support_region: str = db_record.get("support_region")
        self.support_sec_code: str = db_record.get("support_sec_code")
        self.support_sub_code: str = db_record.get("support_sub_code")
        self.application: str = db_record.get("application")
        self.notes: str = db_record.get("notes")
        self.record_number: int = db_record.get("record_number")
        self.cycle_data: str = db_record.get("cycle_data")
