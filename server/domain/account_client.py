from pykis import PyKis
from domain.type import BrokerType
from infra.persistance.schemas.account import Account
import pyupbit


def get_balance(account: Account):
    if account.broker_type == BrokerType.KIS_R:
        return _get_kis_balance_real(account)
    elif account.broker_type == BrokerType.KIS_V:
        return _get_kis_balance_virtual(account)
    elif account.broker_type == BrokerType.UPBIT_R:
        return _get_upbit_balance(account)
    else:
        raise Exception("지원하지 않는 거래소입니다.")


def _get_kis_balance_real(account: Account):
    kis = PyKis(
        id=account.login_id,  # HTS 로그인 ID
        account=f"{account.number}-{account.product_code}",  # 계좌번호
        appkey=account.app_key,  # AppKey 36자리
        secretkey=account.secret_key,  # SecretKey 180자리
        keep_token=True,  # API 접속 토큰 자동 저장
    )
    kis_account = kis.account()
    return kis_account.balance().total


def _get_kis_balance_virtual(account: Account):
    kis = PyKis(
        account=f"{account.number}-{account.product_code}",  # 계좌번호
        id=account.login_id,  # HTS 로그인 ID
        virtual_id=account.login_id,  # HTS 로그인 ID
        appkey=account.app_key,  # AppKey 36자리
        virtual_appkey=account.app_key,  # AppKey 36자리
        secretkey=account.secret_key,  # SecretKey 180자리
        virtual_secretkey=account.secret_key,  # SecretKey 180자리
        keep_token=True,  # API 접속 토큰 자동 저장
    )
    kis_account = kis.account()
    return kis_account.balance().total


def _get_upbit_balance(account: Account):
    upbit = pyupbit.Upbit(account.app_key, account.secret_key)
    return upbit.get_balance()
