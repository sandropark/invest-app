from datetime import datetime
from src.domain.strategy.strategy import Strategy, Interval
from src.domain.common.type import TimeUnit


# 1,2,3월에 실행해야하는 경우, 현재는 2월이고 마지막 실행이 1월이라면 True를 반환한다.
def test_is_time_to_rebalance():
    strategy = get_strategy(Interval(time_unit=TimeUnit.MONTH, value=[1, 2, 3]), datetime(2024, 1, 1))
    assert strategy.is_time_to_rebalance(datetime(2024, 2, 1))


# 1,2,3월에 실행해야하는 경우, 현재는 2월이고 마지막 실행이 2월이라면 False를 반환한다.
def test_is_time_to_rebalance_false():
    strategy = get_strategy(Interval(time_unit=TimeUnit.MONTH, value=[1, 2, 3]), datetime(2024, 2, 1))
    assert not strategy.is_time_to_rebalance(datetime(2024, 2, 1))


def get_strategy(interval: Interval, last_run: datetime):
    return Strategy(
        id=None,
        name=None,
        interval=interval,
        last_run=last_run,
        market=None,
        invest_rate=None,
        stocks={},
        account_id=None,
    )
