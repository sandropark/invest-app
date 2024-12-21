from dependency_injector import containers, providers
from src.domain.account.account_provider import RealAccountProvider
from src.domain.time_holder import TimeHolderImpl
from src.infra.persistance.repo.strategy_repo import StrategyRepositoryImpl
from src.infra.stock_market import StockMarketClientImpl
from src.domain.strategy.strategy_service import StrategyService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    stock_market_client = providers.Singleton(StockMarketClientImpl)
    time_holder = providers.Singleton(TimeHolderImpl)
    account_provider = providers.Singleton(RealAccountProvider)
    strategy_repository = providers.Singleton(StrategyRepositoryImpl)

    strategy_service = providers.Singleton(
        StrategyService,
        stock_market_client=stock_market_client,
        time_holder=time_holder,
        account_provider=account_provider,
        strategy_repo=strategy_repository,
    )
