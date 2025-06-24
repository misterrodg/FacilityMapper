from modules.db.procedure_records import (
    handle_path_term,
    handle_procedure_type,
    handle_transitions,
)
from modules.db.joined_procedure_record import JoinedProcedureRecord
from modules.db.query_helper import (
    str_to_sql_string,
    translate_condition,
)
from modules.db.record_helper import (
    cast_from_to,
    revert_from_to,
    segment_records,
    segment_from_to,
)


def select_joined_procedure_points(
    fac_id: str,
    fac_sub_code: str,
    procedure_id: str,
    transitions: list = [],
    procedure_types: list = [],
    path_terms: list = [],
) -> str:
    fac_id_string = str_to_sql_string(fac_id)
    fac_sub_code_string = str_to_sql_string(fac_sub_code)
    procedure_id_string = translate_condition("procedure_id", procedure_id)
    transition_string = handle_transitions(transitions)
    procedure_type_string = handle_procedure_type(procedure_types)
    path_term_string = handle_path_term(path_terms)
    result = f"""
    WITH unified_table AS (
        SELECT waypoint_id AS id,lat,lon,type,mag_var FROM waypoints
        UNION
        SELECT waypoint_id AS id,lat,lon,type,mag_var FROM terminal_waypoints WHERE environment_id = {fac_id_string}
        UNION
        SELECT vhf_id AS id,lat,lon,"VORDME" AS type,mag_var FROM vhf_navaids WHERE nav_class LIKE 'VD___' OR nav_class LIKE 'VT___'
        UNION
        SELECT vhf_id AS id,lat,lon,"VOR" AS type,mag_var FROM vhf_navaids WHERE nav_class LIKE 'V ___'
        UNION
        SELECT vhf_id AS id,lat,lon,"DME" AS type,mag_var FROM vhf_navaids WHERE nav_class LIKE ' D___' OR nav_class LIKE ' T___'
        UNION
        SELECT ndb_id AS id,lat,lon,"NDB" AS type,mag_var FROM ndb_navaids
        UNION
        SELECT runway_id AS id,lat,lon,"RUNWAY" AS type,0.0 AS mag_var FROM runways WHERE airport_id = {fac_id_string}
    )
    SELECT p.*,id,lat,lon,type,mag_var
    FROM procedure_points AS p
    LEFT JOIN unified_table AS u ON p.fix_id = u.id
    WHERE fac_id = {fac_id_string} AND fac_sub_code = {fac_sub_code_string} AND {procedure_id_string} {procedure_type_string} {transition_string} {path_term_string}
    ORDER BY p.procedure_id,p.procedure_type,p.transition_id DESC,p.seq_no;
    """
    return result


class JoinedProcedureRecords:
    records: list[JoinedProcedureRecord]

    def __init__(self, db_records: list[dict]):
        self.records = []

        for record in db_records:
            joined_procedure_record = JoinedProcedureRecord(record)
            if (
                joined_procedure_record.lat is not None
                and joined_procedure_record.lon is not None
            ):
                self.records.append(joined_procedure_record)

    def get_records(self) -> list[JoinedProcedureRecord]:
        return self.records

    def get_segmented_records(self) -> list[list[JoinedProcedureRecord]]:
        result = segment_records(self.records, JoinedProcedureRecord.SEGMENT_FIELD)
        return result

    def get_segmented_from_to(
        self,
    ) -> list[list[tuple[JoinedProcedureRecord, JoinedProcedureRecord]]]:
        result = segment_from_to(self.records, JoinedProcedureRecord.SEGMENT_FIELD)
        return result

    def get_unique_paths(self) -> list[list[JoinedProcedureRecord]]:
        result: list = []
        segmented_records = segment_records(
            self.records, JoinedProcedureRecord.SEGMENT_FIELD
        )

        seen: list = []

        for segment in segmented_records:
            from_to = cast_from_to(segment)
            unique: list = []
            for record_from, record_to in from_to:
                pair = f"{record_from.fix_id}-{record_to.fix_id}"
                value = None
                if pair not in seen:
                    seen.append(pair)
                    value = (record_from, record_to)
                unique.append(value)
            if unique:
                split = _check_for_split(unique)
                for item in split:
                    result.append(revert_from_to(item))

        return result

    def get_unique_paths_from_to(
        self,
    ) -> list[list[tuple[JoinedProcedureRecord, JoinedProcedureRecord]]]:
        result: list = []
        segmented_records = segment_records(
            self.records, JoinedProcedureRecord.SEGMENT_FIELD
        )

        seen: list = []

        for segment in segmented_records:
            from_to = cast_from_to(segment)
            unique: list = []
            for record_from, record_to in from_to:
                pair = f"{record_from.fix_id}-{record_to.fix_id}"
                value = None
                if pair not in seen and record_from.fix_id != record_to.fix_id:
                    seen.append(pair)
                    value = (record_from, record_to)
                unique.append(value)
            if unique:
                split = _check_for_split(unique)
                for item in split:
                    result.append(item)

        return result

    def trim_missed(self, keep_runway: bool = False) -> None:
        result = []
        missed_reached = False
        for record in self.records:
            if missed_reached == False and (keep_runway or record.fix_id[0:2] != "RW"):
                result.append(record)
            if record.desc_code[3] == "M":
                missed_reached = True

        self.records = result

    def add_procedure_name_to_enroute_transitions(self) -> None:
        for record in self.records:
            if record.fix_id == record.transition_id:
                record.fix_id = f"{record.procedure_id}.{record.fix_id}"
        return

    def add_procedure_name_to_core(self, last: bool = False) -> None:
        record = self.records[-1] if last else self.records[0]
        record.fix_id = f"{record.procedure_id}.{record.fix_id}"

    def add_procedure_name_to_runway_transitions(self) -> None:
        for record in self.records:
            if record.fix_id == record.procedure_id[:-1]:
                record.fix_id = f"{record.procedure_id}.{record.fix_id}"


def _check_for_split(list_to_verify: list) -> list[list]:
    result: list = []
    temporary: list = []

    for item in list_to_verify:
        if item is not None:
            temporary.append(item)
        else:
            if temporary:
                result.append(temporary)
                temporary = []

    if temporary:
        result.append(temporary)

    return result
