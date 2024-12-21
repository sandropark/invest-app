from src.domain.type import BrokerType
from src.infra.kis import kis_client
from src.infra.kis.access_token import KisAccessToken
from src.infra.kis.account import KisAccount
from src.infra.persistance.repo import account_repo


def refresh_kis_token():
    account_dtos = account_repo.find_all(broker_type=BrokerType.KIS)

    for account_dto in account_dtos:
        kis_account: KisAccount = KisAccount(account_dto=account_dto)
        token: KisAccessToken = kis_account.access_token
        if token is None or token.is_expired():
            account_dto.token = kis_client.get_token(kis_account._get_kis_info())

    account_repo.save_all(account_dtos)
