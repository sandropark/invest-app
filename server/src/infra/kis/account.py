from venv import logger
from src.domain.account.account import Account
from src.domain.account.holdings import HoldingsInfo
from src.domain.type import Market
from src.infra.kis import kis_client
from src.infra.kis.access_token import KisAccessToken
from src.infra.kis.dto import KisInfo
from src.infra.persistance.schemas.account import AccountEntity


class KisAccount(Account):
    def __init__(self, account: AccountEntity, is_virtual: bool = False):
        super().__init__(account=account)
        self.is_virtual: bool = is_virtual
        self.access_token: KisAccessToken = self.account.token

    def get_balance(self, market: Market = Market.KR) -> float:
        return kis_client.get_balance(self._get_kis_info(), market)

    def buy_market_order(self, ticker: str, amount: float) -> None:
        pass

    def sell_market_order(self, ticker: str, amount: float) -> None:
        pass

    def get_holdings(self) -> dict[str, HoldingsInfo]:
        return {
            stock["pdno"]: HoldingsInfo(
                name=stock["prdt_name"],
                quantity=float(stock["hldg_qty"]),
                avg_price=float(stock["pchs_avg_pric"]),
                eval_amount=float(stock["evl_amt"]),
            )
            for stock in kis_client.get_stocks(self._get_kis_info())
        }

    def get_current_price(self, ticker: str) -> float:
        return kis_client.get_current_price(self._get_kis_info(), ticker)

    def refresh_token(self):
        if self._is_token_invalid():
            self.account.token = kis_client.get_token(self._get_kis_info())
            logger.info(f"토큰 갱신 완료. account_id={self.account.id}")

    def _is_token_invalid(self) -> bool:
        return self.access_token is None or self._is_token_expired()

    def _get_kis_info(self) -> KisInfo:
        return KisInfo(
            token=self.access_token.token,
            app_key=self.account.app_key,
            secret_key=self.account.secret_key,
            url_base=self.account.url_base,
            account_number=self.account.number,
            product_code=self.account.product_code,
            is_real=not self.is_virtual,
        )


class KisRealAccount(KisAccount):
    def __init__(self, account: AccountEntity):
        super().__init__(account=account)


class KisVirtualAccount(KisAccount):
    def __init__(self, account: AccountEntity):
        super().__init__(account=account, is_virtual=True)
