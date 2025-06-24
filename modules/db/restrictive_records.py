from modules.db.airspace_record import AirspaceRecord
from modules.db.record_helper import segment_records
from modules.db.restrictive_record import RestrictiveRecord


def select_restrictive_points(restrictive_id: str) -> str:
    result = f"""
    SELECT *
    FROM restrictive_airspace_points
    WHERE restrictive_id = {restrictive_id}
    ORDER BY restrictive_id, mult_code, seq_no;
    """
    return result


class RestrictiveRecords:
    records: list[RestrictiveRecord]

    def __init__(self, db_records: list[dict]):
        self.records = []

        for record in db_records:
            restrictive_record = RestrictiveRecord(record)
            self.records.append(restrictive_record)

    def get_records(self) -> list[RestrictiveRecord]:
        return self.records

    def get_segmented_records(self) -> list[list[RestrictiveRecord]]:
        result = segment_records(self.records, RestrictiveRecord.SEGMENT_FIELD)
        return result

    def get_line_definitions(self) -> list[AirspaceRecord]:
        result = []
        for record in self.records:
            line_definition = record.get_line_definition()
            result.append(line_definition)
        return result

    def get_segmented_line_definitions(self) -> list[list[AirspaceRecord]]:
        airspace_records = self.get_line_definitions()
        result = segment_records(airspace_records, RestrictiveRecord.SEGMENT_FIELD)
        return result
