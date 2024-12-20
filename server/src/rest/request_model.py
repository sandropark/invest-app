from typing import Dict, List, Optional
from pydantic import BaseModel
from src.domain.account.dto import AccountDto
from src.domain.strategy.strategy import Strategy
from src.domain.common.type import BrokerType, Market, TimeUnit
from src.infra.strategy.persistance.strategy import Interval, StockInfo


class StockInfoReq(BaseModel):
    target_rate: Optional[float] = None
    rebalance_qty: Optional[int] = None

    def toDomain(self) -> StockInfo:
        return StockInfo(
            target_rate=self.target_rate,
            rebalance_qty=self.rebalance_qty,
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
    stocks: Dict[str, StockInfoReq]
    interval: Optional[IntervalReq] = None
    market: Market
    account_id: int

    def toDomain(self) -> Strategy:
        return Strategy(
            name=self.name,
            invest_rate=self.invest_rate,
            stocks={k: v.toDomain() for k, v in self.stocks.items()},
            interval=self.interval.toDomain(),
            account_id=self.account_id,
            market=self.market,
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

    def to_domain(self) -> AccountDto:
        return AccountDto(
            name=self.name,
            number=self.number,
            product_code=self.product_code,
            app_key=self.app_key,
            secret_key=self.secret_key,
            url_base=self.url_base,
            token=self.token,
            broker_type=self.broker_type,
        )
