class StockInfo:
    def __init__(self, target_rate: float, rebalance_amt: int = 0):
        self.target_rate: float = target_rate
        self.rebalance_amt: int = rebalance_amt

    def to_dict(self):
        return {
            "target_rate": self.target_rate,
            "rebalance_amt": self.rebalance_amt,
        }
