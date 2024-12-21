from sqlalchemy.orm import Session
from src.domain.strategy.strategy import Strategy
from src.infra.persistance.mapper.mapper import Mapper
from src.infra.persistance.repo.repo import SqlalchemyRepository
from src.infra.persistance.schemas.strategy import StrategyEntity


class SqlAlchemyStrategyRepository(SqlalchemyRepository[StrategyEntity, Strategy]):
    def __init__(self, session: Session, mapper: Mapper[StrategyEntity, Strategy]):
        super().__init__(session, mapper, StrategyEntity)
