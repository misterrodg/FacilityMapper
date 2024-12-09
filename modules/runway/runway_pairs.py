from modules.runway.runway_pair import RunwayPair
from modules.db.runway_records import RunwayRecords


class RunwayPairs:
    def __init__(self, runway_records: RunwayRecords):
        self.runway_pairs: list[RunwayPair] = []

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
            reciprocal = runway_records.find_runway(runway_id, True)
            runway_pair = RunwayPair(
                base.airport_id,
                base.runway_id,
                base.lat,
                base.lon,
                base.displaced_threshold,
                reciprocal.runway_id,
                reciprocal.lat,
                reciprocal.lon,
                reciprocal.displaced_threshold,
            )
            self.runway_pairs.append(runway_pair)
        return
