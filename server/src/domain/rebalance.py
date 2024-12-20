from typing import Dict
from domain.account.account import Account, HoldingsInfo
from domain.strategy import Strategy


def rebalance(strategy: Strategy, account: Account):
    # TODO : 1. 마켓이 닫힌 경우 로그 남기고 종료

    # 1. 잔고 조회
    balance: float = account.get_balance()

    # 2. 포트폴리오 할당 금액 계산 (포트 폴리오 비중 * 잔고)
    invest_amount = strategy._get_invest_amount(balance)

    # 3. 보유 종목 리스트 조회
    holddings_dict: Dict[str, HoldingsInfo] = account.get_holdings()

    # 4. 종목별 비중 계산
    for ticker, stock in strategy.stocks.items():
        stock.calculate_rebalance_amt(
            portfolio_target_amt=invest_amount,
            holdings=holddings_dict.get(ticker),
            current_price=account.get_current_price(ticker),
        )

    # 5. 리밸런싱 수량 만큼 매도
    for ticker, stock in strategy.stocks.items():
        if stock.rebalance_amt > 0:
            account.sell_market_order(ticker, stock.rebalance_amt)

    # 6. 리밸런싱 수량 만큼 매수
    for ticker, stock in strategy.stocks.items():
        if stock.rebalance_amt < 0:
            account.buy_market_order(ticker, stock.rebalance_amt)
