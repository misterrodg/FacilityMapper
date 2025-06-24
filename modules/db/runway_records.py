from modules.db.runway_record import RunwayRecord


def select_runways_by_airport_id(airport_id: str) -> str:
    result = f"""
    SELECT airport_id,runway_id,lat,lon,displaced_threshold FROM runways WHERE airport_id = {airport_id} AND runway_id LIKE "RW__%" ORDER BY runway_id;
    """
    return result


def select_runway_by_airport_id_and_runway_id(airport_id: str, runway_id: str) -> str:
    result = f"""
    SELECT * FROM runways WHERE airport_id = {airport_id} AND runway_id = {runway_id};
    """
    return result


def translate_runway_b(runway_id: str) -> list:
    without_b = runway_id[:-1]
    with_l = f"{without_b}L"
    with_c = f"{without_b}C"
    with_r = f"{without_b}R"
    result = [with_l, with_c, with_r]
    return result


class RunwayRecords:
    records: list[RunwayRecord]

    def __init__(self, db_records: list[dict]):
        self.records = []

        for record in db_records:
            runway_record = RunwayRecord(record)
            self.records.append(runway_record)

    def find_runway(self, runway_id: str) -> RunwayRecord:
        result = next((r for r in self.records if r.runway_id == runway_id), None)
        return result

    def get_records(self) -> list[RunwayRecord]:
        return self.records
