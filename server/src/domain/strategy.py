from dataclasses import dataclass
from typing import Dict

from infra.persistance.schemas.strategy import StockInfo


@dataclass
class Strategy:
    name: str
    stocks: Dict[str, StockInfo]
    _invest_rate: float

    def get_invest_amount(self, balance: float) -> float:
        return balance * self.invest_rate
