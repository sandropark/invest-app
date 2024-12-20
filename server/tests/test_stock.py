from src.domain.account.account import HoldingsInfo
from src.domain.stock.stock_info import StockInfo


# 해당 종목을 보유하지 않은 경우
def test_calculate_rebalance_amount_with_no_holdings():
    stock = StockInfo(target_rate=0.5)
    stock.calculate_rebalance_amt(
        portfolio_target_amt=100_000, holdings=None, current_price=10_000
    )
    assert stock.rebalance_qty == 5


# 해당 종목을 보유하고 있는 경우
def test_calculate_rebalance_amount_with_holdings():
    stock = StockInfo(target_rate=0.5)
    stock.calculate_rebalance_amt(
        portfolio_target_amt=100_000,
        holdings=_create_holdings(50_000),
        current_price=10_000,
    )
    assert stock.rebalance_qty == 0


# 매도해야 하는 경우
def test_calculate_rebalance_amount_with_holdings_and_diff():
    stock = StockInfo(target_rate=0.5)
    stock.calculate_rebalance_amt(
        portfolio_target_amt=100_000,
        holdings=_create_holdings(60_000),
        current_price=10_000,
    )
    assert stock.rebalance_qty == -1


# 종목 할당 금액보다 평가 금액이 더 크지만, 매도 수량이 1보다 작은 경우
def test_calculate_rebalance_amount_with_holdings_and_diff_and_negative():
    stock = StockInfo(target_rate=0.5)
    stock.calculate_rebalance_amt(
        portfolio_target_amt=100_000,
        holdings=_create_holdings(59_999),
        current_price=10_000,
    )
    assert stock.rebalance_qty == 0


def _create_holdings(eval_amt: int, quantity: int = 10):
    return HoldingsInfo(
        name="test", quantity=quantity, avg_price=10_000, eval_amt=eval_amt
    )
