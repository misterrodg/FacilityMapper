from modules.db.restrictive_records import RestrictiveRecords
from modules.airspace.airspace_handler import get_line_strings
from modules.geo_json import FeatureCollection


def process_restrictive(restrictive_records: RestrictiveRecords) -> FeatureCollection:
    segmented_airspace_list = restrictive_records.get_segmented_line_definitions()
    feature_collection = get_line_strings(segmented_airspace_list)
    return feature_collection
