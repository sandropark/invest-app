from abc import ABC, abstractmethod


from src.domain.account.account import Account
from src.domain.account.dto import AccountDto
from src.domain.exception import InvestAppException
from src.domain.type import BrokerType
from src.infra.kis.account import KisRealAccount, KisVirtualAccount
from src.infra.persistance.repo import account_repo
from src.infra.upbit.account import UpbitAccount


class AccountProvider(ABC):
    @abstractmethod
    def get_account(self, account_id: int) -> Account:
        pass


class RealAccountProvider(AccountProvider):
    kis_real: Account = None
    kis_virtual: Account = None
    upbit: Account = None

    def get_account(self, account_id: int) -> Account:
        account_dto: AccountDto = account_repo.find_by_id(account_id)

        if account_dto.broker_type == BrokerType.KIS and not account_dto.is_virtual:
            if self.kis_real is None:
                self.kis_real = KisRealAccount(account_dto)
            return self.kis_real

        if account_dto.broker_type == BrokerType.KIS and account_dto.is_virtual:
            if self.kis_virtual is None:
                self.kis_virtual = KisVirtualAccount(account_dto)
            return self.kis_virtual

        if account_dto.broker_type == BrokerType.UPBIT:
            if self.upbit is None:
                self.upbit = UpbitAccount(account_dto)
            return self.upbit

        raise InvestAppException("지원하지 않는 계좌 종류입니다. {}", 400, account_dto.broker_type)
