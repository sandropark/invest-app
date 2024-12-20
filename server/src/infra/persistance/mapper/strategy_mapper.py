from src.domain.strategy.strategy import Strategy
from src.infra.persistance.schemas.strategy import StrategyEntity


def to_domain(entity: StrategyEntity) -> Strategy:
    return Strategy(strategy=entity)
