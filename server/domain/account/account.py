from abc import ABC, abstractmethod
from pykis import KisAccount, KisBalance, PyKis
from pyupbit import Upbit
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
        self.account = account
        self.kis: PyKis = HantuAccount._create_kis_instance(account, is_virtual)
        self.kis_account = self.kis.account()
        self.kis_balance = self.kis_account.balance()

    def _create_kis_instance(account: AccountEntity, is_virtual: bool = False) -> PyKis:
        return PyKis(
            id=account.login_id,  # HTS 로그인 ID
            account=f"{account.number}-{account.product_code}",  # 계좌번호
            appkey=account.app_key,  # AppKey 36자리
            secretkey=account.secret_key,  # SecretKey 180자리
            virtual_id=account.login_id if is_virtual else None,  # 가상 계좌 ID
            virtual_appkey=account.app_key if is_virtual else None,  # 가상 AppKey
            virtual_secretkey=(
                account.secret_key if is_virtual else None
            ),  # 가상 SecretKey
            keep_token=True,  # API 접속 토큰 자동 저장
        )

    def get_balance(self) -> float:
        return self.kis_balance.withdrawable

    def buy_market_order(self, ticker: str, amount: float) -> None:
        self.kis_account.buy(ticker, amount)

    def get_stocks(self):
        return self.kis_account.stocks


class HantuRealAccount(HantuAccount):
    def __init__(self, account: AccountEntity):
        super().__init__(account)


class HantuVirtualAccount(HantuAccount):
    def __init__(self, account: AccountEntity):
        super().__init__(account, True)


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
