from src.domain.strategy import Strategy
from src.infra.persistance.mapper import account_mapper
from src.infra.persistance.schemas.strategy import StrategyEntity


def to_domain(entity: StrategyEntity) -> Strategy:
    return Strategy(strategy=entity, account=account_mapper.to_domain(entity.account))
