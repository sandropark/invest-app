from fastapi import APIRouter

from src.domain.stock import stock_client


router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("", summary="종목 리스트 조회")
def get_ticker_list():
    return stock_client.get_ticker_list()


@router.get("/{ticker}/current-price", summary="현재 가격 조회")
def get_current_price(ticker: str):
    return stock_client.get_current_price(ticker)
