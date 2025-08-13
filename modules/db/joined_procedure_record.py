from modules.db.procedure_record import ProcedureRecord


class JoinedProcedureRecord(ProcedureRecord):
    id: str | None
    lat: float | None
    lon: float | None
    source: str | None
    type: str | None
    mag_var: float | None
    env_id: str | None
    center_id: str | None
    center_lat: float | None
    center_lon: float | None

    def __init__(self, db_record: dict):
        super().__init__(db_record)
        self.id = db_record.get("id")
        self.lat = db_record.get("lat")
        self.lon = db_record.get("lon")
        self.source = db_record.get("source")
        self.type = db_record.get("type")
        self.mag_var = db_record.get("mag_var")
        self.env_id = db_record.get("env_id")
        self.center_id = db_record.get("center_id")
        self.center_lat = db_record.get("center_lat")
        self.center_lon = db_record.get("center_lon")
