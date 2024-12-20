from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from src.domain.stock.stock_info import StockInfo
from src.infra.persistance.schemas.strategy import StrategyEntity


@dataclass
class Strategy:
    entity: StrategyEntity

    def get_invest_amount(self, balance: float) -> float:
        return balance * self.invest_rate

    def get_stocks(self) -> Dict[str, StockInfo]:
        return self.entity.stocks

    def complete_rebalance(self):
        self.entity.last_run = datetime.now()

    # 일단은 매달했는지 확인
    def has_rebalanced(self) -> bool:
        return self.entity.last_run is not None and self.run_this_month()

    def run_this_month(self):
        return datetime.now().date() == self.entity.last_run.date()
