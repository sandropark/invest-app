from src.domain.account.account_provider import RealAccountProvider


account_provider = RealAccountProvider()


def test_get_current_price_real_kr():
    account = account_provider.get_account(1)
    current_price = account.get_current_price("005930")

    assert isinstance(current_price, (int, float))
    assert current_price > 0


def test_get_current_price_real_us():
    account = account_provider.get_account(1)
    current_price = account.get_current_price("AAPL")

    assert isinstance(current_price, (int, float))
    assert current_price > 0


def test_get_current_price_virtual_kr():
    account = account_provider.get_account(2)
    current_price = account.get_current_price("005930")

    assert isinstance(current_price, (int, float))
    assert current_price > 0


def test_get_current_price_virtual_us():
    account = account_provider.get_account(2)
    current_price = account.get_current_price("AAPL")

    assert isinstance(current_price, (int, float))
    assert current_price > 0


def test_get_current_price_upbit():
    account = account_provider.get_account(3)
    current_price = account.get_current_price("KRW-BTC")

    assert isinstance(current_price, (int, float))
    assert current_price > 0


def test_get_balance_kr():
    account = account_provider.get_account(2)
    balance = account.get_balance()

    assert isinstance(balance, (int, float))
    assert balance >= 0
