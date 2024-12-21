from src.domain.account.dto import AccountDto
from src.domain.exception import InvestAppException
from src.domain.type import BrokerType
from src.infra.kis.account import KisAccount
from src.infra.persistance.schemas.account import AccountEntity


def to_dto(entity: AccountEntity) -> AccountDto:
    return AccountDto(
        id=entity.id,
        name=entity.name,
        app_key=entity.app_key,
        secret_key=entity.secret_key,
        broker_type=entity.broker_type,
        number=entity.number,
        product_code=entity.product_code,
        login_id=entity.login_id,
        url_base=entity.url_base,
        is_virtual=entity.is_virtual,
        token=entity.token,
    )


def to_entity(dto: AccountDto) -> AccountEntity:
    return AccountEntity(
        id=dto.id,
        name=dto.name,
        app_key=dto.app_key,
        secret_key=dto.secret_key,
        broker_type=dto.broker_type,
        number=dto.number,
        product_code=dto.product_code,
        login_id=dto.login_id,
        url_base=dto.url_base,
        is_virtual=dto.is_virtual,
        token=dto.token,
    )


def to_kis_domain(entity: AccountEntity) -> KisAccount:
    if entity.broker_type != BrokerType.KIS:
        raise InvestAppException("KIS 계좌가 아닙니다.", 400, entity.broker_type)
    return KisAccount(account_dto=to_dto(entity))
