from fastapi import APIRouter
from src.containers import Container
from src.domain.account.account import Account
from src.infra.kis import token_refresher
from src.rest.request_model import AccountCreateReq


router = APIRouter(prefix="/accounts", tags=["account"])


container = Container.get_instance()
account_repo = container.account_repository()
account_provider = container.account_provider()


@router.post("/", summary="계좌 생성")
def save(req: AccountCreateReq):
    return account_repo.save(req.to_domain())


@router.put("/{id}", summary="계좌 수정")
def update(id: int, req: AccountCreateReq):
    return account_repo.update(id, req.to_domain())


@router.get("/", summary="계좌 목록 조회")
def find_all():
    return account_repo.find_all()


@router.get("/{id}", summary="계좌 상세 조회")
def find_by_id(id: int):
    return account_repo.find_by_id(id)


@router.delete("/{id}", summary="계좌 삭제")
def delete(id: int):
    return account_repo.delete_by_id(id)


@router.get("/{id}/balance", summary="잔고 조회")
def get_balance(id: int):
    account: Account = account_provider.get_account(id)
    return account.get_balance()


@router.post("/{id}/buy", summary="시장가 매수")
def buy(id: int, ticker: str, amount: float):
    account_provider.buy(account_id=id, ticker=ticker, amt=amount)


@router.get("/{id}/holdings", summary="보유 종목 조회")
def get_holdings(id: int):
    account: Account = account_provider.get_account(id)
    return account.get_holdings()


@router.post("/refresh-kis-token", summary="한투 토큰 갱신 (전체)")
def refresh_kis_token_all():
    return token_refresher.refresh_kis_token()


@router.get("/{id}/current-price", summary="현재 가격 조회")
def get_current_price(id: int, ticker: str):
    account: Account = account_provider.get_account(id)
    return account.get_current_price(ticker)
