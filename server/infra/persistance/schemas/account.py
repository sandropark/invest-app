from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Mapped, mapped_column
from domain.type import BrokerType

from infra.persistance.schemas.base import BaseEntity, EnumType


class AccountEntity(BaseEntity):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sqlite.VARCHAR(30))
    app_key: Mapped[str] = mapped_column(sqlite.VARCHAR(50))
    secret_key: Mapped[str] = mapped_column(sqlite.VARCHAR(100))
    broker_type: Mapped[BrokerType] = mapped_column(EnumType(BrokerType))
    number: Mapped[str] = mapped_column(sqlite.VARCHAR(10), nullable=True)
    product_code: Mapped[str] = mapped_column(sqlite.CHAR(2), nullable=True)
    login_id: Mapped[str] = mapped_column(sqlite.VARCHAR(30), nullable=True)
    url_base: Mapped[str] = mapped_column(sqlite.VARCHAR(100), nullable=True)
