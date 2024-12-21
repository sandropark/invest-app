from fastapi import APIRouter
from src.containers import Container
from src.domain.strategy.strategy_service import StrategyService
from src.rest.request_model import StrategyCreateReq

router = APIRouter(prefix="/strategies", tags=["strategy"])

container = Container()
strategy_service: StrategyService = container.strategy_service()


@router.get("/")
def find_all():
    return strategy_service.find_all()


@router.post("/")
def save(req: StrategyCreateReq):
    return strategy_service.save(req.toDomain())


@router.put("/{id}")
def update(id: int, req: StrategyCreateReq):
    return strategy_service.update(id, req.toDomain())


@router.get("/{id}")
def get(id: int):
    return strategy_service.find_by_id(id)


@router.delete("/{id}")
def delete(id: int):
    return strategy_service.delete_by_id(id)
