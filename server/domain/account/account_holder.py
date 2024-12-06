from domain.account.account import (
    Account,
    KISRealAccount,
    KISVirtualAccount,
    UpbitAccount,
)
from domain.type import BrokerType
from infra.persistance.schemas.account import AccountEntity


kis_real = None
kis_virtual = None
upbit = None


def get_account(account: AccountEntity) -> Account:
    global kis_real, kis_virtual, upbit

    if account.broker_type == BrokerType.KIS_R:
        if kis_real is None:
            kis_real = KISRealAccount(account)
        return kis_real
    elif account.broker_type == BrokerType.KIS_V:
        if kis_virtual is None:
            kis_virtual = KISVirtualAccount(account)
        return kis_virtual
    elif account.broker_type == BrokerType.UPBIT_R:
        if upbit is None:
            upbit = UpbitAccount(account)
        return upbit
    else:
        raise Exception("지원하지 않는 거래소입니다.")
