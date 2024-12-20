from typing import Dict
from src.domain.account import account_service
from src.domain.account.account import Account
from src.domain.account.holdings import HoldingsInfo
from src.domain.stock.stock_info import StockInfo
from src.domain.strategy.strategy import Strategy
from src.infra.persistance.mapper import strategy_mapper
from src.infra.persistance.repo import strategy_repo
from src.infra.persistance.schemas.strategy import StrategyEntity


def rebalance(strategy_id: int):
    strategy: Strategy = get_strategy(strategy_id)

    if strategy.has_rebalanced():
        return

    account: Account = account_service.get_account(strategy.account_id)

    # TODO : 1. 마켓이 닫힌 경우 로그 남기고 종료. (외부 : 마켓 물어보기)

    # 2. 포트폴리오 할당 금액 계산 (포트 폴리오 비중 * 잔고)
    invest_amount = strategy.get_invest_amount(account.get_balance())

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
        if stock.rebalance_amt > 0:
            account.sell_market_order(ticker, stock.rebalance_amt)

    # 6. 리밸런싱 수량 만큼 매수
    for ticker, stock in stocks.items():
        if stock.rebalance_amt < 0:
            account.buy_market_order(ticker, stock.rebalance_amt)

    strategy.complete_rebalance()


def get_strategy(strategy_id: int) -> Strategy:
    strategy: StrategyEntity = strategy_repo.get(strategy_id)
    return strategy_mapper.to_domain(strategy)
