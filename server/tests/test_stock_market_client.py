from src.domain.type import Market
from src.infra.stock_market import stock_market_client


def test_is_market_open():
    assert stock_market_client.is_market_open(Market.KR) == True
    assert stock_market_client.is_market_open(Market.US) == True
