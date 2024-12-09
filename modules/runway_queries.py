def select_runways_by_airport_id(airport_id: str) -> str:
    result = f"""
    SELECT airport_id,runway_id,lat,lon,displaced_threshold FROM runways WHERE airport_id = {airport_id} ORDER BY runway_id;
    """
    return result
