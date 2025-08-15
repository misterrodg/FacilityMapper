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


def create_unified_points_table() -> list:
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


def create_unified_navaids_table() -> list:
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

    def __init__(self, db_records: list[dict]):
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
