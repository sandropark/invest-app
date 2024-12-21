from typing import List
from sqlalchemy import delete, select, update
from src.domain.port import StrategyRepository
from src.domain.strategy.strategy import Strategy
from src.infra.persistance import engine
from src.infra.persistance.mapper import strategy_mapper
from src.infra.persistance.schemas.strategy import StrategyEntity


class StrategyRepositoryImpl(StrategyRepository):
    def save(self, dto: Strategy) -> Strategy:
        with engine.get_session() as session:
            entity = strategy_mapper.dto_to_entity(dto)
            session.add(entity)
            session.commit()
            return dto

    def update(self, id: int, domain: Strategy) -> Strategy:
        with engine.get_session() as session:
            stmt = update(StrategyEntity).where(StrategyEntity.id == id).values(domain.__dict__)
            session.execute(stmt)
            session.commit()
            return domain

    def delete_by_id(self, id: int) -> int:
        with engine.get_session() as session:
            stmt = delete(StrategyEntity).where(StrategyEntity.id == id)
            session.execute(stmt)
            session.commit()
            return id

    def find_by_id(self, id: int) -> Strategy | None:
        with engine.get_session() as session:
            entity = session.get(StrategyEntity, id)
            if entity is None:
                return None
            return strategy_mapper.entity_to_dto(entity)

    def find_all(self) -> List[Strategy]:
        with engine.get_session() as session:
            stmt = select(StrategyEntity)
            entities = session.scalars(stmt).all()
            return [strategy_mapper.entity_to_dto(entity) for entity in entities]
