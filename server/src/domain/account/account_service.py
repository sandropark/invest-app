from src.domain.account.account import (
    Account,
    KisAccount,
    KisRealAccount,
    KisVirtualAccount,
    UpbitAccount,
)
from src.infra.kis.access_token import KisAccessToken
from src.domain.exception import InvestAppException
from src.domain.type import BrokerType, Market
from src.infra.kis import kis_client
from src.infra.persistance.mapper import account_mapper
from src.infra.persistance.repo import account_repo
from src.infra.persistance.schemas.account import AccountEntity


kis_real = None
kis_virtual = None
upbit = None


def get_balance(account_id: int, market: Market = Market.KR) -> float:
    account: Account = _get_account(account_id)
    return account.get_balance(market)


def buy(account_id: int, ticker: str, amt: int) -> float:
    account = _get_account(account_id)
    return account.buy_market_order(ticker, amt)


def get_stocks(account_id: int):
    account = _get_account(account_id)
    return account.get_holdings()


def _get_account(account_id: int) -> Account:
    account: AccountEntity = account_repo.get(account_id)

    global kis_real, kis_virtual, upbit

    if account.broker_type == BrokerType.KIS and not account.is_virtual:
        if kis_real is None:
            kis_real = KisRealAccount(account)
        return kis_real

    if account.broker_type == BrokerType.KIS and account.is_virtual:
        if kis_virtual is None:
            kis_virtual = KisVirtualAccount(account)
        return kis_virtual

    if account.broker_type == BrokerType.UPBIT:
        if upbit is None:
            upbit = UpbitAccount(account)
        return upbit

    raise InvestAppException("지원하지 않는 계좌 종류입니다. {}", 400, account.broker_type)


def get_current_price(account_id: int, ticker: str) -> float:
    account = _get_account(account_id)
    return account.get_current_price(ticker)


def refresh_kis_token():
    accounts = account_repo.find_all(broker_type=BrokerType.KIS)

    for account in accounts:
        kis_account: KisAccount = account_mapper.to_kis_domain(account)
        token: KisAccessToken = kis_account.access_token
        if token is None or token.is_expired():
            account.token = kis_client.get_token(kis_account._get_kis_info())

    account_repo.save_all(accounts)
