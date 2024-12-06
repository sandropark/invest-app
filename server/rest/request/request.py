from typing import Dict, List, Optional
from pydantic import BaseModel
from domain.type import BrokerType, TimeUnit
from infra.persistance.schemas.strategy import Interval, StockInfo
from infra.persistance.schemas.strategy import StrategyEntity
from infra.persistance.schemas.account import AccountEntity


class StockInfoReq(BaseModel):
    target_rate: Optional[float] = None
    rebalance_amt: Optional[int] = None

    def toDomain(self) -> StockInfo:
        return StockInfo(
            target_rate=self.target_rate,
            rebalance_amt=self.rebalance_amt,
        )


class IntervalReq(BaseModel):
    time_unit: TimeUnit
    value: List[int]

    def toDomain(self) -> Interval:
        return Interval(
            time_unit=self.time_unit,
            value=self.value,
        )


class StrategyCreateReq(BaseModel):
    name: str
    invest_rate: Optional[float] = None
    env: Optional[str] = None
    stocks: Dict[str, StockInfoReq]
    interval: Optional[IntervalReq] = None

    def toDomain(self) -> StrategyEntity:
        return StrategyEntity(
            name=self.name,
            invest_rate=self.invest_rate,
            env=self.env,
            stocks={k: v.toDomain() for k, v in self.stocks.items()},
            interval=self.interval.toDomain(),
        )


class AccountCreateReq(BaseModel):
    name: str
    number: str
    product_code: str
    app_key: str
    secret_key: str
    url_base: str
    token: Optional[str] = None
    broker_type: BrokerType

    def toDomain(self) -> AccountEntity:
        return AccountEntity(
            name=self.name,
            number=self.number,
            product_code=self.product_code,
            app_key=self.app_key,
            secret_key=self.secret_key,
            url_base=self.url_base,
            token=self.token,
            broker_type=self.broker_type,
        )
