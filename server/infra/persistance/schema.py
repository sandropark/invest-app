from typing import Dict, List
from sqlalchemy import JSON, String, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from domain.stock_info import StockInfo
from sqlalchemy import func
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Mapped, mapped_column
from domain.type import BrokerType
from infra.persistance.model import Interval


Base = declarative_base()


class StockInfoDict(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        if value is not None:
            return {k: v.to_dict() for k, v in value.items()}
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return {k: StockInfo(**v) for k, v in value.items()}
        return None


class IntervalType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.to_dict()
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return Interval(**value)
        return None


class EnumType(TypeDecorator):
    impl = String

    def __init__(self, enum_class):
        super().__init__()
        self.enum_class = enum_class

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return value.value  # Enum의 값을 문자열로 저장

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.enum_class(value)  # 문자열을 다시 Enum으로 변환


class BaseEntity(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[str] = mapped_column(
        sqlite.DATETIME,
        server_default=func.now(),  # INSERT 시 서버에서 시간 생성
        nullable=False,
    )
    updated_at: Mapped[str] = mapped_column(
        sqlite.DATETIME,
        server_default=func.now(),  # INSERT 시 서버에서 시간 생성
        onupdate=func.now(),  # UPDATE 시 자동 업데이트
        nullable=False,
    )


class Strategy(BaseEntity):
    __tablename__ = "strategy"
    name: Mapped[str] = mapped_column(sqlite.VARCHAR(30), index=True)
    invest_rate: Mapped[float] = mapped_column(sqlite.FLOAT)
    env: Mapped[str] = mapped_column(sqlite.CHAR(1), default="R")
    stocks: Mapped[Dict[str, StockInfo]] = mapped_column(StockInfoDict, nullable=True)
    interval: Mapped[Interval] = mapped_column(IntervalType)
    last_run: Mapped[str] = mapped_column(sqlite.DATETIME, nullable=True)


class Account(BaseEntity):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sqlite.VARCHAR(30))
    number: Mapped[str] = mapped_column(sqlite.VARCHAR(10), index=True)
    product_code: Mapped[str] = mapped_column(sqlite.CHAR(2))
    app_key: Mapped[str] = mapped_column(sqlite.VARCHAR(50))
    secret_key: Mapped[str] = mapped_column(sqlite.VARCHAR(100))
    url_base: Mapped[str] = mapped_column(sqlite.VARCHAR(100))
    token: Mapped[str] = mapped_column(sqlite.VARCHAR(200), nullable=True)
    broker_type: Mapped[BrokerType] = mapped_column(EnumType(BrokerType))
