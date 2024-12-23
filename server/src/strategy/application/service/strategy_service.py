import datetime
from typing import Dict
from src.common.application.port.out.time_holder import TimeHolder
from src.common.application.port.out.stock_market_port import StockMarketQueryPort
from src.account.application.service.account_provider import AccountProvider
from src.account.domain.account import Account
from src.account.domain.holdings import HoldingsInfo
from src.common.application.port.out.repository import *
from src.common.domain.exception import ExeptionType, InvestAppException
from src.strategy.application.port.out.strategy_repository import StrategyRepository
from src.strategy.domain.stock_info import StockInfo
from src.strategy.domain.strategy import Strategy
from dependency_injector.wiring import inject

from src.strategy.adapter.out.persistence import strategy_mapper


class StrategyService:
    @inject
    def __init__(
        self,
        strategy_repo: StrategyRepository,
        account_provider: AccountProvider,
        stock_market_query_port: StockMarketQueryPort,
        time_holder: TimeHolder,
    ):
        self.strategy_repo = strategy_repo
        self.account_provider = account_provider
        self.stock_market_query_port = stock_market_query_port
        self.time_holder = time_holder

    def save(self, dto: Strategy) -> Strategy:
        return self.strategy_repo.save(dto)

    def find_by_id(self, id: int) -> Strategy:
        strategy = self.strategy_repo.find_by_id(id)

        if strategy is None:
            raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)

        return strategy

    def find_all(self) -> List[Strategy]:
        return self.strategy_repo.find_all()

    def delete_by_id(self, id: int) -> int:
        return self.strategy_repo.delete_by_id(id)

    def update(self, id: int, dto: Strategy) -> Strategy:
        return self.strategy_repo.update(id, dto)

    def rebalance(self, strategy_id: int):
        strategy: Strategy = self.find_by_id(strategy_id)

        now: datetime = self.time_holder.get_now()

        # 리밸런싱 조건 확인
        strategy.is_time_to_rebalance(now)
        # 주식 시장 열려있는지 확인
        self.stock_market_query_port.is_market_open(strategy.get_market())

        account: Account = self.account_provider.get_account(strategy.get_account_id())

        # 2. 포트폴리오 할당 금액 계산 (포트 폴리오 비중 * 잔고)
        invest_amount: float = strategy.get_invest_amount(account.get_balance())

        # 3. 보유 종목 리스트 조회
        holddings_dict: Dict[str, HoldingsInfo] = account.get_holdings()

        stocks: Dict[str, StockInfo] = strategy.get_stocks()

        # 4. 종목별 비중 계산
        for ticker, stock in stocks.items():
            stock.calculate_rebalance_amt(
                portfolio_target_amt=invest_amount,
                holdings=holddings_dict.get(ticker),
                current_price=account.get_current_price(ticker),
            )

        # 5. 리밸런싱 수량 만큼 매도
        for ticker, stock in stocks.items():
            if stock.rebalance_qty < 0:
                account.sell_market_order(ticker, stock.rebalance_qty)

        # 6. 리밸런싱 수량 만큼 매수
        for ticker, stock in stocks.items():
            if stock.rebalance_qty > 0:
                account.buy_market_order(ticker, stock.rebalance_qty)

        strategy.complete_rebalance()

        self.strategy_repo.update(strategy_id, strategy)

    def rebalance_all(self):
        strategy_entities = self.strategy_repo.find_all()
        for strategy_entity in strategy_entities:
            strategy = strategy_mapper.entity_to_dto(strategy_entity)
            self.rebalance(strategy)