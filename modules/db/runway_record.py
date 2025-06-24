class RunwayRecord:
    st: str | None
    area: str | None
    sec_code: str | None
    airport_id: str | None
    airport_region: str | None
    sub_code: str | None
    runway_id: str | None
    cont_rec_no: int | None
    length: int | None
    bearing: float | None
    true: bool | None
    lat: float | None
    lon: float | None
    gradient: int | None
    ellipsoidal_height: int | None
    threshold_elevation: int | None
    displaced_threshold: int | None
    tch: int | None
    width: int | None
    tch_id: str | None
    ls_ident_1: str | None
    cat_1: str | None
    stopway: str | None
    ls_ident_2: str | None
    cat_2: str | None
    description: str | None
    record_number: int | None
    cycle_data: str | None

    def __init__(self, db_record: dict):
        self.st = db_record.get("st")
        self.area = db_record.get("area")
        self.sec_code = db_record.get("sec_code")
        self.airport_id = db_record.get("airport_id")
        self.airport_region = db_record.get("airport_region")
        self.sub_code = db_record.get("sub_code")
        self.runway_id = db_record.get("runway_id")
        self.cont_rec_no = db_record.get("cont_rec_no")
        self.length = db_record.get("length")
        self.bearing = db_record.get("bearing")
        self.true = db_record.get("true")
        self.lat = db_record.get("lat")
        self.lon = db_record.get("lon")
        self.gradient = db_record.get("gradient")
        self.ellipsoidal_height = db_record.get("ellipsoidal_height")
        self.threshold_elevation = db_record.get("threshold_elevation")
        self.displaced_threshold = db_record.get("displaced_threshold")
        self.tch = db_record.get("tch")
        self.width = db_record.get("width")
        self.tch_id = db_record.get("tch_id")
        self.ls_ident_1 = db_record.get("ls_ident_1")
        self.cat_1 = db_record.get("cat_1")
        self.stopway = db_record.get("stopway")
        self.ls_ident_2 = db_record.get("ls_ident_2")
        self.cat_2 = db_record.get("cat_2")
        self.description = db_record.get("description")
        self.record_number = db_record.get("record_number")
        self.cycle_data = db_record.get("cycle_data")
