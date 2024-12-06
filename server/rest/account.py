from fastapi import APIRouter
from domain.account.account import AccountHoler
from infra.persistance.repo import account_repo
from rest.request.request import AccountCreateReq

router = APIRouter(prefix="/accounts", tags=["account"])


@router.get("/")
def find_all():
    return account_repo.find_all()


@router.post("/")
def save(req: AccountCreateReq):
    return account_repo.save(req.toDomain())


@router.put("/{id}")
def update(id: int, req: AccountCreateReq):
    return account_repo.update(id, req.toDomain())


@router.get("/{id}")
def get(id: int):
    return account_repo.get(id)


@router.delete("/{id}")
def delete(id: int):
    return account_repo.delete(id)


@router.get("/{id}/balance")
def get_balance(id: int):
    account = account_repo.get(id)
    return AccountHoler.get_account(account).get_balance()
