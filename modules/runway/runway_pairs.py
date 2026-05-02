from modules.runway import RunwayPair, inverse_runway
from modules.db.runway_records import RunwayRecords


class RunwayPairs:
    runway_pairs: list[RunwayPair]

    def __init__(self, runway_records: RunwayRecords) -> None:
        self.runway_pairs = []

        self._pair_runways(runway_records)

    def get_runway_pairs(self) -> list[RunwayPair]:
        return self.runway_pairs

    def _pair_runways(self, runway_records: RunwayRecords) -> None:
        records = runway_records.get_records()
        runway_end_count = len(records)
        runway_count = int(runway_end_count / 2)
        runway_bases = records[:runway_count]
        for base in runway_bases:
            runway_id = base.runway_id
            airport_id = base.airport_id
            base_lat = base.lat
            base_lon = base.lon
            if (
                runway_id is None
                or airport_id is None
                or base_lat is None
                or base_lon is None
            ):
                continue

            reciprocal_id = inverse_runway(runway_id)
            reciprocal = runway_records.find_runway(reciprocal_id)
            if reciprocal is None:
                continue

            reciprocal_runway_id = reciprocal.runway_id
            reciprocal_lat = reciprocal.lat
            reciprocal_lon = reciprocal.lon
            if (
                reciprocal_runway_id is None
                or reciprocal_lat is None
                or reciprocal_lon is None
            ):
                continue

            runway_pair = RunwayPair(
                airport_id,
                runway_id,
                base_lat,
                base_lon,
                base.displaced_threshold if base.displaced_threshold is not None else 0,
                reciprocal_runway_id,
                reciprocal_lat,
                reciprocal_lon,
                reciprocal.displaced_threshold
                if reciprocal.displaced_threshold is not None
                else 0,
            )
            self.runway_pairs.append(runway_pair)
        return
