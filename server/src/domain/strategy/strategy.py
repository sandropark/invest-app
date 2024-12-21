from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from src.domain.stock.stock_info import StockInfo
from src.domain.type import Market
from src.infra.persistance.schemas.strategy import StrategyEntity, Interval


@dataclass
class Strategy:
    entity: StrategyEntity

    def get_invest_amount(self, balance: float) -> float:
        return balance * self.invest_rate

    def get_stocks(self) -> Dict[str, StockInfo]:
        return self.entity.stocks

    def complete_rebalance(self):
        self.entity.last_run = datetime.now()

    # TODO: 고도화 하기.
    def is_time_to_rebalance(self, now: datetime) -> bool:
        if self.entity.last_run is None:
            return True

        interval: Interval = self.entity.interval
        if interval.is_month():
            this_month = now.month
            return this_month in interval.value and not self._run_this_month(now)

        # TODO: 다른 조건 추가하기
        return False

    def _run_this_month(self, now: datetime):
        return now.month == self.entity.last_run.month

    def get_market(self) -> Market:
        return self.entity.market

    def get_account_id(self) -> int:
        return self.entity.account_id
