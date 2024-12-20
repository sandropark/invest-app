from sqlalchemy import JSON, ForeignKey, TypeDecorator
from src.domain.stock.stock_info import StockInfo
from src.domain.type import Market, TimeUnit
from src.infra.persistance.schemas.account import AccountEntity
from src.infra.persistance.schemas.base import BaseEntity, EnumType
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects import sqlite
from typing import Dict, List


class Interval:
    def __init__(self, time_unit: TimeUnit, value: List[int]):
        self.time_unit = time_unit
        self.value = value

    def __str__(self):
        return f"{self.start} {self.end}"

    def to_dict(self):
        return {
            "time_unit": self.time_unit.value,
            "value": self.value,
        }


class StockInfoDict(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value: Dict[str, StockInfo], dialect):
        if value is not None:
            return {k: v.to_dict() for k, v in value.items()}
        return None

    def process_result_value(self, value: dict, dialect):
        if value is not None:
            return {k: StockInfo(**v) for k, v in value.items()}
        return None


class IntervalType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value: Interval, dialect):
        if value is not None:
            return value.to_dict()
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return Interval(**value)
        return None


class StrategyEntity(BaseEntity):
    __tablename__ = "strategy"
    name: Mapped[str] = mapped_column(sqlite.VARCHAR(30), index=True)
    invest_rate: Mapped[float] = mapped_column(sqlite.FLOAT)
    market: Mapped[Market] = mapped_column(EnumType(Market))
    stocks: Mapped[Dict[str, StockInfo]] = mapped_column(StockInfoDict, nullable=True)
    interval: Mapped[Interval] = mapped_column(IntervalType)
    last_run: Mapped[str] = mapped_column(sqlite.DATETIME, nullable=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    account: Mapped[AccountEntity] = relationship()
