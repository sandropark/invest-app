from datetime import datetime
from sqlalchemy import JSON, ForeignKey, TypeDecorator
from src.domain.common.type import Market
from src.domain.strategy.interval import Interval
from src.domain.strategy.stock_info import StockInfo
from src.infra.common.persistence.base import BaseEntity, EnumType
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects import sqlite
from typing import Dict


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
    last_run: Mapped[datetime] = mapped_column(sqlite.DATETIME, nullable=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
