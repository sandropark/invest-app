import json
import requests
from domain.exception import InvestAppException
from domain.type import BrokerType
from infra.persistance.repo import account_repo
from infra.persistance.schemas.account import AccountEntity, Token


def get_token(account: AccountEntity) -> str:
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": account.app_key,
        "appsecret": account.secret_key,
    }

    URL = f"{account.url_base}/oauth2/tokenP"
    res = requests.post(URL, headers=headers, data=json.dumps(body))

    if res.status_code != 200:
        raise InvestAppException("토큰 생성 실패. {}", 500, res.text)

    return res.json()


def refresh_token(id: int):
    kis_account: AccountEntity = account_repo.get(id)
    if kis_account.broker_type != BrokerType.KIS:
        raise InvestAppException(
            "한투 계좌만 지원합니다. broker_type={}", 400, kis_account.broker_type
        )
    _refresh_token(kis_account)


def refresh_token_all(refresh_force: bool = False):
    accounts = account_repo.find_all(broker_type=BrokerType.KIS)
    for account in accounts:
        _refresh_token(account, refresh_force)


def _refresh_token(account: AccountEntity, refresh_force: bool = False):
    if refresh_force or account.is_token_expired():
        account.token = Token.of(get_token(account))
        account_repo.save(account)
