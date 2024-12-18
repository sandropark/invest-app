from typing import Dict
from domain.account.account import Account, HoldingsInfo
from domain.strategy import Strategy
from infra.persistance.schemas.strategy import StockInfo


def rebalance(strategy: Strategy, account: Account):
    # 종목 별 리밸런스 수량 계산
    #   - 내 잔고에서 해당 종목을 팔아야 하는지, 사야 하는지 계산
    #   - Data
    #     - 보유 종목 (잔고)
    #     - 종목별 비중 (전략)
    #     - 종목별 현재 가격 (시세)
    # 매도
    # 매수

    balance: float = account.get_balance()
    invest_amount = strategy.get_invest_amount(
        balance
    )  # 포트폴리오 할당 금액 (포트 폴리오 비중 * 총 현금)

    # 2. 보유 종목 리스트 조회
    holddings_dict: Dict[str, HoldingsInfo] = account.get_holdings()

    # 3. 종목별 비중 계산
    stocks: Dict[str, StockInfo] = strategy.stocks
    for ticker, stock in stocks.items():

        current_price = account.get_current_price(ticker)
        holdings = holddings_dict[ticker]

        if holdings is None:
            stock.rebalance_amt = (
                invest_amount * stock.target_rate / current_price
            )  # 리밸런스 수량
            continue

    pass
