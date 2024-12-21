from sqlalchemy.orm import Session
from src.domain.strategy.strategy import Strategy
from src.infra.common.persistence.mapper import Mapper
from src.infra.common.persistence.repo import SqlalchemyRepository
from src.infra.strategy.persistance.strategy import StrategyEntity


class SqlAlchemyStrategyRepository(SqlalchemyRepository[StrategyEntity, Strategy]):
    def __init__(self, session: Session, mapper: Mapper[StrategyEntity, Strategy]):
        super().__init__(session, mapper, StrategyEntity)
