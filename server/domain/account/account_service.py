from domain.account.account import (
    Account,
    HantuRealAccount,
    HantuVirtualAccount,
    UpbitAccount,
)
from domain.exception import InvestAppException
from domain.type import BrokerType
from infra.persistance.repo import account_repo
from infra.persistance.schemas.account import AccountEntity


kis_real = None
kis_virtual = None
upbit = None


def get_balance(account_id: int) -> float:
    account: Account = _get_account(account_id)
    return account.get_balance()


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
            kis_real = HantuRealAccount(account)
        return kis_real

    if account.broker_type == BrokerType.KIS and account.is_virtual:
        if kis_virtual is None:
            kis_virtual = HantuVirtualAccount(account)
        return kis_virtual

    if account.broker_type == BrokerType.UPBIT:
        if upbit is None:
            upbit = UpbitAccount(account)
        return upbit

    raise InvestAppException(
        "지원하지 않는 계좌 종류입니다. {}", 400, account.broker_type
    )
