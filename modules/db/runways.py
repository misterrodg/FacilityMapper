from modules.db.runway import RunwayRecord


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
            runway_id = self._inverse_runway(runway_id)

        result = next((r for r in self.records if r.runway_id == runway_id), None)
        return result

    def get_records(self) -> list[RunwayRecord]:
        return self.records

    def _handle_bearing_component(self, bearing_component: int) -> int:
        if bearing_component == 18:
            return 36
        return (bearing_component + 18) % 36

    def _handle_side_component(self, side_component: str) -> str:
        if side_component == "L":
            return "R"
        if side_component == "R":
            return "L"
        return "C"

    def _inverse_runway(self, runway_id: str) -> str:
        runway_prefix = "RW"
        bearing_component = int(runway_id[2:4])
        inverse_bearing = self._handle_bearing_component(bearing_component)
        side_component = runway_id[4:]
        inverse_side = ""
        if side_component:
            inverse_side = self._handle_side_component(side_component)
        result = f"{runway_prefix}{inverse_bearing:02}{inverse_side}"
        return result
