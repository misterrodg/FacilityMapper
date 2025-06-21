def select_procedure_points(
    fac_id: str,
    fac_sub_code: str,
    procedure_id: str,
    procedure_type_string: str,
    path_term_string: str,
) -> str:
    result = f"""
    WITH unified_table AS (
        SELECT waypoint_id AS id,lat,lon,mag_var,type FROM waypoints
        UNION
        SELECT waypoint_id AS id,lat,lon,mag_var,type FROM terminal_waypoints WHERE environment_id = {fac_id}
        UNION
        SELECT vhf_id AS id,lat,lon,mag_var,"VORDME" AS type FROM vhf_navaids WHERE nav_class LIKE 'VD___' OR nav_class LIKE 'VT___'
        UNION
        SELECT vhf_id AS id,lat,lon,mag_var,"VOR" AS type FROM vhf_navaids WHERE nav_class LIKE 'V ___'
        UNION
        SELECT vhf_id AS id,dme_lat AS lat,dme_lon AS lon,mag_var,"DME" AS type FROM vhf_navaids WHERE nav_class LIKE ' D___' OR nav_class LIKE ' T___'
        UNION
        SELECT ndb_id AS id,lat,lon,mag_var,"NDB" AS type FROM ndb_navaids
        UNION
        SELECT airport_id AS id,lat,lon,mag_var,"AIRPORT" as type FROM airports
    )
    SELECT p.*,lat,lon,mag_var,type
    FROM procedure_points AS p
    LEFT JOIN unified_table AS u ON p.fix_id = u.id
    WHERE fac_id = {fac_id} AND fac_sub_code={fac_sub_code} AND procedure_id LIKE {procedure_id} AND procedure_type IN ({procedure_type_string}) AND p.path_term NOT IN ({path_term_string})
    ORDER BY p.procedure_id,p.transition_id,p.procedure_type,p.seq_no;
    """
    return result
