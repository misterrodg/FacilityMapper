from modules.db.procedure_record import ProcedureRecord, JoinedProcedureRecord
from modules.db.query_helper import (
    list_to_sql_string,
    str_to_sql_string,
    translate_condition,
)
from modules.db.record_helper import segment_records


def _handle_transitions(transition_ids: list) -> str:
    if "ALL" in transition_ids:
        return ""
    if transition_ids:
        transition_ids_as_string = list_to_sql_string(transition_ids)
        return f"AND (transition_id IS NULL OR transition_id IN {transition_ids_as_string})"
    return "AND transition_id IS NULL"


def _handle_path_term(path_terms: list) -> str:
    result = "p.path_term NOT IN ('FM','HA','HF','HM','PI','VM')"
    if path_terms:
        path_terms_as_string = list_to_sql_string(path_terms)
        result = f"p.path_term NOT IN {path_terms_as_string}"
    return result


def select_joined_procedure_points(
    fac_id: str,
    fac_sub_code: str,
    procedure_id: str,
    transitions: list = [],
    path_terms: list = [],
) -> str:
    fac_id_string = str_to_sql_string(fac_id)
    fac_sub_code_string = str_to_sql_string(fac_sub_code)
    transition_string = _handle_transitions(transitions)
    procedure_id_string = translate_condition("procedure_id", procedure_id)
    path_term_string = _handle_path_term(path_terms)
    result = f"""
    WITH unified_table AS (
        SELECT waypoint_id AS id,lat,lon,type FROM waypoints
        UNION
        SELECT vhf_id AS id,lat,lon,"VORDME" AS type FROM vhf_dmes WHERE lat IS NOT NULL AND dme_lat IS NOT NULL
        UNION
        SELECT vhf_id AS id,lat,lon,"VOR" AS type FROM vhf_dmes WHERE lat IS NOT NULL AND dme_lat IS NULL
        UNION
        SELECT vhf_id AS id,lat,lon,"DME" AS type FROM vhf_dmes WHERE dme_id IS NOT NULL
        UNION
        SELECT ndb_id AS id,lat,lon,"NDB" AS type FROM ndbs
        UNION
        SELECT runway_id AS id,lat,lon,"RUNWAY" AS type FROM runways WHERE airport_id = {fac_id_string}
    )
    SELECT p.*,id,lat,lon,type
    FROM procedure_points AS p
    LEFT JOIN unified_table AS u ON p.fix_id = u.id
    WHERE fac_id = {fac_id_string} AND fac_sub_code = {fac_sub_code_string} AND {procedure_id_string} {transition_string} AND {path_term_string}
    ORDER BY p.procedure_id,p.route_type,p.transition_id DESC,p.sequence_number;
    """
    return result


class ProcedureRecords:
    def __init__(self, db_records: list[dict]):
        self.records = list[ProcedureRecord] = []

        for record in db_records:
            procedure_record = ProcedureRecord(record)
            self.records.append(procedure_record)

    def get_records(self) -> list[ProcedureRecord]:
        return self.records


class JoinedProcedureRecords:
    def __init__(self, db_records: list[dict]):
        self.records: list[JoinedProcedureRecord] = []

        for record in db_records:
            joined_procedure_record = JoinedProcedureRecord(record)
            if (
                joined_procedure_record.lat is not None
                and joined_procedure_record.lon is not None
            ):
                self.records.append(joined_procedure_record)

    def get_records(self) -> list[JoinedProcedureRecord]:
        return self.records

    def trim_missed(self) -> list[JoinedProcedureRecord]:
        result = []
        missed_reached = False
        for record in self.records:
            if missed_reached == False and record.fix_id[0:2] != "RW":
                result.append(record)
            if record.description_code[3] == "M":
                missed_reached = True

        return result
