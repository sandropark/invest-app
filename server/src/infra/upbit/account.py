from time import sleep
import pyupbit
from pyupbit import Upbit

from src.domain.account.account import Account
from src.domain.account.holdings import HoldingsInfo
from src.domain.type import Market
from src.infra.persistance.schemas.account import AccountEntity


class UpbitAccount(Account):
    def __init__(self, account: AccountEntity):
        super().__init__(account=account)
        self.upbit = Upbit(access=self.account.app_key, secret=self.account.secret_key)

    def get_balance(self, market: Market = Market.KR) -> float:
        stocks: list[dict] = self.upbit.get_balances()
        total_balance = 0.0

        for stock in stocks:
            if stock["currency"] == "KRW":
                total_balance += float(stock["balance"])
            else:
                sleep(0.1)
                current_price = float(pyupbit.get_current_price(f"KRW-{stock['currency']}"))
                total_balance += current_price * float(stock["balance"])

        return total_balance

    def buy_market_order(self, ticker: str, amount: float) -> None:
        self.upbit.buy_market_order(ticker, amount)

    def sell_market_order(self, ticker: str, amount: float) -> None:
        self.upbit.sell_market_order(ticker, amount)

    def get_holdings(self) -> dict[str, HoldingsInfo]:
        return {
            stock["currency"]: HoldingsInfo(
                name=stock["currency"],
                quantity=float(stock["balance"]),
                avg_price=float(stock["avg_buy_price"]),
            )
            for stock in self.upbit.get_balances()
        }

    def get_current_price(self, ticker: str) -> float:
        return pyupbit.get_current_price(ticker)
