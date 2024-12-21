from abc import ABC, abstractmethod
from typing import TypeVar

M = TypeVar("M")
E = TypeVar("E")


class Mapper[E, M](ABC):
    @abstractmethod
    def to_entity(self, model: M) -> E:
        pass

    @abstractmethod
    def to_model(self, entity: E) -> M:
        pass
