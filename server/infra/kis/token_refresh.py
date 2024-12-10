import json
import requests
from domain.exception import InvestAppException
from domain.type import BrokerType
from infra.persistance.repo import account_repo
from infra.persistance.schemas.account import AccountEntity


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

    return res.json()["access_token"]


def refresh_token():
    kis_accounts = account_repo.find_all(broker_type=BrokerType.KIS)
    token = get_token(kis_accounts[0])
    for kis_account in kis_accounts:
        kis_account.token = token
    account_repo.save_all(kis_accounts)
