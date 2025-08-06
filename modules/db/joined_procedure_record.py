from modules.db.procedure_record import ProcedureRecord


class JoinedProcedureRecord(ProcedureRecord):
    id: str | None
    lat: float | None
    lon: float | None
    source: str | None
    type: str | None
    mag_var: float | None

    def __init__(self, db_record: dict):
        super().__init__(db_record)
        self.id = db_record.get("id")
        self.lat = db_record.get("lat")
        self.lon = db_record.get("lon")
        self.source = db_record.get("source")
        self.type = db_record.get("type")
        self.mag_var = db_record.get("mag_var")
