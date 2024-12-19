from abc import ABC, abstractmethod
from time import sleep
import pyupbit
from pyupbit import Upbit

from src.infra.kis import kis_client
from src.infra.kis.dto import KisInfo
from src.infra.persistance.schemas.account import AccountEntity
from src.domain.type import Market


class HoldingsInfo:
    def __init__(self, name: str, quantity: float, avg_price: float, eval_amt: float):
        self.name: str = name  # 종목명
        self.quantity: float = quantity  # 보유수량
        self.avg_price: float = avg_price  # 평단가
        self.eval_amt: float = eval_amt  # 평가금액


class Account(ABC):
    @abstractmethod
    def get_balance(self, market: Market = Market.KR) -> float:
        pass

    @abstractmethod
    def buy_market_order(self, ticker: str, amount: float) -> None:
        pass

    @abstractmethod
    def get_holdings(self) -> dict[str, HoldingsInfo]:
        pass

    @abstractmethod
    def get_current_price(self, ticker: str) -> float:
        pass


class HantuAccount(Account):
    def __init__(self, account: AccountEntity, is_virtual: bool = False):
        self.account: AccountEntity = account
        self.is_virtual: bool = is_virtual

    def get_balance(self, market: Market = Market.KR) -> float:
        return kis_client.get_balance(self._kis_info(), market)

    def buy_market_order(self, ticker: str, amount: float) -> None:
        pass

    def get_holdings(self) -> dict[str, HoldingsInfo]:
        return {
            stock["pdno"]: HoldingsInfo(
                name=stock["prdt_name"],
                quantity=float(stock["hldg_qty"]),
                avg_price=float(stock["pchs_avg_pric"]),
                eval_amount=float(stock["evl_amt"]),
            )
            for stock in kis_client.get_stocks(self._kis_info())
        }

    def get_current_price(self, ticker: str) -> float:
        return kis_client.get_current_price(self._kis_info(), ticker)

    def _kis_info(self):
        return KisInfo(
            token=self.account.get_access_token(),
            app_key=self.account.app_key,
            secret_key=self.account.secret_key,
            url_base=self.account.url_base,
            account_number=self.account.number,
            product_code=self.account.product_code,
            is_real=not self.is_virtual,
        )


class HantuRealAccount(HantuAccount):
    def __init__(self, account: AccountEntity):
        super().__init__(account=account)


class HantuVirtualAccount(HantuAccount):
    def __init__(self, account: AccountEntity):
        super().__init__(account=account, is_virtual=True)


class UpbitAccount(Account):
    def __init__(self, account: AccountEntity):
        self.account = account
        self.upbit: Upbit = Upbit(access=account.app_key, secret=account.secret_key)

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
