from pykis import KisAccount, KisBalance, PyKis
from domain.type import BrokerType
from infra.persistance.schemas.account import AccountEntity
import pyupbit


def get_balance(account: AccountEntity):
    if account.broker_type == BrokerType.KIS_R:
        return _get_kis_balance_real(account)
    elif account.broker_type == BrokerType.KIS_V:
        return _get_kis_balance_virtual(account)
    elif account.broker_type == BrokerType.UPBIT_R:
        return _get_upbit_balance(account)
    else:
        raise Exception("지원하지 않는 거래소입니다.")


class KisHolder:
    kis_real = None
    kis_virtual = None

    def create_kis_instance(account: AccountEntity, is_virtual: bool = False) -> PyKis:
        if is_virtual:
            if KisHolder.kis_virtual is None:
                KisHolder.kis_virtual = KisHolder._create_kis_instance(account, True)
            return KisHolder.kis_virtual

        if KisHolder.kis_real is None:
            KisHolder.kis_real = KisHolder._create_kis_instance(account)
        return KisHolder.kis_real

    def _create_kis_instance(account: AccountEntity, is_virtual: bool = False) -> PyKis:
        return PyKis(
            id=account.login_id,  # HTS 로그인 ID
            account=f"{account.number}-{account.product_code}",  # 계좌번호
            appkey=account.app_key,  # AppKey 36자리
            secretkey=account.secret_key,  # SecretKey 180자리
            virtual_id=account.login_id if is_virtual else None,  # 가상 계좌 ID
            virtual_appkey=account.app_key if is_virtual else None,  # 가상 AppKey
            virtual_secretkey=(
                account.secret_key if is_virtual else None
            ),  # 가상 SecretKey
            keep_token=True,  # API 접속 토큰 자동 저장
        )


class UpbitHolder(object):
    upbit = None

    def create_upbit_instance(account: AccountEntity) -> pyupbit.Upbit:
        if UpbitHolder.upbit is None:
            UpbitHolder.upbit = pyupbit.Upbit(
                access=account.app_key, secret=account.secret_key
            )
        return UpbitHolder.upbit


def _get_kis_balance_real(account: AccountEntity):
    kis: PyKis = KisHolder.create_kis_instance(account)
    kis_account: KisAccount = kis.account()
    kis_balance: KisBalance = kis_account.balance()
    return kis_balance.total


def _get_kis_balance_virtual(account: AccountEntity):
    kis: PyKis = KisHolder.create_kis_instance(account, True)
    kis_account: KisAccount = kis.account()
    kis_balance: KisBalance = kis_account.balance()
    return kis_balance.total


def _get_upbit_balance(account: AccountEntity):
    upbit: pyupbit.Upbit = UpbitHolder.create_upbit_instance(account)
    return upbit.get_balance()
