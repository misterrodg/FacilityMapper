from modules.db.airspace_record import AirspaceRecord
from modules.db.controlled_record import ControlledRecord
from modules.db.record_helper import segment_records


def select_controlled_points(airport_id: str) -> str:
    result = f"""
    SELECT * 
    FROM controlled_points 
    WHERE center_id = {airport_id}
    ORDER BY center_id, airspace_class, mult_code, seq_no;
    """
    return result


class ControlledRecords:
    records: list[ControlledRecord]

    def __init__(self):
        self.records = []

    def from_list(self, controlled_record_list: list[ControlledRecord]) -> None:
        self.records.extend(controlled_record_list)
        return

    def from_db_records(self, db_records: list[dict]) -> None:
        for record in db_records:
            controlled_record = ControlledRecord(record)
            self.records.append(controlled_record)
        return

    def get_records(self) -> list[ControlledRecord]:
        return self.records

    def get_segmented_records(self) -> list[list[ControlledRecord]]:
        result = segment_records(self.records, ControlledRecord.SEGMENT_FIELD)
        return result

    def get_segmented_by_airspace_class(self) -> list[list[ControlledRecord]]:
        result = segment_records(self.records, "airspace_class")
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
        result = segment_records(airspace_records, ControlledRecord.SEGMENT_FIELD)
        return result

    def check_for_multiple_classes(self) -> bool:
        last_airspace_class = None
        for record in self.records:
            if (
                last_airspace_class != None
                and record.airspace_class != last_airspace_class
            ):
                return True
            last_airspace_class = record.airspace_class
        return False
