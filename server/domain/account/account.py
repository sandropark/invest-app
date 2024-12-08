from abc import ABC, abstractmethod
from pykis import KisAccount, KisBalance, PyKis
from pyupbit import Upbit
from domain.exception import InvestAppException
from infra.persistance.schemas.account import AccountEntity


class Account(ABC):
    @abstractmethod
    def get_balance(self) -> float:
        pass


class KisAccount(Account):
    def __init__(self, account: AccountEntity, is_virtual: bool = False):
        self.account = account
        self.kis: PyKis = KisAccount._create_kis_instance(account, is_virtual)

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
        kis_account: KisAccount = self.kis.account()
        kis_balance: KisBalance = kis_account.balance()
        return kis_balance.withdrawable


class KISRealAccount(KisAccount):
    def __init__(self, account: AccountEntity):
        super().__init__(account)


class KISVirtualAccount(KisAccount):
    def __init__(self, account: AccountEntity):
        super().__init__(account, True)


class UpbitAccount(Account):
    def __init__(self, account: AccountEntity):
        self.account = account
        self.upbit: Upbit = Upbit(access=account.app_key, secret=account.secret_key)

    def get_balance(self) -> float:
        return self.upbit.get_balance_t()
