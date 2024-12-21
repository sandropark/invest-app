from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, TypeVar

from src.domain.common.type import Market


M = TypeVar("M")


class Repository[M](ABC):
    @abstractmethod
    def save(self, model: M) -> M:
        pass

    @abstractmethod
    def update(self, id: int, model: M) -> M:
        pass

    @abstractmethod
    def delete_by_id(self, id: int) -> int:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> M | None:
        pass

    @abstractmethod
    def find_all(self) -> List[M]:
        pass


class StockMarketClient(ABC):
    @abstractmethod
    def is_market_open(self, market: Market) -> bool:
        pass


class TimeHolder(ABC):
    @abstractmethod
    def get_now(self) -> datetime:
        pass
