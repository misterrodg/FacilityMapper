from modules.db.controlled_records import ControlledRecords
from modules.airspace.airspace_handler import get_line_strings
from modules.geo_json import FeatureCollection


def process_controlled(controlled_records: ControlledRecords) -> FeatureCollection:
    segmented_airspace_list = controlled_records.get_segmented_line_definitions()
    feature_collection = get_line_strings(segmented_airspace_list)
    return feature_collection
