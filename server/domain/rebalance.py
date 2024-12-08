from typing import Dict
from domain.account.account import Account
from infra.persistance.schemas.strategy import StockInfo, StrategyEntity


def rebalance(strategy: StrategyEntity, account: Account):
    # 종목 별 리밸런스 수량 계산
    #   - 내 잔고에서 해당 종목을 팔아야 하는지, 사야 하는지 계산
    #   - Data
    #     - 보유 종목 (잔고)
    #     - 종목별 비중 (전략)
    #     - 종목별 현재 가격 (시세)
    # 매도
    # 매수

    # 1. 포트폴리오 할당 금액 (포트 폴리오 비중 * 총 현금)
    balance: float = account.get_balance()
    invest_rate: float = strategy.invest_rate
    invest_amount = balance * invest_rate

    # 2. 종목별 비중 계산
    stocks: Dict[str, StockInfo] = strategy.stocks

    pass
