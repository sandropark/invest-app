from src.domain.strategy.strategy import Strategy
from src.infra.persistance.schemas.strategy import StrategyEntity
from src.infra.persistance.mapper.mapper import Mapper


class StrategyMapper(Mapper[StrategyEntity, Strategy]):
    def to_entity(self, model: Strategy) -> StrategyEntity:
        return StrategyEntity(
            id=model.id,
            name=model.name,
            invest_rate=model.invest_rate,
            market=model.market,
            stocks=model.stocks,
            interval=model.interval,
            last_run=model.last_run,
            account_id=model.account_id,
        )

    def to_model(self, entity: StrategyEntity) -> Strategy:
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
