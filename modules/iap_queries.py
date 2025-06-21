def select_procedure_points(
    fac_id: str, fac_sub_code: str, procedure_id: str, transition_id_string: str
) -> str:
    result = f"""
    WITH unified_table AS (
        SELECT waypoint_id AS id,lat,lon,type FROM waypoints
        UNION
        SELECT waypoint_id AS id,lat,lon,type FROM terminal_waypoints WHERE environment_id = {fac_id}
        UNION
        SELECT vhf_id AS id,lat,lon,"VORDME" AS type FROM vhf_navaids WHERE nav_class LIKE 'VD___' OR nav_class LIKE 'VT___'
        UNION
        SELECT vhf_id AS id,lat,lon,"VOR" AS type FROM vhf_navaids WHERE nav_class LIKE 'V ___'
        UNION
        SELECT vhf_id AS id,lat,lon,"DME" AS type FROM vhf_navaids WHERE nav_class LIKE ' D___' OR nav_class LIKE ' T___'
        UNION
        SELECT ndb_id AS id,lat,lon,"NDB" AS type FROM ndb_navaids
        UNION
        SELECT runway_id AS id,lat,lon,"RUNWAY" AS type FROM runways WHERE airport_id = {fac_id}
    )
    SELECT p.*,lat,lon,type
    FROM procedure_points AS p
    LEFT JOIN unified_table AS u ON p.fix_id = u.id
    WHERE fac_id = {fac_id} AND fac_sub_code={fac_sub_code} AND procedure_id={procedure_id} AND transition_id {transition_id_string} AND p.path_term NOT IN ('FM','HA','HF','HM','PI','VM')
    ORDER BY p.procedure_id,p.transition_id,p.procedure_type,p.seq_no;
    """
    return result
