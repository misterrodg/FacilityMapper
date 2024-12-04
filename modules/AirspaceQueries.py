def select_controlled_points(airport_id: str) -> str:
    result = f"""
    SELECT * 
    FROM controlled_airspace_points 
    WHERE center_id = {airport_id}
    ORDER BY center_id, multiple_code, sequence_number;
    """
    return result


def select_restrictive_points(restrictive_id: str) -> str:
    result = f"""
    SELECT *
    FROM restrictive_airspace_points
    WHERE restrictive_designation = {restrictive_id}
    ORDER BY restrictive_designation, multiple_code, sequence_number;
    """
    return result
