from infra.persistance.schemas.account import AccountEntity, Strategy


def rebalance(strategy: Strategy, account: AccountEntity):
    # 포트폴리오 할당 금액 (포트 폴리오 비중 * 총 현금)
    #   - Data
    #     - 총 현금 (잔고)
    #     - 포트폴리오 비중 (전략)
    # 종목 별 리밸런스 수량 계산
    #   - 내 잔고에서 해당 종목을 팔아야 하는지, 사야 하는지 계산
    #   - Data
    #     - 보유 종목 (잔고)
    #     - 종목별 비중 (전략)
    #     - 종목별 현재 가격 (시세)
    # 매도
    # 매수

    # 계좌는 한투와 업비트 두 곳에 동시에 있을 수 있음
    account.get_balance()

    pass
