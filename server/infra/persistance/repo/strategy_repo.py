from typing import List
from contextlib import contextmanager
from infra.persistance import engine
from infra.persistance.schemas.strategy import StrategyEntity


@contextmanager
def get_db():
    db = engine.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save(strategy: StrategyEntity) -> StrategyEntity:
    with get_db() as db:
        db.add(strategy)
        db.commit()
        db.refresh(strategy)
        return strategy


def find_all() -> List[StrategyEntity]:
    with get_db() as db:
        return db.query(StrategyEntity).all()


def update(id: int, strategy: StrategyEntity) -> StrategyEntity:
    with get_db() as db:
        update_data = {
            key: value
            for key, value in strategy.__dict__.items()
            if not key.startswith("_") and key != "id"
        }

        db.query(StrategyEntity).filter(StrategyEntity.id == id).update(update_data)
        db.commit()

        return db.query(StrategyEntity).get(id)


def get(id: int) -> StrategyEntity:
    with get_db() as db:
        return db.query(StrategyEntity).get(id)


def delete(id: int):
    with get_db() as db:
        db.query(StrategyEntity).filter(StrategyEntity.id == id).delete()
        db.commit()
