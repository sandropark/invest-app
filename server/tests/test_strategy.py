from datetime import datetime
from src.domain.strategy.strategy import Strategy, Interval
from src.domain.type import TimeUnit
from src.infra.persistance.schemas.strategy import StrategyEntity


# 1,2,3월에 실행해야하는 경우, 현재는 2월이고 마지막 실행이 1월이라면 True를 반환한다.
def test_is_time_to_rebalance():
    entity = StrategyEntity(interval=Interval(time_unit=TimeUnit.MONTH, value=[1, 2, 3]), last_run=datetime(2024, 1, 1))
    strategy = Strategy(entity=entity)
    assert strategy.is_time_to_rebalance(datetime(2024, 2, 1))


# 1,2,3월에 실행해야하는 경우, 현재는 2월이고 마지막 실행이 2월이라면 False를 반환한다.
def test_is_time_to_rebalance_false():
    entity = StrategyEntity(interval=Interval(time_unit=TimeUnit.MONTH, value=[1, 2, 3]), last_run=datetime(2024, 2, 1))
    strategy = Strategy(entity=entity)
    assert not strategy.is_time_to_rebalance(datetime(2024, 2, 1))
