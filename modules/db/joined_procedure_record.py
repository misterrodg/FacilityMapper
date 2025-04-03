from modules.db.procedure_record import ProcedureRecord


class JoinedProcedureRecord(ProcedureRecord):
    def __init__(self, db_record: dict):
        super().__init__(db_record)
        self.id = db_record.get("id")
        self.lat = db_record.get("lat")
        self.lon = db_record.get("lon")
        self.type = db_record.get("type")
