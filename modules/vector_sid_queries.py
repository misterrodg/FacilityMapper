def select_procedure_points(fac_id: str, procedure_id: str) -> str:
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
    )
    SELECT p.*,lat,lon,type
    FROM procedure_points AS p
    LEFT JOIN unified_table AS u ON p.fix_id = u.id
    WHERE fac_id={fac_id} AND fac_sub_code = 'D' AND procedure_id LIKE {procedure_id} AND fix_id != {fac_id} AND route_type = 'V' AND p.path_term NOT IN ('FM','HA','HF','HM','PI','VM')
    ORDER BY p.procedure_id,p.transition_id,p.route_type,p.sequence_number;
    """
    return result
