# -*- coding: utf-8 -*-
"""

아래 구글 드라이브 링크에 권한 요청을 해주세요!
이후 업데이트 사항은 여기서 실시간으로 편하게 다운로드 하시면 됩니다. (클래스 구독이 끝나더라도..)
https://drive.google.com/drive/folders/1mKGGR355vmBCxB7A3sOOSh8-gQs1CiMF?usp=drive_link



클래스 진행하면서 채워나가는 구성이지만
학습 편의를 위해 최종 버전의 코드를 제공합니다. 

변경될 일은 거의 없지만 만의 하나 변경이 이후 생긴다면 수정본은 
맨 마지막 Outro-2 강의 수업자료에 먼저 반영되니 그 코드를 최종본이라 생각하고 받으시면 됩니다.
구독이 끝났다면 위 구글 드라이브 링크에서 다운로드 하세요!(실시간 업데이트!)

공통 모듈 중 KIS_common.py만 클래스 진행하시면 계속 내용이 추가 수정 되며 Outro-2에 최종본이라고 생각하시면 되는데
다계좌매매를 위해서는 챕터8을 수강하셔서 자신만의 계좌상황에 맞게 수정해야 합니다.


하다가 잘 안되시면 계속 내용이 추가되고 있는 아래 FAQ를 꼭꼭 체크하시고

주식/코인 자동매매 FAQ
https://blog.naver.com/zacra/223203988739

그래도 안 된다면 구글링 해보시고
그래도 모르겠다면 클래스 댓글, 블로그 댓글, 단톡방( https://blog.naver.com/zacra/223111402375 )에 질문주세요! ^^

클래스 제작 후 전략의 많은 발전이 있었습니다.
백테스팅으로 검증해보고 실제로 제가 현재 돌리는 최신 전략을 완강 후 제 블로그에서 체크해 보셔요!
https://blog.naver.com/zacra

기다릴게요 ^^!

"""
from domain import kis_common as common
import requests
import json
from datetime import datetime
from pytz import timezone
import pprint
import math
import time
import pandas as pd
from pykrx import stock

from domain.env.env_type import EnvType
from domain.env import env


# 오늘 개장일인지 조회! (휴장일이면 'N'을 리턴!)
def is_today_open_check():
    time.sleep(0.2)

    now_time = datetime.now(timezone("Asia/Seoul"))
    formattedDate = now_time.strftime("%Y%m%d")
    pprint.pprint(formattedDate)

    PATH = "uapi/domestic-stock/v1/quotations/chk-holiday"
    URL = f"{env.get_url_base()}/{PATH}"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {env.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": "CTCA0903R",
    }

    params = {"BASS_DT": formattedDate, "CTX_AREA_NK": "", "CTX_AREA_FK": ""}

    # 호출
    res = requests.get(URL, headers=headers, params=params)
    # pprint.pprint(res.json())

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        DayList = res.json()["output"]

        IsOpen = "Y"
        for dayInfo in DayList:
            if dayInfo["bass_dt"] == formattedDate:
                IsOpen = dayInfo["opnd_yn"]
                break

        return IsOpen

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 시장이 열렸는지 여부 체크! #토요일 일요일은 확실히 안열리니깐 제외!
def is_market_open():
    now_time = datetime.now(timezone("Asia/Seoul"))
    pprint.pprint(now_time)

    date_week = now_time.weekday()

    # 주말은 무조건 장이 안열리니 False 리턴!
    if date_week == 5 or date_week == 6:
        return False

    # 9시 부터 3시 반
    if (
        now_time.hour < 9
        or now_time.hour > 16
        or (now_time.hour == 15 and now_time.minute >= 30)
    ):
        print("Time is NO!!!")
        return False

    # 평일 장 시간이어도 공휴일같은날 장이 안열린다.
    print("Time is OK... but one more checked!!!")

    NowDist = common.get_now_dist()
    try:
        # 가상 계좌면 메세지 통일을 위해 실계좌에서 가짜 주문 취소 주문을 넣는다!
        if common.get_now_dist() == EnvType.VIRTUAL:

            common.set_change_mode(EnvType.REAL)
            result = make_sell_limit_order("069500", 1, 1, "CHECK")
            common.set_change_mode(EnvType.VIRTUAL)

        else:
            result = make_sell_limit_order("069500", 1, 1, "CHECK")

    except Exception as e:
        common.set_change_mode(NowDist)
        print("EXCEPTION ", e)

    # 장운영시간이 아니라고 리턴되면 장이 닫힌거다!
    if result == "APBK0918" or result == "APBK0919" or is_today_open_check() == "N":
        print("Market is Close!!")
        return False

    # 아니라면 열린거다
    if result == "EGW00123":
        print("Token is failed...So You need Action!!")

    print("Market is Open!!")
    return True


# price_pricision 호가 단위에 맞게 변형해준다. 지정가 매매시 사용
def price_adjust(price, stock_code):

    NowPrice = get_current_price(stock_code)

    price = int(price)

    data = get_current_status(stock_code)
    if data["StockMarket"] == "ETF" or price <= NowPrice:
        hoga = get_hoga(stock_code)
        adjust_price = math.floor(price / hoga) * hoga
        return adjust_price

    # 호가를 직접 구해서 개선!!!
    hoga = 1
    if price < 2000:
        hoga = 1
    elif price < 5000:
        hoga = 5
    elif price < 20000:
        hoga = 10
    elif price < 50000:
        hoga = 50
    elif price < 200000:
        hoga = 100
    elif price < 500000:
        hoga = 500
    elif price >= 500000:
        hoga = 1000

    adjust_price = math.floor(price / hoga) * hoga

    return adjust_price


# 나의 계좌 잔고!
def get_balance() -> dict:

    # 퇴직연금(29) 반영
    if int(env.get_account_prd_no()) == 29:
        return get_balance_IRP()

    time.sleep(0.2)

    PATH = "uapi/domestic-stock/v1/trading/inquire-balance"
    URL = f"{env.get_url_base()}/{PATH}"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": env.get_tr_id_get_balance(),
        "custtype": "P",
    }

    params = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
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

    # 호출
    res = requests.get(URL, headers=headers, params=params)
    # pprint.pprint(res.json())
    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        result = res.json()["output2"][0]
        # pprint.pprint(result)

        balanceDict = dict()
        # 주식 총 평가 금액
        balanceDict["StockMoney"] = float(result["scts_evlu_amt"])
        # 평가 손익 금액
        balanceDict["StockRevenue"] = float(result["evlu_pfls_smtl_amt"])

        # 총 평가 금액
        balanceDict["total_money"] = float(result["tot_evlu_amt"])

        # 예수금이 아예 0이거나 총평가금액이랑 주식평가금액이 같은 상황일때는.. 좀 이상한 특이사항이다 풀매수하더라도 1원이라도 남을 테니깐
        # 퇴직연금 계좌에서 tot_evlu_amt가 제대로 반영이 안되는 경우가 있는데..이때는 전일 총평가금액을 가져오도록 한다!
        if (
            float(result["dnca_tot_amt"]) == 0
            or balanceDict["total_money"] == balanceDict["StockMoney"]
        ):
            # 장이 안열린 상황을 가정
            # if is_market_open() == False:
            balanceDict["total_money"] = float(result["bfdy_tot_asst_evlu_amt"])

        # 예수금 총금액 (즉 주문가능현금)
        balanceDict["RemainMoney"] = float(balanceDict["total_money"]) - float(
            balanceDict["StockMoney"]
        )  # result['dnca_tot_amt']

        # 그래도 아직도 남은 금액이 0이라면 dnca_tot_amt 예수금 항목에서 정보를 가지고 온다
        if balanceDict["RemainMoney"] == 0:
            balanceDict["RemainMoney"] = float(result["dnca_tot_amt"])

        return balanceDict

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 나의 계좌 잔고!
def get_balance_IRP():

    time.sleep(0.2)

    PATH = "uapi/domestic-stock/v1/trading/pension/inquire-balance"
    URL = f"{env.get_url_base()}/{PATH}"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": env.get_tr_id_get_balance(),
        "custtype": "P",
    }

    params = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "ACCA_DVSN_CD": "00",
        "INQR_DVSN": "00",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": "",
    }

    # 호출
    res = requests.get(URL, headers=headers, params=params)
    # pprint.pprint(res.json())
    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        result = res.json()["output2"][0]

        # pprint.pprint(result)

        balanceDict = dict()
        # 주식 총 평가 금액
        balanceDict["StockMoney"] = float(result["scts_evlu_amt"])
        # 평가 손익 금액
        balanceDict["StockRevenue"] = float(result["evlu_pfls_smtl_amt"])

        Data = adjust_possible_buy_info_IRP("069500", 9140, "LIMIT")

        # 예수금 총금액 (즉 주문가능현금)
        balanceDict["RemainMoney"] = float(
            Data["RemainMoney"]
        )  # float(balanceDict['total_money']) - float(balanceDict['StockMoney'])

        # 총 평가 금액
        balanceDict["total_money"] = (
            balanceDict["StockMoney"] + balanceDict["RemainMoney"]
        )

        return balanceDict

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 한국 보유 주식 리스트!
def get_my_stock_list():

    PATH = "uapi/domestic-stock/v1/trading/inquire-balance"
    URL = f"{env.get_url_base()}/{PATH}"

    StockList = list()

    DataLoad = True

    FKKey = ""
    NKKey = ""
    PrevNKKey = ""
    tr_cont = ""

    count = 0

    # 드물지만 보유종목이 아주 많으면 한 번에 못가져 오므로 SeqKey를 이용해 연속조회를 하기 위한 반복 처리
    while DataLoad:

        time.sleep(0.2)
        # 헤더 설정
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {common.get_token()}",
            "appKey": env.get_app_key(),
            "appSecret": env.get_app_secret(),
            "tr_id": env.get_tr_id_get_balance(),
            "tr_cont": tr_cont,
            "custtype": "P",
        }

        params = {
            "CANO": env.get_account_no(),
            "ACNT_PRDT_CD": env.get_account_prd_no(),
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "",
            "INQR_DVSN": "01",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "00",
            "CTX_AREA_FK100": FKKey,
            "CTX_AREA_NK100": NKKey,
        }

        # 호출
        res = requests.get(URL, headers=headers, params=params)

        if res.headers["tr_cont"] == "M" or res.headers["tr_cont"] == "F":
            tr_cont = "N"
        else:
            tr_cont = ""

        if res.status_code == 200 and res.json()["rt_cd"] == "0":

            NKKey = res.json()["ctx_area_nk100"].strip()
            if NKKey != "":
                print("---> CTX_AREA_NK100: ", NKKey)

            FKKey = res.json()["ctx_area_fk100"].strip()
            if FKKey != "":
                print("---> CTX_AREA_FK100: ", FKKey)

            if PrevNKKey == NKKey:
                DataLoad = False
            else:
                PrevNKKey = NKKey

            if NKKey == "":
                DataLoad = False

            ResultList = res.json()["output1"]
            # pprint.pprint(ResultList)

            for stock in ResultList:
                # 잔고 수량이 0 이상인것만
                if int(stock["hldg_qty"]) > 0:

                    StockInfo = dict()

                    StockInfo["stock_code"] = stock["pdno"]
                    StockInfo["stock_name"] = stock["prdt_name"]
                    StockInfo["stock_amt"] = stock["hldg_qty"]
                    StockInfo["stock_avg_price"] = stock["pchs_avg_pric"]
                    StockInfo["StockOriMoney"] = stock["pchs_amt"]
                    StockInfo["stock_now_money"] = stock["evlu_amt"]
                    StockInfo["StockNowPrice"] = stock["prpr"]
                    # StockInfo["StockNowRate"] = stock['fltt_rt'] #등락률인데 해외 주식에는 없어서 통일성을 위해 여기도 없앰 ㅎ
                    StockInfo["stock_revenue_rate"] = stock["evlu_pfls_rt"]
                    StockInfo["stock_revenue_money"] = stock["evlu_pfls_amt"]

                    Is_Duple = False
                    for exist_stock in StockList:
                        if exist_stock["stock_code"] == StockInfo["stock_code"]:
                            Is_Duple = True
                            break

                    if Is_Duple == False:
                        StockList.append(StockInfo)

        else:
            print("Error Code : " + str(res.status_code) + " | " + res.text)
            # return res.json()["msg_cd"]

            if res.json()["msg_cd"] == "EGW00123":
                DataLoad = False

            count += 1
            if count > 10:
                DataLoad = False

    return StockList


############################################################################################################################################################


# 국내 주식현재가 시세
def get_current_price(stock_code):
    time.sleep(0.2)

    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{env.get_url_base()}/{PATH}"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": "FHKST01010100",
    }

    params = {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": stock_code}

    # 호출
    res = requests.get(URL, headers=headers, params=params)
    # pprint.pprint(res.json())

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        return int(res.json()["output"]["stck_prpr"])

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 국내 주식 호가 단위!
def get_hoga(stock_code):
    time.sleep(0.2)

    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{env.get_url_base()}/{PATH}"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": "FHKST01010100",
    }

    params = {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": stock_code}

    # 호출
    res = requests.get(URL, headers=headers, params=params)
    # pprint.pprint(res.json())

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        return int(res.json()["output"]["aspr_unit"])

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 국내 주식 이름
def get_stock_name(stock_code):
    time.sleep(0.2)

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{env.get_url_base()}/{PATH}"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": "FHKST03010100",
    }

    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": stock_code,
        "FID_INPUT_DATE_1": common.get_from_now_date_str("KR", "NONE", -7),
        "FID_INPUT_DATE_2": common.get_now_date_str("KR"),
        "FID_PERIOD_DIV_CODE": "D",
        "FID_ORG_ADJ_PRC": "0",
    }

    # 호출
    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        return res.json()["output1"]["hts_kor_isnm"]

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 퀀트 투자를 위한 함수!
# 국내 주식 시총, PER, PBR, EPS, PBS 구해서 리턴하기!
def get_current_status(stock_code):
    time.sleep(0.2)

    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{env.get_url_base()}/{PATH}"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": "FHKST01010100",
    }

    params = {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": stock_code}

    # 호출
    res = requests.get(URL, headers=headers, params=params)
    # pprint.pprint(res.json())

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        result = res.json()["output"]

        # pprint.pprint(result)

        stockDataDict = dict()
        stockDataDict["stock_code"] = stock_code
        stockDataDict["stock_name"] = get_stock_name(stock_code)
        stockDataDict["StockNowPrice"] = int(result["stck_prpr"])
        stockDataDict["StockMarket"] = result[
            "rprs_mrkt_kor_name"
        ]  # ETF인지 코스피, 코스닥인지

        try:
            stockDataDict["StockDistName"] = result[
                "bstp_kor_isnm"
            ]  # 금융주 등을 제외 하기 위해!!
        except Exception as e:
            stockDataDict["StockDistName"] = ""

        stockDataDict["StockNowStatus"] = result[
            "iscd_stat_cls_code"
        ]  # 관리종목,투자경고,투자주의,거래정지,단기과열을 제끼기 위해

        try:
            stockDataDict["StockMarketCap"] = float(result["hts_avls"])  # 시총
        except Exception as e:
            stockDataDict["StockMarketCap"] = 0

        try:
            stockDataDict["StockPER"] = float(result["per"])  # PER
        except Exception as e:
            stockDataDict["StockPER"] = 0

        try:
            stockDataDict["StockPBR"] = float(result["pbr"])  # PBR
        except Exception as e:
            stockDataDict["StockPBR"] = 0

        try:
            stockDataDict["StockEPS"] = float(result["eps"])  # EPS
        except Exception as e:
            stockDataDict["StockEPS"] = 0

        try:
            stockDataDict["StockBPS"] = float(result["bps"])  # BPS
        except Exception as e:
            stockDataDict["StockBPS"] = 0

        return stockDataDict

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


############################################################################################################################################################
# 시장가 주문하기!
def make_buy_market_order(stockcode, amt, adjustAmt=False):

    # 매수가능 수량으로 보정할지 여부
    if adjustAmt == True:
        try:
            # 매수 가능한수량으로 보정
            amt = adjust_possible_amt(stockcode, amt, "MARKET")

        except Exception as e:
            print("Exception")

    # 퇴직연금(29) 반영
    if int(env.get_account_prd_no()) == 29:
        return make_buy_market_order_IRP(stockcode, amt)

    time.sleep(0.2)

    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{env.get_url_base()}/{PATH}"
    data = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "PDNO": stockcode,
        "ORD_DVSN": "01",
        "ORD_QTY": str(int(amt)),
        "ORD_UNPR": "0",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": env.get_tr_id_buy(),
        "custtype": "P",
        "hashkey": common.get_hash_key(data),
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        order = res.json()["output"]

        OrderInfo = dict()

        OrderInfo["OrderNum"] = order["KRX_FWDG_ORD_ORGNO"]
        OrderInfo["OrderNum2"] = order["ODNO"]
        OrderInfo["OrderTime"] = order["ORD_TMD"]

        return OrderInfo

    print("Error Code : " + str(res.status_code) + " | " + res.text)

    if res.json()["msg_cd"] == "APBK1744":
        make_buy_market_order_IRP(stockcode, amt)

    return res.json()["msg_cd"]


# 시장가 매도하기!
def make_sell_market_order(stockcode, amt):

    # 퇴직연금(29) 반영
    if int(env.get_account_prd_no()) == 29:
        return make_sell_market_order_IRP(stockcode, amt)

    time.sleep(0.2)

    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{env.get_url_base()}/{PATH}"
    data = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "PDNO": stockcode,
        "ORD_DVSN": "01",
        "ORD_QTY": str(int(amt)),
        "ORD_UNPR": "0",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": env.get_tr_id_sell(),
        "custtype": "P",
        "hashkey": common.get_hash_key(data),
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        order = res.json()["output"]

        OrderInfo = dict()

        OrderInfo["OrderNum"] = order["KRX_FWDG_ORD_ORGNO"]
        OrderInfo["OrderNum2"] = order["ODNO"]
        OrderInfo["OrderTime"] = order["ORD_TMD"]

        return OrderInfo

    print("Error Code : " + str(res.status_code) + " | " + res.text)

    if res.json()["msg_cd"] == "APBK1744":
        make_sell_market_order_IRP(stockcode, amt)

    return res.json()["msg_cd"]


# 지정가 주문하기!
def make_buy_limit_order(stockcode, amt, price, adjustAmt=False, ErrLog="NO"):

    # 매수가능 수량으로 보정할지 여부
    if adjustAmt == True:
        try:
            # 매수 가능한수량으로 보정
            amt = adjust_possible_amt(stockcode, amt, "LIMIT")

        except Exception as e:
            print("Exception")

    # 퇴직연금(29) 반영
    if int(env.get_account_prd_no()) == 29:
        return make_buy_limit_order_IRP(stockcode, amt, price)

    time.sleep(0.2)

    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{env.get_url_base()}/{PATH}"
    data = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "PDNO": stockcode,
        "ORD_DVSN": "00",
        "ORD_QTY": str(int(amt)),
        "ORD_UNPR": str(price_adjust(price, stockcode)),
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": env.get_tr_id_buy(),
        "custtype": "P",
        "hashkey": common.get_hash_key(data),
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        order = res.json()["output"]

        OrderInfo = dict()

        OrderInfo["OrderNum"] = order["KRX_FWDG_ORD_ORGNO"]
        OrderInfo["OrderNum2"] = order["ODNO"]
        OrderInfo["OrderTime"] = order["ORD_TMD"]
        return OrderInfo

    if ErrLog == "YES":
        print("Error Code : " + str(res.status_code) + " | " + res.text)

    if res.json()["msg_cd"] == "APBK1744":
        make_buy_limit_order_IRP(stockcode, amt, price)

    return res.json()["msg_cd"]


# 지정가 매도하기!
def make_sell_limit_order(stockcode, amt, price, ErrLog="YES"):

    time.sleep(0.2)

    # 퇴직연금(29) 반영
    if int(env.get_account_prd_no()) == 29:
        return make_sell_limit_order_IRP(stockcode, amt, price)

    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{env.get_url_base()}/{PATH}"
    data = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "PDNO": stockcode,
        "ORD_DVSN": "00",
        "ORD_QTY": str(int(amt)),
        "ORD_UNPR": str(price_adjust(price, stockcode)),
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": env.get_tr_id_sell(),
        "custtype": "P",
        "hashkey": common.get_hash_key(data),
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        order = res.json()["output"]

        OrderInfo = dict()

        OrderInfo["OrderNum"] = order["KRX_FWDG_ORD_ORGNO"]
        OrderInfo["OrderNum2"] = order["ODNO"]
        OrderInfo["OrderTime"] = order["ORD_TMD"]

        return OrderInfo

    if ErrLog == "YES":
        print("Error Code : " + str(res.status_code) + " | " + res.text)

    if res.json()["msg_cd"] == "APBK1744":
        make_sell_limit_order_IRP(stockcode, amt, price)

    return res.json()["msg_cd"]


# 보유한 주식을 모두 시장가 매도하는 극단적 함수
def sell_all_stock():
    StockList = get_my_stock_list()

    # 시장가로 모두 매도 한다
    for stock_info in StockList:
        pprint.pprint(
            make_sell_market_order(stock_info["stock_code"], stock_info["stock_amt"])
        )


############# #############   IRP 계좌를 위한 매수 매도 함수   ############# ############# #############


# 시장가 주문하기!
def make_buy_market_order_IRP(stockcode, amt):

    time.sleep(0.2)

    TrId = "TTTC0502U"

    PATH = "uapi/domestic-stock/v1/trading/order-pension"
    URL = f"{env.get_url_base()}/{PATH}"
    data = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "SLL_BUY_DVSN_CD": "02",
        "SLL_TYPE": "01",
        "ORD_DVSN": "01",
        "PDNO": stockcode,
        "LNKD_ORD_QTY": str(int(amt)),
        "LNKD_ORD_UNPR": "0",
        "RVSE_CNCL_DVSN_CD": "00",
        "KRX_FWDG_ORD_ORGNO": "",
        "ORGN_ODNO": "",
        "CTAC_TLNO": "",
        "ACCA_DVSN_CD": "01",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": TrId,
        "custtype": "P",
        "hashkey": common.get_hash_key(data),
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        order = res.json()["output"]

        OrderInfo = dict()

        OrderInfo["OrderNum"] = order["KRX_FWDG_ORD_ORGNO"]
        OrderInfo["OrderNum2"] = order["ODNO"]
        OrderInfo["OrderTime"] = order["ORD_TMD"]
        return OrderInfo

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 시장가 매도하기!
def make_sell_market_order_IRP(stockcode, amt):

    time.sleep(0.2)

    TrId = "TTTC0502U"

    PATH = "uapi/domestic-stock/v1/trading/order-pension"
    URL = f"{env.get_url_base()}/{PATH}"
    data = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "SLL_BUY_DVSN_CD": "01",
        "SLL_TYPE": "01",
        "ORD_DVSN": "01",
        "PDNO": stockcode,
        "LNKD_ORD_QTY": str(int(amt)),
        "LNKD_ORD_UNPR": "0",
        "RVSE_CNCL_DVSN_CD": "00",
        "KRX_FWDG_ORD_ORGNO": "",
        "ORGN_ODNO": "",
        "CTAC_TLNO": "",
        "ACCA_DVSN_CD": "01",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": TrId,
        "custtype": "P",
        "hashkey": common.get_hash_key(data),
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        order = res.json()["output"]

        OrderInfo = dict()

        OrderInfo["OrderNum"] = order["KRX_FWDG_ORD_ORGNO"]
        OrderInfo["OrderNum2"] = order["ODNO"]
        OrderInfo["OrderTime"] = order["ORD_TMD"]

        return OrderInfo

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 지정가 주문하기!
def make_buy_limit_order_IRP(stockcode, amt, price, ErrLog="YES"):

    time.sleep(0.2)

    TrId = "TTTC0502U"

    PATH = "uapi/domestic-stock/v1/trading/order-pension"
    URL = f"{env.get_url_base()}/{PATH}"
    data = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "SLL_BUY_DVSN_CD": "02",
        "SLL_TYPE": "01",
        "ORD_DVSN": "00",
        "PDNO": stockcode,
        "LNKD_ORD_QTY": str(int(amt)),
        "LNKD_ORD_UNPR": str(price_adjust(price, stockcode)),
        "RVSE_CNCL_DVSN_CD": "00",
        "KRX_FWDG_ORD_ORGNO": "",
        "ORGN_ODNO": "",
        "CTAC_TLNO": "",
        "ACCA_DVSN_CD": "01",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": TrId,
        "custtype": "P",
        "hashkey": common.get_hash_key(data),
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        order = res.json()["output"]

        OrderInfo = dict()

        OrderInfo["OrderNum"] = order["KRX_FWDG_ORD_ORGNO"]
        OrderInfo["OrderNum2"] = order["ODNO"]
        OrderInfo["OrderTime"] = order["ORD_TMD"]

        return OrderInfo

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 지정가 매도하기!
def make_sell_limit_order_IRP(stockcode, amt, price, ErrLog="YES"):

    time.sleep(0.2)

    TrId = "TTTC0502U"

    PATH = "uapi/domestic-stock/v1/trading/order-pension"
    URL = f"{env.get_url_base()}/{PATH}"
    data = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "SLL_BUY_DVSN_CD": "01",
        "SLL_TYPE": "01",
        "ORD_DVSN": "00",
        "PDNO": stockcode,
        "LNKD_ORD_QTY": str(int(amt)),
        "LNKD_ORD_UNPR": str(price_adjust(price, stockcode)),
        "RVSE_CNCL_DVSN_CD": "00",
        "KRX_FWDG_ORD_ORGNO": "",
        "ORGN_ODNO": "",
        "CTAC_TLNO": "",
        "ACCA_DVSN_CD": "01",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": TrId,
        "custtype": "P",
        "hashkey": common.get_hash_key(data),
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        order = res.json()["output"]

        OrderInfo = dict()

        OrderInfo["OrderNum"] = order["KRX_FWDG_ORD_ORGNO"]
        OrderInfo["OrderNum2"] = order["ODNO"]
        OrderInfo["OrderTime"] = order["ORD_TMD"]

        return OrderInfo

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 보유한 주식을 모두 시장가 매도하는 극단적 함수
def sell_all_stock_IRP():
    StockList = get_my_stock_list()

    # 시장가로 모두 매도 한다
    for stock_info in StockList:
        pprint.pprint(
            make_sell_market_order_IRP(
                stock_info["stock_code"], stock_info["stock_amt"]
            )
        )


############################################################################################################################################################


############################################################################################################################################################


# 매수 가능한지 체크 하기!
def check_possible_buy_info(stockcode, price, type):

    time.sleep(0.2)

    PATH = "uapi/domestic-stock/v1/trading/inquire-psbl-order"
    URL = f"{env.get_url_base()}/{PATH}"

    type_code = "00"  # 지정가
    if type.upper() == "MAREKT":
        type_code = "01"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": env.get_tr_id_psbl_order(),
        "custtype": "P",
    }

    params = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "PDNO": stockcode,
        "ORD_UNPR": str(price_adjust(price, stockcode)),
        "ORD_DVSN": type_code,
        "CMA_EVLU_AMT_ICLD_YN": "N",
        "OVRS_ICLD_YN": "N",
    }

    # 호출
    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        result = res.json()["output"]
        #        pprint.pprint(result)

        CheckDict = dict()

        CheckDict["RemainMoney"] = result["nrcvb_buy_amt"]
        CheckDict["MaxAmt"] = result["nrcvb_buy_qty"]

        return CheckDict

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 매수 가능한수량으로 보정
def adjust_possible_amt(stockcode, amt, type):
    NowPrice = get_current_price(stockcode)

    data = None

    # 퇴직연금(29) 반영
    if int(env.get_account_prd_no()) == 29:
        data = adjust_possible_buy_info_IRP(stockcode, NowPrice, type)
    else:
        data = check_possible_buy_info(stockcode, NowPrice, type)

    MaxAmt = int(data["MaxAmt"])

    if MaxAmt <= int(amt):
        print("!!!!!!!!!!!!MaxAmt Over!!!!!!!!!!!!!!!!!!")
        return MaxAmt

    print("!!!!!!!!!!!!Amt OK!!!!!!!!!!!!!!!!!!")
    return int(amt)


# 매수 가능한지 체크 하기! -IRP 계좌
def adjust_possible_buy_info_IRP(stockcode, price, type):

    time.sleep(0.2)

    PATH = "uapi/domestic-stock/v1/trading/pension/inquire-psbl-order"
    URL = f"{env.get_url_base()}/{PATH}"

    TrId = "TTTC0503R"

    type_code = "00"  # 지정가
    if type.upper() == "MAREKT":
        type_code = "01"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": TrId,
        "custtype": "P",
    }

    params = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "PDNO": stockcode,
        "ORD_UNPR": str(price_adjust(price, stockcode)),
        "ORD_DVSN": type_code,
        "CMA_EVLU_AMT_ICLD_YN": "N",
        "ACCA_DVSN_CD": "00",
    }

    # 호출
    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        result = res.json()["output"]
        #        pprint.pprint(result)

        CheckDict = dict()

        CheckDict["RemainMoney"] = result["max_buy_amt"]
        CheckDict["MaxAmt"] = result["max_buy_qty"]

        return CheckDict

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


############################################################################################################################################################


# 주문 리스트를 얻어온다! 종목 코드, side는 ALL or BUY or SELL, 상태는 OPEN or CLOSE
def get_order_list(stockcode="", side="ALL", status="ALL", limit=5):

    time.sleep(0.2)

    sell_buy_code = "00"
    if side.upper() == "BUY":
        sell_buy_code = "02"
    elif side.upper() == "SELL":
        sell_buy_code = "01"
    else:
        sell_buy_code = "00"

    status_code = "00"
    if status.upper() == "OPEN":
        status_code = "02"
    elif status.upper() == "CLOSE":
        status_code = "01"
    else:
        status_code = "00"

    PATH = "uapi/domestic-stock/v1/trading/inquire-daily-ccld"
    URL = f"{env.get_url_base()}/{PATH}"

    params = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "INQR_STRT_DT": common.get_from_now_date_str("KR", "NONE", -limit),
        "INQR_END_DT": common.get_now_date_str("KR"),
        "SLL_BUY_DVSN_CD": sell_buy_code,
        "INQR_DVSN": "00",
        "PDNO": stockcode,
        "CCLD_DVSN": status_code,
        "ORD_GNO_BRNO": "",
        "ODNO": "",
        "INQR_DVSN_3": "00",
        "INQR_DVSN_1": "",
        "INQR_DVSN_2": "",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": "",
    }

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": env.get_tr_id_order_list(),
        "custtype": "P",
        "hashkey": common.get_hash_key(params),
    }

    res = requests.get(URL, headers=headers, params=params)
    # pprint.pprint(res.json())

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        ResultList = res.json()["output1"]

        OrderList = list()
        # pprint.pprint(ResultList)

        for order in ResultList:
            # 잔고 수량이 0 이상인것만

            OrderInfo = dict()

            OrderInfo["OrderStock"] = order["pdno"]
            OrderInfo["OrderStockName"] = order["prdt_name"]

            # 주문 구분
            if order["ord_dvsn_cd"] == "00":
                OrderInfo["OrderType"] = "Limit"
            else:
                OrderInfo["OrderType"] = "Market"

            # 주문 사이드
            if order["sll_buy_dvsn_cd"] == "01":
                OrderInfo["OrderSide"] = "Sell"
            else:
                OrderInfo["OrderSide"] = "Buy"

            # 주문 상태
            if (
                float(order["ord_qty"])
                - (float(order["tot_ccld_qty"]) + float(order["cncl_cfrm_qty"]))
                == 0
            ):
                OrderInfo["OrderSatus"] = "Close"
            else:
                OrderInfo["OrderSatus"] = "Open"

            if common.get_now_date_str("KR") != order["ord_dt"]:
                OrderInfo["OrderSatus"] = "Close"

            # 주문 수량~
            OrderInfo["OrderAmt"] = int(float(order["ord_qty"]))

            # 주문 최종 수량~
            OrderInfo["OrderResultAmt"] = int(
                float(order["tot_ccld_qty"]) + float(order["cncl_cfrm_qty"])
            )

            # 주문넘버..
            OrderInfo["OrderNum"] = order["ord_gno_brno"]
            OrderInfo["OrderNum2"] = order["odno"]

            # 아직 미체결 주문이라면 주문 단가를
            if OrderInfo["OrderSatus"] == "Open":
                OrderInfo["OrderAvgPrice"] = order["ord_unpr"]

            # 체결된 주문이면 평균체결금액을!
            else:
                OrderInfo["OrderAvgPrice"] = order["avg_prvs"]

            OrderInfo["OrderIsCancel"] = order["cncl_yn"]  # 주문 취소 여부!
            OrderInfo["OrderMarket"] = "KOR"  # 마켓인데 미국과 통일성을 위해!

            OrderInfo["OrderDate"] = order["ord_dt"]
            OrderInfo["OrderTime"] = order["ord_tmd"]

            Is_Ok = False

            if status == "ALL":
                Is_Ok = True
            else:
                if status.upper() == OrderInfo["OrderSatus"].upper():
                    Is_Ok = True

            if Is_Ok == True:
                Is_Ok = False

                if side.upper() == "ALL":
                    Is_Ok = True
                else:
                    if side.upper() == OrderInfo["OrderSide"].upper():
                        Is_Ok = True

            if Is_Ok == True:
                if stockcode != "":
                    if stockcode.upper() == OrderInfo["OrderStock"].upper():
                        OrderList.append(OrderInfo)
                else:
                    OrderList.append(OrderInfo)

        return OrderList

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 주문 취소/수정 함수
def cancel_modify_order(
    stockcode,
    order_num1,
    order_num2,
    order_amt,
    order_price,
    mode="CANCEL",
    order_type="LIMIT",
    order_dist="NONE",
):

    # 퇴직연금(29) 반영
    if int(env.get_account_prd_no()) == 29:
        return cancel_modify_order_IRP(
            stockcode,
            order_num1,
            order_num2,
            order_amt,
            order_price,
            mode,
            order_type,
            order_dist,
        )

    time.sleep(0.2)

    order_type = "00"
    if order_type.upper() == "MARKET":
        order_type = "01"

    mode_type = "02"
    if mode.upper() == "MODIFY":
        mode_type = "01"

    PATH = "uapi/domestic-stock/v1/trading/order-rvsecncl"
    URL = f"{env.get_url_base()}/{PATH}"
    data = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "KRX_FWDG_ORD_ORGNO": order_num1,
        "ORGN_ODNO": order_num2,
        "ORD_DVSN": order_type,
        "RVSE_CNCL_DVSN_CD": mode_type,
        "ORD_QTY": str(order_amt),
        "ORD_UNPR": str(price_adjust(order_price, stockcode)),
        "QTY_ALL_ORD_YN": "N",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": env.get_tr_id_cancel_order(),
        "custtype": "P",
        "hashkey": common.get_hash_key(data),
    }

    res = requests.post(URL, headers=headers, data=json.dumps(data))

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        order = res.json()["output"]

        OrderInfo = dict()

        OrderInfo["OrderNum"] = order["KRX_FWDG_ORD_ORGNO"]
        OrderInfo["OrderNum2"] = order["ODNO"]
        OrderInfo["OrderTime"] = order["ORD_TMD"]

        return OrderInfo

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 연금IRP 계좌 주문 취소/수정 함수
def cancel_modify_order_IRP(
    stockcode,
    order_num1,
    order_num2,
    order_amt,
    order_price,
    mode="CANCEL",
    order_type="LIMIT",
    order_dist="NONE",
):

    time.sleep(0.2)

    order_dist = "02"
    if order_dist.upper() == "SELL":
        order_dist = "01"

    order_type = "00"
    if order_type.upper() == "MARKET":
        order_type = "01"

    mode_type = "02"
    if mode.upper() == "MODIFY":
        mode_type = "01"

    TrId = "TTTC0502U"

    PATH = "uapi/domestic-stock/v1/trading/order-pension"
    URL = f"{env.get_url_base()}/{PATH}"
    data = {
        "CANO": env.get_account_no(),
        "ACNT_PRDT_CD": env.get_account_prd_no(),
        "SLL_BUY_DVSN_CD": order_dist,
        "SLL_TYPE": "01",
        "ORD_DVSN": order_type,
        "PDNO": "",
        "LNKD_ORD_QTY": str(int(order_amt)),
        "LNKD_ORD_UNPR": str(price_adjust(order_price, stockcode)),
        "RVSE_CNCL_DVSN_CD": mode_type,
        "KRX_FWDG_ORD_ORGNO": order_num1,
        "ORGN_ODNO": order_num2,
        "CTAC_TLNO": "",
        "ACCA_DVSN_CD": "01",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": TrId,
        "custtype": "P",
        "hashkey": common.get_hash_key(data),
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        order = res.json()["output"]

        OrderInfo = dict()

        OrderInfo["OrderNum"] = order["KRX_FWDG_ORD_ORGNO"]
        OrderInfo["OrderNum2"] = order["ODNO"]
        OrderInfo["OrderTime"] = order["ORD_TMD"]

        return OrderInfo

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 모든 주문을 취소하는 함수
def cancel_all_orders(stockcode="", side="ALL"):

    OrderList = get_order_list(stockcode, side)

    for order in OrderList:
        if order["OrderSatus"].upper() == "OPEN":
            pprint.pprint(
                cancel_modify_order(
                    order["OrderStock"],
                    order["OrderNum"],
                    order["OrderNum2"],
                    order["OrderAmt"],
                    order["OrderAvgPrice"],
                )
            )


# 시장가 주문 정보를 읽어서 체결 평균가를 리턴! 에러나 못가져오면 현재가를 리턴!
def get_market_order_price(stockcode, ResultOrder):
    time.sleep(0.2)

    OrderList = get_order_list(stockcode)

    OrderDonePrice = 0

    # 넘어온 주문정보와 일치하는 주문을 찾아서 평균 체결가를 세팅!
    for orderInfo in OrderList:
        if orderInfo["OrderNum"] == ResultOrder["OrderNum"] and float(
            orderInfo["OrderNum2"]
        ) == float(ResultOrder["OrderNum2"]):
            OrderDonePrice = int(orderInfo["OrderAvgPrice"])
            break

    # 혹시나 없다면 현재가로 셋팅!
    if OrderDonePrice == 0:
        OrderDonePrice = get_current_price(stockcode)

    return OrderDonePrice


############################################################################################################################################################


# p_code -> D:일, W:주, M:월, Y:년
def get_ohlcv(stock_code, p_code, adj_ok="1"):

    time.sleep(0.2)

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{env.get_url_base()}/{PATH}"

    FID_ORG_ADJ_PRC = "0"
    if adj_ok == "1":
        FID_ORG_ADJ_PRC = "0"
    else:
        FID_ORG_ADJ_PRC = "1"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": env.get_app_key(),
        "appSecret": env.get_app_secret(),
        "tr_id": "FHKST03010100",
    }

    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": stock_code,
        "FID_INPUT_DATE_1": common.get_from_now_date_str("KR", "NONE", -36500),
        "FID_INPUT_DATE_2": common.get_now_date_str("KR"),
        "FID_PERIOD_DIV_CODE": p_code,
        "FID_ORG_ADJ_PRC": FID_ORG_ADJ_PRC,
    }

    # 호출
    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        ResultList = res.json()["output2"]

        df = list()

        if len(pd.DataFrame(ResultList)) > 0:

            OhlcvList = list()

            for ohlcv in ResultList:

                if len(ohlcv) == 0:
                    continue

                OhlcvData = dict()

                try:
                    if ohlcv["stck_oprc"] != "":

                        OhlcvData["Date"] = ohlcv["stck_bsop_date"]
                        OhlcvData["open"] = float(ohlcv["stck_oprc"])
                        OhlcvData["high"] = float(ohlcv["stck_hgpr"])
                        OhlcvData["low"] = float(ohlcv["stck_lwpr"])
                        OhlcvData["close"] = float(ohlcv["stck_clpr"])
                        OhlcvData["volume"] = float(ohlcv["acml_vol"])
                        OhlcvData["value"] = float(ohlcv["acml_tr_pbmn"])

                        OhlcvList.append(OhlcvData)
                except Exception as e:
                    print("E:", e)

            if len(OhlcvList) > 0:

                df = pd.DataFrame(OhlcvList)
                df = df.set_index("Date")

                df = df.sort_values(by="Date")
                df.insert(
                    6,
                    "change",
                    (df["close"] - df["close"].shift(1)) / df["close"].shift(1),
                )

                df[["open", "high", "low", "close", "volume", "change"]] = df[
                    ["open", "high", "low", "close", "volume", "change"]
                ].apply(pd.to_numeric)

                df.index = pd.to_datetime(df.index).strftime("%Y-%m-%d")

        return df

    print("Error Code : " + str(res.status_code) + " | " + res.text)
    return res.json()["msg_cd"]


# 100개이상 가져오도록 수정!
def get_ohlcv_new(stock_code, p_code, get_count, adj_ok="1"):

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{env.get_url_base()}/{PATH}"

    FID_ORG_ADJ_PRC = "0"
    if adj_ok == "1":
        FID_ORG_ADJ_PRC = "0"
    else:
        FID_ORG_ADJ_PRC = "1"

    OhlcvList = list()

    DataLoad = True

    count = 0

    now_date = common.get_now_date_str("KR")
    date_str_start = common.GetFromDateStr(pd.to_datetime(now_date), "NONE", -100)
    date_str_end = now_date

    while DataLoad:

        time.sleep(0.2)

        print("...Data.Length..", len(OhlcvList), "-->", get_count)
        if len(OhlcvList) >= get_count:
            DataLoad = False

        # 헤더 설정
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {common.get_token()}",
            "appKey": env.get_app_key(),
            "appSecret": env.get_app_secret(),
            "tr_id": "FHKST03010100",
        }

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": stock_code,
            "FID_INPUT_DATE_1": date_str_start,
            "FID_INPUT_DATE_2": date_str_end,
            "FID_PERIOD_DIV_CODE": p_code,
            "FID_ORG_ADJ_PRC": FID_ORG_ADJ_PRC,
        }

        # 호출
        res = requests.get(URL, headers=headers, params=params)

        if res.status_code == 200 and res.json()["rt_cd"] == "0":

            ResultList = res.json()["output2"]

            df = list()

            add_cnt = 0
            if len(pd.DataFrame(ResultList)) > 0:

                for ohlcv in ResultList:

                    if len(ohlcv) == 0:
                        continue

                    OhlcvData = dict()

                    try:
                        if ohlcv["stck_oprc"] != "":

                            OhlcvData["Date"] = ohlcv["stck_bsop_date"]
                            OhlcvData["open"] = float(ohlcv["stck_oprc"])
                            OhlcvData["high"] = float(ohlcv["stck_hgpr"])
                            OhlcvData["low"] = float(ohlcv["stck_lwpr"])
                            OhlcvData["close"] = float(ohlcv["stck_clpr"])
                            OhlcvData["volume"] = float(ohlcv["acml_vol"])
                            OhlcvData["value"] = float(ohlcv["acml_tr_pbmn"])

                            Is_Duple = False

                            for exist_stock in OhlcvList:
                                if exist_stock["Date"] == OhlcvData["Date"]:
                                    Is_Duple = True
                                    break

                            if Is_Duple == False:
                                if len(OhlcvList) < get_count:
                                    OhlcvList.append(OhlcvData)
                                    add_cnt += 1

                                    date_str_end = OhlcvData["Date"]

                    except Exception as e:
                        print("E:", e)

            if add_cnt == 0:
                DataLoad = False
            else:
                date_str_start = common.GetFromDateStr(
                    pd.to_datetime(date_str_end), "NONE", -100
                )

        else:
            print("Error Code : " + str(res.status_code) + " | " + res.text)

            count += 1
            if count > 10:
                DataLoad = False

    if len(OhlcvList) > 0:
        df = pd.DataFrame(OhlcvList)
        df = df.set_index("Date")

        df = df.sort_values(by="Date")
        df.insert(
            6, "change", (df["close"] - df["close"].shift(1)) / df["close"].shift(1)
        )

        df[["open", "high", "low", "close", "volume", "change"]] = df[
            ["open", "high", "low", "close", "volume", "change"]
        ].apply(pd.to_numeric)

        df.index = pd.to_datetime(df.index).strftime("%Y-%m-%d")

        return df
    return None


# ETF의 NAV얻기
def get_ETF_NAV(stock_code, Log="N"):

    IsExcept = False
    Nav = 0

    # 영상과 다르게 먼저 네이버 크롤링해서 먼저 NAV를 가지고 온다 -> 이게 장중 실시간 NAV를 더 잘 반영!
    try:

        url = "https://finance.naver.com/item/main.naver?code=" + stock_code
        dfs = pd.read_html(url, encoding="euc-kr")
        # pprint.pprint(dfs)

        data_dict = dfs[8]

        """
        data_keys = list(data_dict.keys())
        for key in data_keys:
            print("key:",key)
            print("data_dict[key]:",data_dict[key])

            Second_Key = list(data_dict[key].keys())
            for secondkey in Second_Key:
                print("secondkey:",secondkey)
                print("data_dict[key][secondkey]:", data_dict[key][secondkey])
        """

        Nav = int(data_dict[1][0])

        time.sleep(0.3)

    except Exception as e:
        print("ex", e)
        IsExcept = True

    # 만약 실패한다면 pykrx를 이용해 NAV값을 가지고 온다
    if IsExcept == True:
        try:

            df = stock.get_etf_price_deviation(
                common.get_from_now_date_str("KR", "NONE", -5),
                common.get_now_date_str("KR"),
                stock_code,
            )

            if Log == "Y":
                pprint.pprint(df)

            if len(df) == 0:
                IsExcept = True

            Nav = df["NAV"].iloc[-1]
            print(Nav)

        except Exception as e:
            print("except!!!!!!!!")
            Nav = get_current_price(stock_code)

    return Nav


# ETF의 괴리율 구하기!
def get_ETF_gap_avg(stock_code, Log="N"):

    GapAvg = 0
    IsExcept = False

    # pykrx 모듈 통해서 괴리율 평균을 구해옴!!!
    try:
        df = stock.get_etf_price_deviation(
            common.get_from_now_date_str("KR", "NONE", -120),
            common.get_now_date_str("KR"),
            stock_code,
        )
        if Log == "Y":
            pprint.pprint(df)

        if len(df) == 0:
            IsExcept = True

        TotalGap = 0

        for idx, row in df.iterrows():

            Gap = abs(float(row["괴리율"]))

            TotalGap += Gap

        GapAvg = TotalGap / len(df)

        print("GapAvg", GapAvg)

    except Exception as e:
        IsExcept = True
        print("ex", e)

    # 만약 실패한다면 네이버 직접 크롤링을 통해 가져옴!!!!
    if IsExcept == True:
        try:

            url = "https://finance.naver.com/item/main.naver?code=" + stock_code
            dfs = pd.read_html(url, encoding="euc-kr")

            data_dict = dfs[4]

            data_list = data_dict["괴리율"].to_list()

            count = 0
            TotalGap = 0
            for data in data_list:
                if "%" in str(data):
                    Gap = float(data.replace("%", ""))
                    TotalGap += Gap
                    count += 1

            GapAvg = TotalGap / count

        except Exception as e:
            print("except!!!!!!!!")

    return GapAvg
