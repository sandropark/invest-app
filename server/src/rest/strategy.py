from fastapi import APIRouter
from infra.persistance.repo import strategy_repo
from rest.request.request import StrategyCreateReq

router = APIRouter(prefix="/strategies", tags=["strategy"])


@router.get("/")
def find_all():
    return strategy_repo.find_all()


@router.post("/")
def save(req: StrategyCreateReq):
    return strategy_repo.save(req.toDomain())


@router.put("/{id}")
def update(id: int, req: StrategyCreateReq):
    return strategy_repo.update(id, req.toDomain())


@router.get("/{id}")
def get(id: int):
    return strategy_repo.get(id)


@router.delete("/{id}")
def delete(id: int):
    return strategy_repo.delete(id)
