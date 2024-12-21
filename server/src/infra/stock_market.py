from datetime import datetime
import exchange_calendars as market_calendar

from src.domain.port import StockMarketClient
from src.domain.type import Market


class StockMarketClientImpl(StockMarketClient):
    def is_market_open(self, market: Market):
        if market.is_kr():
            return market_calendar.get_calendar("XKRX").is_session(datetime.now().date())
        return market_calendar.get_calendar("XNYS").is_session(datetime.now().date())
