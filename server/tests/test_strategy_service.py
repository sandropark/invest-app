from datetime import datetime
from typing import Dict, List
from src.containers import Container
from src.domain.account.account import Account
from src.domain.account.account_provider import AccountProvider
from src.domain.account.holdings import HoldingsInfo
from src.domain.port import StockMarketClient, StrategyRepository, TimeHolder
from src.domain.strategy.stock_info import StockInfo
from src.domain.strategy.strategy import Strategy
from src.domain.strategy.strategy_service import StrategyService
from src.domain.type import Market, TimeUnit
from src.infra.persistance.schemas.account import AccountEntity
from src.infra.persistance.schemas.strategy import Interval


# 리밸런스 테스트
def test_rebalance():
    # Given
    container = Container()

    strategy_repo = FakeStrategyRepository()
    container.stock_market_client.override(FakeStockMarketClient())
    container.time_holder.override(FakeTimeHolder())
    container.account_provider.override(FakeAccountProvider())
    container.strategy_repository.override(strategy_repo)

    strategy = Strategy(
        id=None,
        name="정적 자산 배분",
        invest_rate=1,
        stocks={"spy": StockInfo(target_rate=1)},
        market=Market.US,
        interval=Interval(time_unit=TimeUnit.MONTH, value=[1]),
        last_run=None,
        account_id=1,
    )

    saved_strategy = strategy_repo.save(strategy)

    strategy_service: StrategyService = container.strategy_service()

    # When
    strategy_service.rebalance(saved_strategy.id)

    # Then
    found_strategy = strategy_repo.find_by_id(1)
    assert found_strategy.stocks["spy"].rebalance_qty == 100
    assert found_strategy.last_run is not None
    assert FakeAccount.balance == 0


class FakeStockMarketClient(StockMarketClient):
    def is_market_open(self, market: Market) -> bool:
        return True


class FakeTimeHolder(TimeHolder):
    def get_now(self) -> datetime:
        return datetime(2024, 1, 1)


class FakeAccountProvider(AccountProvider):
    account: Account = None

    def get_account(self, account_id: int) -> Account:
        if FakeAccountProvider.account is None:
            FakeAccountProvider.account = FakeAccount(None)
        return FakeAccountProvider.account


class FakeAccount(Account):
    balance: float = 10_000
    holdings: Dict[str, HoldingsInfo] = {}

    def __init__(self, entity: AccountEntity):
        self.entity = entity

    def get_balance(self) -> float:
        return FakeAccount.balance

    def get_holdings(self) -> Dict[str, HoldingsInfo]:
        return FakeAccount.holdings

    def buy_market_order(self, ticker: str, amount: float) -> None:
        FakeAccount.balance -= self.get_current_price(ticker) * amount

    def sell_market_order(self, ticker: str, amount: float) -> None:
        FakeAccount.balance += self.get_current_price(ticker) * amount

    def get_current_price(self, ticker: str) -> float:
        return 100


class FakeStrategyRepository(StrategyRepository):
    id_counter: int = 1
    strategies: List[Strategy] = []

    def find_by_id(self, id: int) -> Strategy:
        return next((strategy for strategy in FakeStrategyRepository.strategies if strategy.id == id), None)

    def save(self, dto: Strategy) -> Strategy:
        dto.id = FakeStrategyRepository.id_counter
        FakeStrategyRepository.id_counter += 1
        FakeStrategyRepository.strategies.append(dto)
        return dto

    def delete_by_id(self, id: int) -> None:
        FakeStrategyRepository.strategies.remove(next((strategy for strategy in FakeStrategyRepository.strategies if strategy.id == id), None))

    def find_all(self) -> List[Strategy]:
        return FakeStrategyRepository.strategies

    def update(self, id: int, dto: Strategy) -> Strategy:
        found_strategy = next((s for s in FakeStrategyRepository.strategies if s.id == id), None)
        if found_strategy is not None:
            FakeStrategyRepository.strategies.remove(found_strategy)
            FakeStrategyRepository.strategies.append(dto)
        return dto
