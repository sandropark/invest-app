from dataclasses import dataclass

from src.domain.account.account import HoldingsInfo


@dataclass
class StockInfo:
    target_rate: float
    rebalance_qty: int = 0

    def to_dict(self):
        return {
            "target_rate": self.target_rate,
            "rebalance_qty": self.rebalance_qty,
        }

    def calculate_rebalance_amt(self, portfolio_target_amt: float, holdings: HoldingsInfo, current_price: float):
        # 종목 목표 금액
        stock_target_amt = portfolio_target_amt * self.target_rate
        rebalance_amt = stock_target_amt

        # 보유 종목이 있는 경우
        if holdings is not None:
            rebalance_amt -= holdings.eval_amt

        self.rebalance_qty = int(rebalance_amt / current_price)
