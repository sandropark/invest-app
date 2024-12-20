from abc import ABC, abstractmethod

from src.domain.account.dto import AccountDto
from src.domain.account.holdings import HoldingsInfo
from src.domain.common.type import Market


class Account(ABC):
    def __init__(self, account_dto: AccountDto):
        self.account_dto: AccountDto = account_dto

    @abstractmethod
    def get_balance(self, market: Market = Market.KR) -> float:
        pass

    @abstractmethod
    def buy_market_order(self, ticker: str, amount: float) -> None:
        pass

    @abstractmethod
    def sell_market_order(self, ticker: str, amount: float) -> None:
        pass

    @abstractmethod
    def get_holdings(self) -> dict[str, HoldingsInfo]:
        pass

    @abstractmethod
    def get_current_price(self, ticker: str) -> float:
        pass
