from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from src.domain.common.type import Market
from src.domain.strategy.interval import Interval
from src.domain.strategy.stock_info import StockInfo


@dataclass
class Strategy:
    id: int
    name: str
    invest_rate: float
    market: Market
    stocks: Dict[str, StockInfo]
    interval: Interval
    last_run: datetime
    account_id: int

    def get_invest_amount(self, balance: float) -> float:
        return balance * self.invest_rate

    def get_stocks(self) -> Dict[str, StockInfo]:
        return self.stocks

    def complete_rebalance(self):
        self.last_run = datetime.now()

    # TODO: 고도화 하기.
    def is_time_to_rebalance(self, now: datetime) -> bool:
        if self.last_run is None:
            return True

        interval: Interval = self.interval
        if interval.is_month():
            this_month = now.month
            return this_month in interval.value and not self._run_this_month(now)

        # TODO: 다른 조건 추가하기
        return False

    def _run_this_month(self, now: datetime):
        return now.month == self.last_run.month

    def get_market(self) -> Market:
        return self.market

    def get_account_id(self) -> int:
        return self.account_id
