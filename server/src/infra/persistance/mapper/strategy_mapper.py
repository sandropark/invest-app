from src.domain.strategy.strategy import Strategy
from src.infra.persistance.schemas.strategy import StrategyEntity


def entity_to_dto(entity: StrategyEntity) -> Strategy:
    return Strategy(
        id=entity.id,
        name=entity.name,
        invest_rate=entity.invest_rate,
        market=entity.market,
        stocks=entity.stocks,
        interval=entity.interval,
        last_run=entity.last_run,
        account_id=entity.account_id,
    )


def dto_to_entity(domain: Strategy) -> StrategyEntity:
    return StrategyEntity(
        id=domain.id,
        name=domain.name,
        invest_rate=domain.invest_rate,
        market=domain.market,
        stocks=domain.stocks,
        interval=domain.interval,
        last_run=domain.last_run,
        account_id=domain.account_id,
    )
