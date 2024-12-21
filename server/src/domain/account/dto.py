from dataclasses import dataclass
from src.domain.type import BrokerType
from src.infra.kis.access_token import KisAccessToken


@dataclass
class AccountDto:
    id: int
    name: str
    app_key: str
    secret_key: str
    broker_type: BrokerType
    number: str
    product_code: str
    login_id: str
    url_base: str
    is_virtual: bool
    token: KisAccessToken
