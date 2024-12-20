from time import sleep
import pyupbit
from pyupbit import Upbit

from src.domain.account.account import Account
from src.domain.account.dto import AccountDto
from src.domain.account.holdings import HoldingsInfo
from src.domain.common.exception import ExeptionType, InvestAppException
from src.domain.common.type import Market


class UpbitAccount(Account):
    def __init__(self, account_dto: AccountDto):
        super().__init__(account_dto=account_dto)
        self.upbit = Upbit(access=self.account_dto.app_key, secret=self.account_dto.secret_key)

    def get_balance(self, market: Market = Market.KR) -> float:
        stocks: list[dict] = self._get_balances()
        total_balance = 0.0

        for stock in stocks:
            if stock["currency"] == "KRW":
                total_balance += float(stock["balance"])
            else:
                sleep(0.1)
                current_price = float(pyupbit.get_current_price(f"KRW-{stock['currency']}"))
                total_balance += current_price * float(stock["balance"])

        return float(total_balance)

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
                eval_amt=round(float(stock["balance"]) * float(stock["avg_buy_price"]), 4),
            )
            for stock in self._get_balances()
        }

    def get_current_price(self, ticker: str) -> float:
        return pyupbit.get_current_price(ticker)

    def _get_balances(self) -> list[dict]:
        balances: dict | list = self.upbit.get_balances()

        if isinstance(balances, dict) and "error" in balances.keys():
            raise InvestAppException(ExeptionType.FAILED_TO_GET_BALANCE, balances.get("error"))

        return balances
