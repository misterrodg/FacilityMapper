from modules.db.procedure_records import (
    handle_path_term,
    handle_route_type,
    handle_transitions,
)
from modules.db.joined_procedure_record import JoinedProcedureRecord
from modules.db.query_helper import (
    str_to_sql_string,
    translate_condition,
)
from modules.db.record_helper import cast_from_to, revert_from_to, segment_records


def select_joined_procedure_points(
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
    WHERE fac_id = {fac_id_string} AND fac_sub_code = {fac_sub_code_string} AND {procedure_id_string} {route_type_string} {transition_string} {path_term_string}
    ORDER BY p.procedure_id,p.route_type,p.transition_id DESC,p.sequence_number;
    """
    return result


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

    def get_segmented_records(self) -> list[list[JoinedProcedureRecord]]:
        result = segment_records(self.records, JoinedProcedureRecord.SEGMENT_FIELD)
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

    def trim_missed(self) -> list[JoinedProcedureRecord]:
        result = []
        missed_reached = False
        for record in self.records:
            if missed_reached == False and record.fix_id[0:2] != "RW":
                result.append(record)
            if record.description_code[3] == "M":
                missed_reached = True

        return result


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
