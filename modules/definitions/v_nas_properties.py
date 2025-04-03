from modules.definitions.serializable import Serializable
from modules.v_nas import (
    BCG_MIN,
    BCG_MAX,
    FILTER_MIN,
    FILTER_MAX,
)


class vNASProperties(Serializable):
    def __init__(self, bcg: int, filters: list):
        self.bcg = bcg
        self.filters = filters

        self._process()

    def _verify_bcg(self) -> None:
        if self.bcg and not (self.bcg >= BCG_MIN and self.bcg <= BCG_MAX):
            self.bcg = None
        return

    def _verify_filters(self) -> None:
        if self.filters and (
            isinstance(self.filters, list)
            or all(isinstance(item, int) for item in self.filters)
        ):
            filters = []
            for item in self.filters:
                if item >= FILTER_MIN and item <= FILTER_MAX:
                    filters.append(item)
            self.filters = filters if len(filters) > 0 else None
        return

    def _process(self) -> None:
        self._verify_bcg()
        self._verify_filters()

    def to_dict(self) -> dict:
        return {"bcg": self.bcg, "filters": self.filters}
