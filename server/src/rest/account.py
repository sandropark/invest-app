from fastapi import APIRouter
from src.domain.account import account_service
from src.infra.kis.token_refresher import refresh_token, refresh_token_all
from src.infra.persistance.repo import account_repo
from src.rest.request.request import AccountCreateReq


router = APIRouter(prefix="/accounts", tags=["account"])


@router.post("/", summary="계좌 생성")
def save(req: AccountCreateReq):
    return account_repo.save(req.toDomain())


@router.get("/", summary="계좌 목록 조회")
def find_all():
    return account_repo.find_all()


@router.put("/{id}", summary="계좌 수정")
def update(id: int, req: AccountCreateReq):
    return account_repo.update(id, req.toDomain())


@router.get("/{id}", summary="계좌 상세 조회")
def get(id: int):
    return account_repo.get(id)


@router.delete("/{id}", summary="계좌 삭제")
def delete(id: int):
    return account_repo.delete(id)


@router.get("/{id}/balance", summary="잔고 조회")
def get_balance(id: int):
    return account_service.get_balance(account_id=id)


@router.post("/{id}/buy", summary="시장가 매수")
def buy(id: int, ticker: str, amount: float):
    account_service.buy(account_id=id, ticker=ticker, amt=amount)


@router.get("/{id}/stocks", summary="보유 종목 조회")
def get_stocks(id: int):
    return account_service.get_stocks(account_id=id)


@router.post("/refresh-kis-token", summary="한투 토큰 갱신 (전체)")
def refresh_kis_token_all(refresh_force: bool = False):
    return refresh_token_all(refresh_force)


@router.post("/{id}/refresh-kis-token", summary="한투 토큰 갱신")
def refresh_kis_token(id: int):
    return refresh_token(id)


@router.get("/{id}/current-price", summary="현재 가격 조회")
def get_current_price(id: int, ticker: str):
    return account_service.get_current_price(account_id=id, ticker=ticker)
