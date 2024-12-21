from src.domain.account.dto import AccountDto
from src.domain.common.exception import ExeptionType, InvestAppException
from src.domain.common.type import BrokerType
from src.infra.account.kis.account import KisAccount
from src.infra.account.persistence.account import AccountEntity
from src.infra.common.persistence.mapper import Mapper


class AccountMapper(Mapper[AccountEntity, AccountDto]):
    def to_model(self, entity: AccountEntity) -> AccountDto:
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

    def to_entity(self, dto: AccountDto) -> AccountEntity:
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

    def to_kis_domain(self, entity: AccountEntity) -> KisAccount:
        if entity.broker_type != BrokerType.KIS:
            raise InvestAppException(ExeptionType.INVALID_ACCOUNT_TYPE, entity.broker_type)
        return KisAccount(account_dto=self.to_model(entity))
