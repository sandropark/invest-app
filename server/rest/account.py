from fastapi import APIRouter
from domain.account import account_holder
from infra.persistance.repo import account_repo
from rest.request.request import AccountCreateReq


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
    account = account_repo.get(id)
    return account_holder.get_account(account).get_balance()
