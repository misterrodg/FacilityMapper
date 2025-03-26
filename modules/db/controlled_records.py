from modules.db.airspace_record import AirspaceRecord
from modules.db.controlled_record import ControlledRecord
from modules.db.record_helper import segment_records


def select_controlled_points(airport_id: str) -> str:
    result = f"""
    SELECT * 
    FROM controlled_airspace_points 
    WHERE center_id = {airport_id}
    ORDER BY center_id, airspace_class, multiple_code, sequence_number;
    """
    return result


class ControlledRecords:
    def __init__(self, db_records: list[dict]):
        self.records: list[ControlledRecord] = []

        for record in db_records:
            controlled_record = ControlledRecord(record)
            self.records.append(controlled_record)

    def get_records(self) -> list[ControlledRecord]:
        return self.records

    def get_segmented_records(self) -> list[list[ControlledRecord]]:
        result = segment_records(self.records, ControlledRecord.SEGMENT_FIELDS)
        return result

    def get_line_definitions(self) -> list[AirspaceRecord]:
        result = []
        for record in self.records:
            line_definition = record.get_line_definition()
            result.append(line_definition)
        return result

    def get_segmented_line_definitions(self) -> list[list[AirspaceRecord]]:
        airspace_records = []
        for record in self.records:
            line_definition = record.get_line_definition()
            airspace_records.append(line_definition)
        result = segment_records(airspace_records, ControlledRecord.SEGMENT_FIELDS)
        return result
