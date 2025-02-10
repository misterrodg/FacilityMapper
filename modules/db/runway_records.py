from modules.db.runway_record import RunwayRecord
from modules.runway.runway_helper import inverse_runway


def select_runways_by_airport_id(airport_id: str) -> str:
    result = f"""
    SELECT airport_id,runway_id,lat,lon,displaced_threshold FROM runways WHERE airport_id = {airport_id} ORDER BY runway_id;
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
    def __init__(self, db_records: list[dict]):
        self.records: list[RunwayRecord] = []

        for record in db_records:
            runway_record = RunwayRecord(record)
            self.records.append(runway_record)

    def find_runway(
        self, runway_id: str, find_inverse_id: bool = False
    ) -> RunwayRecord:
        if find_inverse_id:
            runway_id = inverse_runway(runway_id)

        result = next((r for r in self.records if r.runway_id == runway_id), None)
        return result

    def get_records(self) -> list[RunwayRecord]:
        return self.records
