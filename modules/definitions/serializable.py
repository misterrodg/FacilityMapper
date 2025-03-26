from abc import ABC, abstractmethod


class Serializable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass
