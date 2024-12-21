from typing import List

from sqlalchemy import delete, select, update
from src.domain.account.dto import AccountDto
from src.domain.type import BrokerType
from src.infra.persistance import engine
from src.infra.persistance.mapper import account_mapper
from src.infra.persistance.schemas.account import AccountEntity


def save(account: AccountDto) -> AccountDto:
    with engine.get_session() as session:
        session.add(account)
        session.commit()
        return account


def save_all(accounts_dtos: List[AccountDto]) -> List[AccountDto]:
    with engine.get_session() as session:
        [session.merge(account_mapper.to_entity(account_dto)) for account_dto in accounts_dtos]
        session.commit()
        return accounts_dtos


def find_all(broker_type: BrokerType = None) -> List[AccountDto]:
    with engine.get_session() as session:
        stmt = select(AccountEntity)
        if broker_type is not None:
            stmt = stmt.where(AccountEntity.broker_type == broker_type)
        return [account_mapper.to_dto(account_entity) for account_entity in session.scalars(stmt).all()]


def update(id: int, account: AccountDto) -> AccountDto:
    with engine.get_session() as session:
        stmt = update(AccountEntity).where(AccountEntity.id == id).values(account.__dict__)
        session.execute(stmt)
        session.commit()
        return account


def find_by_id(id: int) -> AccountDto:
    with engine.get_session() as session:
        account_entity = session.get(AccountEntity, id)
        return account_mapper.to_dto(account_entity)


def delete_by_id(id: int):
    with engine.get_session() as session:
        stmt = delete(AccountEntity).where(AccountEntity.id == id)
        session.execute(stmt)
        session.commit()
        return id
