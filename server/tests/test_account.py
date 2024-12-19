from src.domain.account import account_service
from src.domain.type import Market


def test_get_current_price_1():
    current_price = account_service.get_current_price(account_id=1, ticker="005930")
    assert isinstance(current_price, (int, float))
    assert current_price > 0


def test_get_current_price_2():
    current_price = account_service.get_current_price(account_id=3, ticker="KRW-BTC")
    assert isinstance(current_price, (int, float))
    assert current_price > 0


def test_get_balance_kr():
    balance = account_service.get_balance(account_id=2)
    assert isinstance(balance, (int, float))
    assert balance >= 0
