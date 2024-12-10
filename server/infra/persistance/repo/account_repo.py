from typing import List
from contextlib import contextmanager
from domain.type import BrokerType
from infra.persistance import engine
from infra.persistance.schemas.account import AccountEntity


@contextmanager
def get_db():
    db = engine.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save(account: AccountEntity) -> AccountEntity:
    with get_db() as db:
        db.add(account)
        db.commit()
        db.refresh(account)
        return account


def save_all(accounts: List[AccountEntity]) -> List[AccountEntity]:
    with get_db() as db:
        db.add_all(accounts)
        db.commit()
        return accounts


def find_all(broker_type: BrokerType = None) -> List[AccountEntity]:
    with get_db() as db:
        if broker_type is None:
            return db.query(AccountEntity).all()
        return (
            db.query(AccountEntity)
            .filter(AccountEntity.broker_type == broker_type)
            .all()
        )


def update(id: int, account: AccountEntity) -> AccountEntity:
    with get_db() as db:
        update_data = {
            key: value
            for key, value in account.__dict__.items()
            if not key.startswith("_") and key != "id"
        }

        db.query(AccountEntity).filter(AccountEntity.id == id).update(update_data)
        db.commit()

        return db.query(AccountEntity).get(id)


def get(id: int) -> AccountEntity:
    with get_db() as db:
        account = db.query(AccountEntity).get(id)
        assert account is not None, f"계좌가 존재하지 않습니다. id={id}"
        return account


def delete(id: int):
    with get_db() as db:
        db.query(AccountEntity).filter(AccountEntity.id == id).delete()
        db.commit()
