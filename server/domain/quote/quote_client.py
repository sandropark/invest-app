import pyupbit
import yfinance as yf
import FinanceDataReader as fdr
import pykrx
import pandas_datareader.data as web
from datetime import datetime


def get_current_price(ticker: str):
    # 숫자 6자리면 한국 주식
    if ticker.isdigit() and len(ticker) == 6:
        end = datetime.now()
        start = end.replace(month=end.month - 1)
        return web.DataReader(ticker, "naver", start, end)["Close"][-1]

    # KRW-로 시작하면 업비트
    if ticker.startswith("KRW-"):
        return pyupbit.get_current_price(ticker)

    # 나머지는 yfinance
    return yf.Ticker(ticker).history(period="1d").Close[0]
