from dependency_injector import containers, providers
from src.domain.account.account_provider import RealAccountProvider
from src.domain.common.time_holder import TimeHolderImpl
from src.infra.common.stock_market import StockMarketClientImpl
from src.infra.persistance import engine
from src.infra.persistance.mapper.account_mapper import AccountMapper
from src.infra.persistance.mapper.strategy_mapper import StrategyMapper
from src.infra.persistance.repo.account_repo import SqlAlchemyAccountRepository
from src.infra.persistance.repo.strategy_repo import SqlAlchemyStrategyRepository
from src.domain.strategy.strategy_service import StrategyService


class Container(containers.DeclarativeContainer):
    _instance = None

    def __init__(self):
        self.init_resources()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    config = providers.Configuration()

    session = providers.Singleton(engine.get_session)
    strategy_mapper = providers.Singleton(StrategyMapper)
    strategy_repository = providers.Singleton(
        SqlAlchemyStrategyRepository,
        session=session,
        mapper=strategy_mapper,
    )

    account_mapper = providers.Singleton(AccountMapper)
    account_repository = providers.Singleton(
        SqlAlchemyAccountRepository,
        session=session,
        mapper=account_mapper,
    )

    account_provider = providers.Singleton(RealAccountProvider, account_repository=account_repository)

    stock_market_client = providers.Singleton(StockMarketClientImpl)
    time_holder = providers.Singleton(TimeHolderImpl)

    strategy_service = providers.Singleton(
        StrategyService,
        stock_market_client=stock_market_client,
        time_holder=time_holder,
        account_provider=account_provider,
        strategy_repo=strategy_repository,
    )
