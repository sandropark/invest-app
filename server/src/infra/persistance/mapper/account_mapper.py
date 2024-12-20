from src.domain.account.account import Account
from src.domain.exception import InvestAppException
from src.domain.type import BrokerType
from src.infra.kis.account import KisAccount
from src.infra.persistance.schemas.account import AccountEntity


def to_domain(entity: AccountEntity) -> Account:
    return Account(account=entity)


def to_kis_domain(entity: AccountEntity) -> KisAccount:
    if entity.broker_type != BrokerType.KIS:
        raise InvestAppException("KIS 계좌가 아닙니다.", 400, entity.broker_type)
    return KisAccount(account=entity)
