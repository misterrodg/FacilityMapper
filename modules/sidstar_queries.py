def select_procedure_points(
    fac_id: str,
    fac_sub_code: str,
    procedure_id: str,
    route_type_string: str,
    path_term_string: str,
) -> str:
    result = f"""
    WITH unified_table AS (
        SELECT waypoint_id AS id,lat,lon,mag_var,type FROM waypoints
        UNION
        SELECT vhf_id AS id,lat,lon,mag_var,"VORDME" AS type FROM vhf_dmes WHERE lat IS NOT NULL AND dme_lat IS NOT NULL
        UNION
        SELECT vhf_id AS id,lat,lon,mag_var,"VOR" AS type FROM vhf_dmes WHERE lat IS NOT NULL AND dme_lat IS NULL
        UNION
        SELECT vhf_id AS id,lat,lon,mag_var,"DME" AS type FROM vhf_dmes WHERE dme_id IS NOT NULL
        UNION
        SELECT ndb_id AS id,lat,lon,mag_var,"NDB" AS type FROM ndbs
        UNION
        SELECT airport_id AS id,lat,lon,mag_var,"AIRPORT" as type FROM airports
    )
    SELECT p.*,lat,lon,mag_var,type
    FROM procedure_points AS p
    LEFT JOIN unified_table AS u ON p.fix_id = u.id
    WHERE fac_id = {fac_id} AND fac_sub_code={fac_sub_code} AND procedure_id LIKE {procedure_id} AND route_type IN ({route_type_string}) AND p.path_term NOT IN ({path_term_string})
    ORDER BY p.procedure_id,p.transition_id,p.route_type,p.sequence_number;
    """
    return result
