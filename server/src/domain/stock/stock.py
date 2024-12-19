from src.domain.account.account import HoldingsInfo


class StockInfo:
    def __init__(self, target_rate: float, rebalance_amt: int = 0):
        self.target_rate: float = target_rate  # 목표 비중
        self.rebalance_amt: int = rebalance_amt  # 리밸런스 수량

    def to_dict(self):
        return {
            "target_rate": self.target_rate,
            "rebalance_amt": self.rebalance_amt,
        }

    def calculate_rebalance_amount(self, invest_amount: float, holdings: HoldingsInfo, current_price: float):
        if holdings is None:
            self.rebalance_amt = invest_amount * self.target_rate / current_price
            return
