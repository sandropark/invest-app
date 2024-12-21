from typing import List
from pytest import Session
from sqlalchemy import select
from src.domain.account.dto import AccountDto
from src.domain.common.type import BrokerType
from src.infra.common.persistence.mapper import Mapper
from src.infra.common.persistence.repo import SqlalchemyRepository
from src.infra.account.persistence.account import AccountEntity


class SqlAlchemyAccountRepository(SqlalchemyRepository[AccountEntity, AccountDto]):
    def __init__(self, session: Session, mapper: Mapper[AccountEntity, AccountDto]):
        super().__init__(session, mapper, AccountEntity)

    def find_all(self, broker_type: BrokerType = None) -> List[AccountDto]:
        stmt = select(self.entity_type)
        if broker_type is not None:
            stmt = stmt.where(self.entity_type.broker_type == broker_type)
        return [self.mapper.to_model(entity) for entity in self.session.scalars(stmt).all()]

    def upsert_all(self, accounts_dtos: List[AccountDto]) -> List[AccountDto]:
        with self.session as session:
            [session.merge(self.mapper.to_entity(account_dto)) for account_dto in accounts_dtos]
            session.commit()
            return accounts_dtos
