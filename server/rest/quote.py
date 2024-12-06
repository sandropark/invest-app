from fastapi import APIRouter

from domain.quote import quote_client


router = APIRouter(prefix="/quote", tags=["quote"])


@router.get("/current-price/{ticker}", summary="현재 가격 조회")
def get_current_price(ticker: str):
    return quote_client.get_current_price(ticker)
