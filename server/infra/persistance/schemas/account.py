from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Mapped, mapped_column
from domain.type import BrokerType

from infra.persistance.schemas.base import BaseEntity, EnumType


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
