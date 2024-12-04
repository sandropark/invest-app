from typing import List
from contextlib import contextmanager
from infra.persistance import engine
from infra.persistance.schemas.strategy import Strategy


@contextmanager
def get_db():
    db = engine.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save(strategy: Strategy) -> Strategy:
    with get_db() as db:
        db.add(strategy)
        db.commit()
        db.refresh(strategy)
        return strategy


def find_all() -> List[Strategy]:
    with get_db() as db:
        return db.query(Strategy).all()


def update(id: int, strategy: Strategy) -> Strategy:
    with get_db() as db:
        update_data = {
            key: value
            for key, value in strategy.__dict__.items()
            if not key.startswith("_") and key != "id"
        }

        db.query(Strategy).filter(Strategy.id == id).update(update_data)
        db.commit()

        return db.query(Strategy).get(id)


def get(id: int) -> Strategy:
    with get_db() as db:
        return db.query(Strategy).get(id)


def delete(id: int):
    with get_db() as db:
        db.query(Strategy).filter(Strategy.id == id).delete()
        db.commit()
