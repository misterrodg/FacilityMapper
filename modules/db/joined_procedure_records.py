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
from typing import Any


def create_unified_points_table() -> list[str]:
    return [
        """
        CREATE TABLE unified_points AS
        SELECT waypoint_id AS id,lat,lon,"ENR" AS source,type,mag_var,NULL AS env_id FROM waypoints
        UNION
        SELECT waypoint_id AS id,lat,lon,"TRM" AS source,type,mag_var,environment_id env_id FROM terminal_waypoints
        UNION
        SELECT vhf_id AS id,lat,lon,"VHF" AS source,nav_class AS type,mag_var,NULL AS env_id FROM vhf_navaids WHERE nav_class LIKE '_D___' OR nav_class LIKE '_T___'
        UNION
        SELECT ndb_id AS id,lat,lon,"NDB" AS source,nav_class AS type,mag_var,NULL AS env_id FROM ndb_navaids
        UNION
        SELECT airport_id AS id,lat,lon,"APT" AS source,"AIRPORT" AS type,mag_var,airport_id AS env_id FROM airports
        UNION
        SELECT runway_id AS id,lat,lon,"RWY" AS source,"RUNWAY" AS type,0.0 AS mag_var,airport_id AS env_id FROM runways;
        """,
        """
        CREATE INDEX idx_unified_point_id ON unified_points(id,env_id);
        """,
    ]


def create_unified_navaids_table() -> list[str]:
    return [
        """
        CREATE TABLE unified_navaids AS
        SELECT vhf_id AS id,lat,lon,sub_code,mag_var,vhf_region AS region FROM vhf_navaids
        UNION
        SELECT ndb_id AS id,lat,lon,sub_code,mag_var,ndb_region AS region FROM ndb_navaids;
        """,
        """
        CREATE INDEX idx_unified_navaid_id ON unified_navaids(id,sub_code,region);
        """,
    ]


def select_joined_procedure_points(
    fac_id: str,
    fac_sub_code: str,
    procedure_id: str,
    transitions: list[str] | None = None,
    procedure_types: list[str] | None = None,
    path_terms: list[str] | None = None,
) -> str:
    transitions = transitions or []
    procedure_types = procedure_types or []
    path_terms = path_terms or []

    fac_id_string = str_to_sql_string(fac_id)
    fac_sub_code_string = str_to_sql_string(fac_sub_code)
    procedure_id_string = translate_condition("procedure_id", procedure_id)
    transition_string = handle_transitions(transitions)
    procedure_type_string = handle_procedure_type(procedure_types)
    path_term_string = handle_path_term(path_terms)
    result = f"""
    SELECT p.*,up.lat AS fix_lat,up.lon AS fix_lon,up.source AS fix_source,up.type AS fix_type,up.mag_var AS fix_mag_var,un.lat AS rec_vhf_lat,un.lon AS rec_vhf_lon,t.lat AS center_lat,t.lon AS center_lon
    FROM procedure_points AS p
    LEFT JOIN unified_points AS up ON p.fix_id = up.id AND (up.env_id = {fac_id_string} OR up.env_id IS NULL)
    LEFT JOIN unified_navaids AS un ON p.rec_vhf = un.id AND p.rec_vhf_sub_code = un.sub_code AND p.rec_vhf_region = un.region
    LEFT JOIN terminal_waypoints AS t ON p.center_fix = t.waypoint_id AND t.environment_id = {fac_id_string}
    WHERE fac_id = {fac_id_string} AND fac_sub_code = {fac_sub_code_string} AND {procedure_id_string} {procedure_type_string} {transition_string} {path_term_string}
    ORDER BY p.procedure_id,p.procedure_type,p.transition_id DESC,p.seq_no;
    """
    return result


class JoinedProcedureRecords:
    records: list[JoinedProcedureRecord]

    def __init__(self, db_records: list[dict[str, Any]]):
        self.records = []

        for record in db_records:
            joined_procedure_record = JoinedProcedureRecord(record)
            if (
                joined_procedure_record.fix_lat is not None
                and joined_procedure_record.fix_lon is not None
            ):
                self.records.append(joined_procedure_record)

    def get_records(self) -> list[JoinedProcedureRecord]:
        return self.records

    def trim_missed(self, keep_runway: bool = False) -> None:
        result: list[JoinedProcedureRecord] = []
        missed_reached = False
        for record in self.records:
            fix_id = record.fix_id
            is_runway_fix = isinstance(fix_id, str) and fix_id.startswith("RW")
            if not missed_reached and (keep_runway or not is_runway_fix):
                result.append(record)

            desc_code = record.desc_code
            if isinstance(desc_code, str) and len(desc_code) > 3 and desc_code[3] == "M":
                missed_reached = True

        self.records = result
