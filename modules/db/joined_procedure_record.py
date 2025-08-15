from modules.db.procedure_record import ProcedureRecord


class JoinedProcedureRecord(ProcedureRecord):
    fix_lat: float | None
    fix_lon: float | None
    fix_source: str | None
    fix_type: str | None
    fix_mag_var: float | None
    rec_vhf_id: str | None
    rec_vhf_lat: float | None
    rec_vhf_lon: float | None
    center_id: str | None
    center_lat: float | None
    center_lon: float | None

    def __init__(self, db_record: dict):
        super().__init__(db_record)
        self.fix_lat = db_record.get("fix_lat")
        self.fix_lon = db_record.get("fix_lon")
        self.fix_source = db_record.get("fix_source")
        self.fix_type = db_record.get("fix_type")
        self.fix_mag_var = db_record.get("fix_mag_var")
        self.rec_vhf_id = db_record.get("rec_vhf_id")
        self.rec_vhf_lat = db_record.get("rec_vhf_lat")
        self.rec_vhf_lon = db_record.get("rec_vhf_lon")
        self.center_id = db_record.get("center_id")
        self.center_lat = db_record.get("center_lat")
        self.center_lon = db_record.get("center_lon")
