from src.domain.account import account_service


def test_get_current_price():
    current_price = account_service.get_current_price(account_id=1, ticker="005930")
    assert isinstance(current_price, (int, float))
    assert current_price > 0
