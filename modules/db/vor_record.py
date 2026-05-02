from typing import Any


class VORRecord:
    st: str | None
    area: str | None
    sec_code: str | None
    sub_code: str | None
    airport_id: str | None
    airport_region: str | None
    vhf_id: str | None
    vhf_region: str | None
    cont_rec_no: int | None
    frequency: float | None
    nav_class: str | None
    lat: float | None
    lon: float | None
    dme_id: str | None
    dme_lat: float | None
    dme_lon: float | None
    mag_var: float | None
    dme_elevation: int | None
    figure_of_merit: str | None
    dme_bias: str | None
    frequency_protection: str | None
    datum_code: str | None
    vhf_name: str | None
    record_number: int | None
    cycle_data: str | None

    def __init__(self, db_record: dict[str, Any]) -> None:
        self.st = db_record.get("st")
        self.area = db_record.get("area")
        self.sec_code = db_record.get("sec_code")
        self.sub_code = db_record.get("sub_code")
        self.airport_id = db_record.get("airport_id")
        self.airport_region = db_record.get("airport_region")
        self.vhf_id = db_record.get("vhf_id")
        self.vhf_region = db_record.get("vhf_region")
        self.cont_rec_no = db_record.get("cont_rec_no")
        self.frequency = db_record.get("frequency")
        self.nav_class = db_record.get("nav_class")
        self.lat = db_record.get("lat")
        self.lon = db_record.get("lon")
        self.dme_id = db_record.get("dme_id")
        self.dme_lat = db_record.get("dme_lat")
        self.dme_lon = db_record.get("dme_lon")
        self.mag_var = db_record.get("mag_var")
        self.dme_elevation = db_record.get("dme_elevation")
        self.figure_of_merit = db_record.get("figure_of_merit")
        self.dme_bias = db_record.get("dme_bias")
        self.frequency_protection = db_record.get("frequency_protection")
        self.datum_code = db_record.get("datum_code")
        self.vhf_name = db_record.get("vhf_name")
        self.record_number = db_record.get("record_number")
        self.cycle_data = db_record.get("cycle_data")
