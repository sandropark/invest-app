from src.domain.account.account import HoldingsInfo


class StockInfo:
    def __init__(self, target_rate: float, rebalance_qty: int = 0):
        self.target_rate: float = target_rate  # 목표 비중
        self.rebalance_qty: int = rebalance_qty  # 리밸런스 수량

    def to_dict(self):
        return {
            "target_rate": self.target_rate,
            "rebalance_amt": self.rebalance_qty,
        }

    def calculate_rebalance_amount(self, portfolio_target_amt: float, holdings: HoldingsInfo, current_price: float):
        # 종목 목표 금액
        stock_target_amt = portfolio_target_amt * self.target_rate
        rebalance_amt = stock_target_amt

        # 보유 종목이 있는 경우
        if holdings is not None:
            rebalance_amt -= holdings.eval_amt

        self.rebalance_qty = int(rebalance_amt / current_price)
