from typing import List
from contextlib import contextmanager
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


def find_all() -> List[AccountEntity]:
    with get_db() as db:
        return db.query(AccountEntity).all()


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
        return db.query(AccountEntity).get(id)


def delete(id: int):
    with get_db() as db:
        db.query(AccountEntity).filter(AccountEntity.id == id).delete()
        db.commit()
