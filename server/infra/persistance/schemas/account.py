from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import JSON, TypeDecorator
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Mapped, mapped_column
from domain.type import BrokerType

from infra.persistance.schemas.base import BaseEntity, EnumType


@dataclass
class Token:
    token: str
    expiration: str

    def of(json: dict):
        return Token(
            token=json["access_token"], expiration=json["access_token_token_expired"]
        )

    def to_dict(self):
        return {
            "token": self.token,
            "expiration": self.expiration,
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
    token: Mapped[Token] = mapped_column(TokenType, nullable=True)

    def is_token_invalid(self) -> bool:
        return self.token is None or self._is_token_expired()

    def _is_token_expired(self):
        return self._get_token_expiration() < datetime.now()

    def _get_token_expiration(self) -> datetime:
        return datetime.strptime(self.token.expiration, "%Y-%m-%d %H:%M:%S")

    def get_access_token(self) -> str:
        return self.token.token
