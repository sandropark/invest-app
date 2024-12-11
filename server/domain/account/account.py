from abc import ABC, abstractmethod
from pyupbit import Upbit

from infra.kis import kis_client
from infra.kis.dto import KisInfo
from infra.persistance.schemas.account import AccountEntity


class Account(ABC):
    @abstractmethod
    def get_balance(self) -> float:
        pass

    @abstractmethod
    def buy_market_order(self, ticker: str, amount: float) -> None:
        pass

    @abstractmethod
    def get_stocks(self):
        pass


class HantuAccount(Account):
    def __init__(self, account: AccountEntity, is_virtual: bool = False):
        self.account: AccountEntity = account
        self.is_virtual: bool = is_virtual

    def get_balance(self) -> float:
        return kis_client.get_balance(self._kis_info())

    def buy_market_order(self, ticker: str, amount: float) -> None:
        pass

    def get_stocks(self):
        pass

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

    def get_balance(self) -> float:
        return self.upbit.get_balance_t()

    def buy_market_order(self, ticker: str, amount: float) -> None:
        self.upbit.buy_market_order(ticker, amount)

    def get_stocks(self):
        return self.upbit.get_balances()
