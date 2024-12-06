import pyupbit
from pykis import KisQuote, KisStock, PyKis


def get_current_price(ticker: str):
    # KRW-BTC, AAPL, QQQ, 005930
    # 티커에 따라서 어느 거래소를 사용하지 결정.

    if ticker.startswith("KRW-"):
        return pyupbit.get_current_price(ticker)

    return (
        PyKis(
            id="1",
            appkey="123451234512345123451234512345123456",
            secretkey="XL7@t2!uoG81CA8qJDM&bK6^24Z0H@EI8czSFAWHL3&g9Om#zp1wQW53GcNCHOtrkI$7k!NWp0ZW98p2oPbWgQLZ&hXL7@t2!uoG81CA8qJDM&bK6^24Z0H@EI8czSFAWHL3&g9Om#zp1wQW53GcNCHOtrkI$7k!NWp0ZW98p2oPbWgQLZ&h",
            keep_token=True,
        )
        .stock(ticker)
        .quote()
        .close
    )
