from sqlalchemy import JSON, TypeDecorator
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.account.token import KisAccessToken
from src.domain.type import BrokerType

from src.infra.persistance.schemas.base import BaseEntity, EnumType


class TokenType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value: KisAccessToken, dialect):
        if value is not None:
            return value.to_dict()
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return KisAccessToken(**value)
        return None


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
    is_virtual: Mapped[bool] = mapped_column(
        sqlite.BOOLEAN, default=False, nullable=False
    )
    token: Mapped[KisAccessToken] = mapped_column(TokenType, nullable=True)
