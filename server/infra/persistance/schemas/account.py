from datetime import datetime
from sqlalchemy import JSON, TypeDecorator
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Mapped, mapped_column
from domain.type import BrokerType

from infra.persistance.schemas.base import BaseEntity, EnumType


class Token:
    def __init__(self, token: str, expired_at: str):
        self.token = token
        self.expired_at = expired_at

    def to_dict(self):
        return {
            "token": self.token,
            "expired_at": self.expired_at,
        }


class TokenType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value: Token, dialect):
        if value is not None:
            return value.to_dict()
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return Token(**value)
        return None


class AccountEntity(BaseEntity):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    login_id: Mapped[str] = mapped_column(sqlite.VARCHAR(30))
    name: Mapped[str] = mapped_column(sqlite.VARCHAR(30))
    number: Mapped[str] = mapped_column(sqlite.VARCHAR(10), index=True)
    product_code: Mapped[str] = mapped_column(sqlite.CHAR(2))
    app_key: Mapped[str] = mapped_column(sqlite.VARCHAR(50))
    secret_key: Mapped[str] = mapped_column(sqlite.VARCHAR(100))
    url_base: Mapped[str] = mapped_column(sqlite.VARCHAR(100))
    token: Mapped[Token] = mapped_column(TokenType, nullable=True)
    broker_type: Mapped[BrokerType] = mapped_column(EnumType(BrokerType), nullable=True)

    def is_token_invalid(self):
        return (
            self.token is None
            or datetime.strptime(self.token.expired_at, "%Y-%m-%d %H:%M:%S")
            < datetime.now()
        )
