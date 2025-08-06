from modules.db.vor_record import VORRecord
from modules.db.query_helper import str_to_sql_string, list_to_sql_string


def select_vor_by_id(vor_id: str) -> str:
    vor_string = str_to_sql_string(vor_id)
    result = f"""
    SELECT * FROM vhf_navaids WHERE vhf_id = {vor_string};
    """
    return result


def select_vors_by_ids(vor_ids: list[str]) -> str:
    vor_string = list_to_sql_string(vor_ids)
    result = f"""
    SELECT * FROM vhf_navaids WHERE vhf_id IN {vor_string};
    """
    return result


class VORRecords:
    def __init__(self, db_records: list[dict]):
        self.records: list[VORRecord] = []

        for record in db_records:
            vor_record = VORRecord(record)
            self.records.append(vor_record)

    def find_vor(self, vor_id: str) -> VORRecord:
        result = next((r for r in self.records if r.vor_id == vor_id), None)
        return result

    def get_records(self) -> list[VORRecord]:
        return self.records
