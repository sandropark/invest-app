from src.containers import Container
from src.domain.common.type import BrokerType
from src.infra.account.kis import kis_client
from src.infra.account.kis.access_token import KisAccessToken
from src.infra.account.kis.account import KisAccount

container = Container.get_instance()
account_repo = container.account_repository()


def refresh_kis_token():
    account_dtos = account_repo.find_all(broker_type=BrokerType.KIS)

    for account_dto in account_dtos:
        kis_account: KisAccount = KisAccount(account_dto=account_dto)
        token: KisAccessToken = kis_account.access_token
        if token is None or token.is_expired():
            account_dto.token = kis_client.get_token(kis_account._get_kis_info())

    account_repo.upsert_all(account_dtos)
