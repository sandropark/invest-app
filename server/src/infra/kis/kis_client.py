import json
import requests
from src.infra.kis.access_token import KisAccessToken
from src.domain.exception import ExeptionType, InvestAppException
from src.infra.kis.dto import BalanceResponse, KisInfo
import yfinance as yf

from src.domain.type import Market


def get_token(info: KisInfo) -> KisAccessToken:
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": info.app_key,
        "appsecret": info.secret_key,
    }

    URL = f"{info.url_base}/oauth2/tokenP"
    res = requests.post(URL, headers=headers, data=json.dumps(body))

    if res.status_code != 200:
        raise InvestAppException(ExeptionType.FAILED_TO_CREATE_TOKEN, res.text)

    return KisAccessToken.of(res.json())


def get_balance(info: KisInfo, market: Market = Market.KR) -> float:
    if market == Market.KR:
        return BalanceResponse.of(_get_balance_kr(info).json()["output2"][0]).total_money

    return _get_balance_us(info)


def get_stocks(info: KisInfo):
    res = _get_balance_kr(info)

    return res.json()["output1"]


def _get_balance_kr(info: KisInfo):
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {info.token}",
        "appKey": info.app_key,
        "appSecret": info.secret_key,
        "tr_id": "TTTC8434R" if info.is_real else "VTTC8434R",
        "custtype": "P",
    }

    params = {
        "CANO": info.account_number,
        "ACNT_PRDT_CD": info.product_code,
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "02",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": "",
    }

    URL = f"{info.url_base}/uapi/domestic-stock/v1/trading/inquire-balance"

    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        return res

    raise InvestAppException(ExeptionType.FAILED_TO_GET_BALANCE, res.text)


def _get_balance_us(info: KisInfo):
    URL = f"{info.url_base}/uapi/overseas-stock/v1/trading/inquire-present-balance"

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {info.token}",
        "appKey": info.app_key,
        "appSecret": info.secret_key,
        "tr_id": "CTRP6504R" if info.is_real else "VTRP6504R",
        "custtype": "P",
    }

    params = {
        "CANO": info.account_number,
        "ACNT_PRDT_CD": info.product_code,
        "WCRC_FRCR_DVSN_CD": "02",
        "NATN_CD": "840",
        "TR_MKET_CD": "00",
        "INQR_DVSN_CD": "00",
    }

    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        result = res.json()["output2"]
        return result

        # # 실시간 주식 상태가 반영이 안되서 주식 정보를 직접 읽어서 계산!
        # my_stock_list = GetMyStockList(st)

        # StockOriMoneyTotal = 0
        # StockNowMoneyTotal = 0

        # for stock in my_stock_list:
        #     # pprint.pprint(stock)
        #     StockOriMoneyTotal += float(stock["StockOriMoney"])
        #     StockNowMoneyTotal += float(stock["StockNowMoney"])

        #     # print("--", StockNowMoneyTotal, StockOriMoneyTotal)

        # balanceDict = dict()
        # balanceDict["RemainMoney"] = 0

        # Rate = 1200

        # if st == "USD":

        #     for data in result:
        #         if data["crcy_cd"] == "USD":
        #             # 예수금 총금액 (즉 주문가능 금액)
        #             balanceDict["RemainMoney"] = (
        #                 float(data["frcr_dncl_amt_2"])
        #                 - float(data["frcr_buy_amt_smtl"])
        #                 + float(data["frcr_sll_amt_smtl"])
        #             )  # 모의계좌는 0으로 나온다 이유는 모르겠음!
        #             Rate = data["frst_bltn_exrt"]
        #             break

        #     result = res.json()["output3"]

        #     # 임시로 모의 계좌 잔고가 0으로
        #     if (
        #         common.GetNowDist() == "VIRTUAL"
        #         and float(balanceDict["RemainMoney"]) == 0
        #     ):

        #         # 주식 총 평가 금액
        #         balanceDict["stock_money"] = (
        #             StockNowMoneyTotal  # (float(result['evlu_amt_smtl_amt']) / float(Rate))
        #         )
        #         # 평가 손익 금액
        #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
        #             StockOriMoneyTotal
        #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

        #         balanceDict["RemainMoney"] = float(result["frcr_evlu_tota"]) / float(
        #             Rate
        #         )

        #         # 총 평가 금액
        #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
        #             balanceDict["RemainMoney"]
        #         )

        #     else:

        #         # 주식 총 평가 금액
        #         balanceDict["stock_money"] = (
        #             StockNowMoneyTotal  # (float(result['evlu_amt_smtl_amt']) / float(Rate))
        #         )
        #         # 평가 손익 금액
        #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
        #             StockOriMoneyTotal
        #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

        #         # 총 평가 금액
        #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
        #             balanceDict["RemainMoney"]
        #         )

        # else:

        #     for data in result:
        #         if data["crcy_cd"] == "USD":
        #             Rate = data["frst_bltn_exrt"]
        #             # 예수금 총금액 (즉 주문가능현금)
        #             balanceDict["RemainMoney"] = (
        #                 float(data["frcr_dncl_amt_2"])
        #                 - float(data["frcr_buy_amt_smtl"])
        #                 + float(data["frcr_sll_amt_smtl"])
        #             ) * float(Rate)
        #             # balanceDict['RemainMoney'] = data['frcr_evlu_amt2'] #모의계좌는 0으로 나온다 이유는 모르겠음!

        #             break

        #     # print("balanceDict['RemainMoney'] ", balanceDict['RemainMoney'] )

        #     result = res.json()["output3"]

        #     # 임시로 모의 계좌 잔고가 0으로 나오면
        #     if (
        #         common.GetNowDist() == "VIRTUAL"
        #         and float(balanceDict["RemainMoney"]) == 0
        #     ):

        #         # 주식 총 평가 금액
        #         balanceDict["stock_money"] = (
        #             StockNowMoneyTotal  # result['evlu_amt_smtl_amt']
        #         )
        #         # 평가 손익 금액
        #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
        #             StockOriMoneyTotal
        #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

        #         balanceDict["RemainMoney"] = float(result["frcr_evlu_tota"])

        #         # 총 평가 금액
        #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
        #             balanceDict["RemainMoney"]
        #         )

        #     else:

        #         # 주식 총 평가 금액
        #         balanceDict["stock_money"] = (
        #             StockNowMoneyTotal  # result['evlu_amt_smtl_amt']
        #         )
        #         # 평가 손익 금액
        #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
        #             StockOriMoneyTotal
        #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

        #         # 총 평가 금액
        #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
        #             balanceDict["RemainMoney"]
        #         )

        # return balanceDict

    raise InvestAppException(ExeptionType.FAILED_TO_GET_BALANCE, res.text)


def get_current_price(info: KisInfo, ticker: str) -> float:
    if ticker.isdigit():
        return _get_current_price_kr(info, ticker)

    return _get_current_price_us(ticker)


def _get_current_price_kr(info: KisInfo, ticker: str) -> float:
    URL = f"{info.url_base}/uapi/domestic-stock/v1/quotations/inquire-price"

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {info.token}",
        "appKey": info.app_key,
        "appSecret": info.secret_key,
        "tr_id": "FHKST01010100",
    }

    params = {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": ticker}

    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        return int(res.json()["output"]["stck_prpr"])

    raise InvestAppException(ExeptionType.FAILED_TO_GET_CURRENT_PRICE, res.text)


def _get_current_price_us(ticker: str) -> float:
    stock = yf.Ticker(ticker)

    return stock.info["currentPrice"]
