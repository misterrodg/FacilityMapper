from modules.db.procedure_record import ProcedureRecord
from modules.db.query_helper import (
    list_to_sql_string,
    str_to_sql_string,
    translate_condition,
)


def handle_transitions(transition_ids: list) -> str:
    if "ALL" in transition_ids:
        return ""
    if transition_ids:
        transition_ids_as_string = list_to_sql_string(transition_ids)
        return f"AND (transition_id IS NULL OR transition_id IN {transition_ids_as_string})"
    return "AND (transition_id IS NULL OR transition_id = 'ALL')"


def handle_route_type(route_types: list) -> str:
    result = ""
    if route_types:
        route_types_as_string = list_to_sql_string(route_types)
        result = f"AND p.route_type IN {route_types_as_string}"
    return result


def handle_path_term(path_terms: list) -> str:
    result = "AND p.path_term NOT IN ('FM','HA','HF','HM','PI','VM')"
    if path_terms:
        path_terms_as_string = list_to_sql_string(path_terms)
        result = f"AND p.path_term NOT IN {path_terms_as_string}"
    return result


def select_procedure_points(
    fac_id: str,
    fac_sub_code: str,
    procedure_id: str,
    transitions: list = [],
    route_types: list = [],
    path_terms: list = [],
) -> str:
    fac_id_string = str_to_sql_string(fac_id)
    fac_sub_code_string = str_to_sql_string(fac_sub_code)
    procedure_id_string = translate_condition("procedure_id", procedure_id)
    transition_string = handle_transitions(transitions)
    route_type_string = handle_route_type(route_types)
    path_term_string = handle_path_term(path_terms)
    result = f"""
    SELECT *
    FROM procedure_points
    WHERE fac_id = {fac_id_string} AND fac_sub_code = {fac_sub_code_string} AND {procedure_id_string} {route_type_string} {transition_string} {path_term_string}
    ORDER BY procedure_id,route_type,transition_id DESC,sequence_number;
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
