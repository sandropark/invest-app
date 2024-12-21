from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from src.domain.strategy.strategy import Strategy
from src.domain.type import Market


class StockMarketClient(ABC):
    @abstractmethod
    def is_market_open(self, market: Market) -> bool:
        pass


class StrategyRepository(ABC):
    @abstractmethod
    def save(self, dto: Strategy) -> Strategy:
        pass

    @abstractmethod
    def update(self, id: int, dto: Strategy) -> Strategy:
        pass

    @abstractmethod
    def delete_by_id(self, id: int) -> int:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Strategy | None:
        pass

    @abstractmethod
    def find_all(self) -> List[Strategy]:
        pass


class TimeHolder(ABC):
    @abstractmethod
    def get_now(self) -> datetime:
        pass
