# -*- coding: utf-8 -*-
"""

아래 구글 드라이브 링크에 권한 요청을 해주세요!
이후 업데이트 사항은 여기서 실시간으로 편하게 다운로드 하시면 됩니다. (클래스 구독이 끝나더라도..)
https://drive.google.com/drive/folders/1mKGGR355vmBCxB7A3sOOSh8-gQs1CiMF?usp=drive_link




클래스 진행하면서 채워나가는 구성이지만
학습 편의를 위해 최종 버전의 코드를 제공합니다. 

변경될 일은 거의 없지만 만의 하나 변경이 이후 생긴다면 수정본은 
맨 마지막 Outro-2 강의 수업자료에 먼저 반영되니 그 코드를 최종본이라 생각하고 받으시면 됩니다.

공통 모듈 중 kis_common.py만 클래스 진행하시면 계속 내용이 추가 수정 되며 Outro-2에 최종본이라고 생각하시면 되는데
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
import time
import pandas as pd

from domain.env_type import EnvType


# 시장이 열렸는지 여부 체크! #토요일 일요일은 확실히 안열리니깐 제외!
def is_market_open():

    now_time = datetime.now(timezone("America/New_York"))
    pprint.pprint(now_time)
    strNow = now_time.strftime("%Y/%m/%d")

    date_week = now_time.weekday()

    IsOpen = False

    # 주말은 무조건 장이 안열리니 False 리턴!
    if date_week == 5 or date_week == 6:
        IsOpen = False
    else:
        # 현지시간 기준 9시 반부터 4시
        if now_time.hour >= 9 and now_time.hour <= 15:
            IsOpen = True

            if now_time.hour == 9 and now_time.minute < 30:
                IsOpen = False

            if now_time.hour == 15 and now_time.minute > 50:
                IsOpen = False

    # 평일 장 시간이어도 공휴일같은날 장이 안열린다. 그래서 1번 더 체크!!
    if IsOpen == True:

        print("Time is OK... but one more checked!!!")

        Is_CheckTody = False

        CheckDict = dict()

        # 파일 경로입니다.
        file_path = "/var/autobot/US_Market_OpenCheck.json"
        try:
            with open(file_path, "r") as json_file:
                CheckDict = json.load(json_file)

        except Exception as e:
            print("Exception by First")

        # 만약 키가 존재 하지 않는다 즉 아직 한번도 체크하지 않은 상황
        if CheckDict.get("CheckTody") == None:

            Is_CheckTody = True

        else:

            # 날짜가 바뀌었다면 체크 해야 한다!
            if CheckDict["CheckTody"] != strNow:
                Is_CheckTody = True

        result = ""
        order = ""

        # 체크할 필요가 있을 때만 체크한다!
        if Is_CheckTody == True:

            try:

                order = make_buy_limit_order("AAPL", 1, 1)
                result = cancel_modify_order(
                    "AAPL", str(int(order["OrderNum2"])), 1, 1, "CANCEL", "YES"
                )
                pprint.pprint(result)

            except Exception as e:

                print("EXCEPTION ", e)

        # 장운영시간이 아니라고 리턴되면 장이 닫힌거다!
        if (
            result == "APBK0918"
            or result == "APBK0919"
            or order == "APBK1664"
            or order == "40100000"
            or order == "APAM3099"
        ):

            print("Market is Close!!")
            return False

        else:

            if result == "EGW00123":
                print("Token is failed...So You need Action!!")

            # 마켓이 열린 시간내에 가짜주문이 유효하다면 장이 열렸으니 더이상 이 시간내에 또 체크할 필요가 없다.
            CheckDict["CheckTody"] = strNow
            with open(file_path, "w") as outfile:
                json.dump(CheckDict, outfile)

            print("Market is Open!!")
            return True
    else:

        print("Time is NO!!!")
        return False


# price_pricision 호가 단위에 맞게 변형해준다. 지정가 매매시 사용
def price_adjust(price):

    return round(float(price), 2)


# 환율 리턴!
def get_exrt():

    time.sleep(0.2)

    PATH = "/uapi/overseas-stock/v1/trading/inquire-present-balance"
    URL = f"{common.get_url_base()}/{PATH}"

    TrId = "CTRP6504R"
    if common.get_now_dist() == EnvType.V:
        TrId = "VTRP6504R"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": common.get_app_key(),
        "appSecret": common.get_app_secret(),
        "tr_id": TrId,
        "custtype": "P",
    }

    params = {
        "CANO": common.get_account_no(),
        "ACNT_PRDT_CD": common.get_account_prd_no(),
        "WCRC_FRCR_DVSN_CD": "02",
        "NATN_CD": "840",
        "TR_MKET_CD": "00",
        "INQR_DVSN_CD": "00",
    }

    # 호출
    res = requests.get(URL, headers=headers, params=params)
    # pprint.pprint(res.json())

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        result = res.json()["output2"]

        Rate = 1200

        for data in result:
            if data["crcy_cd"] == "USD":
                Rate = data["frst_bltn_exrt"]
                break

        return Rate

    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None


""" 23.5.13일 이후 사용하지 않게됨
#미국 주식 주간 / 야간 여부를 리턴 하는 함수!
def GetDayOrNight():

    time.sleep(0.2)
    
    PATH = "uapi/overseas-stock/v1/trading/dayornight"
    URL = f"{common.get_url_base()}/{PATH}"

    # 헤더 설정
    headers = {"Content-Type":"application/json", 
            "authorization": f"Bearer {common.get_token()}",
            "appKey":common.get_app_key(),
            "appSecret":common.get_app_secret(),
            "tr_id":"JTTT3010R"}

    params = {
    }

    # 호출
    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == '0':
        return res.json()['output']['PSBL_YN']
    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None
"""


# 미국 잔고! 달러로 리턴할건지 원화로 리턴할건지!
def get_balance(st="USD"):

    time.sleep(0.2)

    PATH = "uapi/overseas-stock/v1/trading/inquire-present-balance"
    URL = f"{common.get_url_base()}/{PATH}"

    TrId = "CTRP6504R"
    if common.get_now_dist() == EnvType.V:
        TrId = "VTRP6504R"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": common.get_app_key(),
        "appSecret": common.get_app_secret(),
        "tr_id": TrId,
        "custtype": "P",
    }

    params = {
        "CANO": common.get_account_no(),
        "ACNT_PRDT_CD": common.get_account_prd_no(),
        "WCRC_FRCR_DVSN_CD": "02",
        "NATN_CD": "840",
        "TR_MKET_CD": "00",
        "INQR_DVSN_CD": "00",
    }

    # 호출
    res = requests.get(URL, headers=headers, params=params)
    # pprint.pprint(res.json())

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        result = res.json()["output2"]

        # 실시간 주식 상태가 반영이 안되서 주식 정보를 직접 읽어서 계산!
        my_stock_list = get_my_stock_list(st)

        StockOriMoneyTotal = 0
        StockNowMoneyTotal = 0

        for stock in my_stock_list:
            # pprint.pprint(stock)
            StockOriMoneyTotal += float(stock["StockOriMoney"])
            StockNowMoneyTotal += float(stock["stock_now_money"])

            # print("--", StockNowMoneyTotal, StockOriMoneyTotal)

        balanceDict = dict()
        balanceDict["RemainMoney"] = 0

        Rate = 1200

        if st == "USD":

            for data in result:
                if data["crcy_cd"] == "USD":
                    # 예수금 총금액 (즉 주문가능 금액)
                    balanceDict["RemainMoney"] = (
                        float(data["frcr_dncl_amt_2"])
                        - float(data["frcr_buy_amt_smtl"])
                        + float(data["frcr_sll_amt_smtl"])
                    )  # 모의계좌는 0으로 나온다 이유는 모르겠음!
                    Rate = data["frst_bltn_exrt"]
                    break

            result = res.json()["output3"]

            # 임시로 모의 계좌 잔고가 0으로
            if (
                common.get_now_dist() == EnvType.V
                and float(balanceDict["RemainMoney"]) == 0
            ):

                # 주식 총 평가 금액
                balanceDict["StockMoney"] = (
                    StockNowMoneyTotal  # (float(result['evlu_amt_smtl_amt']) / float(Rate))
                )
                # 평가 손익 금액
                balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
                    StockOriMoneyTotal
                )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

                balanceDict["RemainMoney"] = float(result["frcr_evlu_tota"]) / float(
                    Rate
                )

                # 총 평가 금액
                balanceDict["total_money"] = float(balanceDict["StockMoney"]) + float(
                    balanceDict["RemainMoney"]
                )

            else:

                # 주식 총 평가 금액
                balanceDict["StockMoney"] = (
                    StockNowMoneyTotal  # (float(result['evlu_amt_smtl_amt']) / float(Rate))
                )
                # 평가 손익 금액
                balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
                    StockOriMoneyTotal
                )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

                # 총 평가 금액
                balanceDict["total_money"] = float(balanceDict["StockMoney"]) + float(
                    balanceDict["RemainMoney"]
                )

        else:

            for data in result:
                if data["crcy_cd"] == "USD":
                    Rate = data["frst_bltn_exrt"]
                    # 예수금 총금액 (즉 주문가능현금)
                    balanceDict["RemainMoney"] = (
                        float(data["frcr_dncl_amt_2"])
                        - float(data["frcr_buy_amt_smtl"])
                        + float(data["frcr_sll_amt_smtl"])
                    ) * float(Rate)
                    # balanceDict['RemainMoney'] = data['frcr_evlu_amt2'] #모의계좌는 0으로 나온다 이유는 모르겠음!

                    break

            # print("balanceDict['RemainMoney'] ", balanceDict['RemainMoney'] )

            result = res.json()["output3"]

            # 임시로 모의 계좌 잔고가 0으로 나오면
            if (
                common.get_now_dist() == EnvType.V
                and float(balanceDict["RemainMoney"]) == 0
            ):

                # 주식 총 평가 금액
                balanceDict["StockMoney"] = (
                    StockNowMoneyTotal  # result['evlu_amt_smtl_amt']
                )
                # 평가 손익 금액
                balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
                    StockOriMoneyTotal
                )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

                balanceDict["RemainMoney"] = float(result["frcr_evlu_tota"])

                # 총 평가 금액
                balanceDict["total_money"] = float(balanceDict["StockMoney"]) + float(
                    balanceDict["RemainMoney"]
                )

            else:

                # 주식 총 평가 금액
                balanceDict["StockMoney"] = (
                    StockNowMoneyTotal  # result['evlu_amt_smtl_amt']
                )
                # 평가 손익 금액
                balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
                    StockOriMoneyTotal
                )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

                # 총 평가 금액
                balanceDict["total_money"] = float(balanceDict["StockMoney"]) + float(
                    balanceDict["RemainMoney"]
                )

        return balanceDict

    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None


# 미국 보유 주식 리스트
def get_my_stock_list(st="USD"):

    PATH = "uapi/overseas-stock/v1/trading/inquire-balance"
    URL = f"{common.get_url_base()}/{PATH}"

    StockList = list()

    for i in range(1, 4):

        try_market = "NASD"

        if i == 2:
            try_market = "NYSE"
        elif i == 3:
            try_market = "AMEX"
        else:
            try_market = "NASD"

        TrId = "TTTS3012R"
        if common.get_now_dist() == EnvType.V:
            TrId = "VTTS3012R"

        """
        if GetDayOrNight() == 'N':
            TrId = "TTTS3012R"
            if common.get_now_dist() == EnvType.V:
                TrId = "VTTS3012R"
        """

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
                "appKey": common.get_app_key(),
                "appSecret": common.get_app_secret(),
                "tr_id": TrId,
                "tr_cont": tr_cont,
                "custtype": "P",
            }

            params = {
                "CANO": common.get_account_no(),
                "ACNT_PRDT_CD": common.get_account_prd_no(),
                "OVRS_EXCG_CD": try_market,
                "TR_CRCY_CD": "USD",
                "CTX_AREA_FK200": FKKey,
                "CTX_AREA_NK200": NKKey,
            }

            # 호출
            res = requests.get(URL, headers=headers, params=params)

            if res.headers["tr_cont"] == "M" or res.headers["tr_cont"] == "F":
                tr_cont = "N"
            else:
                tr_cont = ""

            if res.status_code == 200 and res.json()["rt_cd"] == "0":

                NKKey = res.json()["ctx_area_nk200"].strip()
                if NKKey != "":
                    print("---> CTX_AREA_NK200: ", NKKey)

                FKKey = res.json()["ctx_area_fk200"].strip()
                if FKKey != "":
                    print("---> CTX_AREA_FK200: ", FKKey)

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
                    if int(stock["ovrs_cblc_qty"]) > 0:

                        StockInfo = dict()

                        StockInfo["stock_code"] = stock["ovrs_pdno"]
                        StockInfo["stock_name"] = stock["ovrs_item_name"]
                        StockInfo["stock_amt"] = stock["ovrs_cblc_qty"]

                        if st == "USD":

                            StockInfo["stock_avg_price"] = stock["pchs_avg_pric"]
                            StockInfo["StockOriMoney"] = stock["frcr_pchs_amt1"]
                            StockInfo["stock_now_money"] = stock["ovrs_stck_evlu_amt"]
                            StockInfo["StockNowPrice"] = stock["now_pric2"]
                            StockInfo["stock_revenue_money"] = stock[
                                "frcr_evlu_pfls_amt"
                            ]

                        else:

                            time.sleep(0.2)
                            Rate = get_exrt()

                            StockInfo["stock_avg_price"] = float(
                                stock["pchs_avg_pric"]
                            ) * float(Rate)
                            StockInfo["StockOriMoney"] = float(
                                stock["frcr_pchs_amt1"]
                            ) * float(Rate)
                            StockInfo["stock_now_money"] = float(
                                stock["ovrs_stck_evlu_amt"]
                            ) * float(Rate)
                            StockInfo["StockNowPrice"] = float(
                                stock["now_pric2"]
                            ) * float(Rate)
                            StockInfo["stock_revenue_money"] = float(
                                stock["frcr_evlu_pfls_amt"]
                            ) * float(Rate)

                        StockInfo["stock_revenue_rate"] = stock["evlu_pfls_rt"]

                        Is_Duple = False
                        for exist_stock in StockList:
                            if exist_stock["stock_code"] == StockInfo["stock_code"]:
                                Is_Duple = True
                                break

                        if Is_Duple == False:
                            StockList.append(StockInfo)

            else:
                print("Error Code : " + str(res.status_code) + " | " + res.text)
                if res.json()["msg_cd"] == "EGW00123":
                    DataLoad = False

                count += 1

                if count > 100:
                    DataLoad = False

    return StockList


############################################################################################################################################################


# 미국 주식현재가 시세
def get_current_price_ori(market, stock_code):

    time.sleep(0.2)

    PATH = "uapi/overseas-price/v1/quotations/price"
    URL = f"{common.get_url_base()}/{PATH}"

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": common.get_app_key(),
        "appSecret": common.get_app_secret(),
        "tr_id": "HHDFS00000300",
    }

    params = {
        "AUTH": "",
        "EXCD": market.upper(),
        "SYMB": stock_code,
    }

    # 호출
    res = requests.get(URL, headers=headers, params=params)
    # pprint.pprint(res.json())

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        return float(res.json()["output"]["last"])
    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None


# 미국의 나스닥,뉴욕거래소, 아멕스를 뒤져서 있는 증권의 현재가를 가지고 옵니다!
def get_current_price(stock_code):

    time.sleep(0.2)

    PATH = "uapi/overseas-price/v1/quotations/price"
    URL = f"{common.get_url_base()}/{PATH}"

    for i in range(1, 4):

        try_market = "NAS"

        if i == 2:
            try_market = "NYS"
        elif i == 3:
            try_market = "AMS"
        else:
            try_market = "NAS"

        # 헤더 설정
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {common.get_token()}",
            "appKey": common.get_app_key(),
            "appSecret": common.get_app_secret(),
            "tr_id": "HHDFS00000300",
        }

        params = {
            "AUTH": "",
            "EXCD": try_market,
            "SYMB": stock_code,
        }

        # 호출
        res = requests.get(URL, headers=headers, params=params)

        if res.status_code == 200 and res.json()["rt_cd"] == "0":

            if res.json()["output"]["last"] == "":
                # print(try_market, " is Failed.. Next market.. ")
                time.sleep(0.2)
                continue  # 다음 시도를 한다!
            else:
                # print(try_market, " is Succeed!! ")
                return float(res.json()["output"]["last"])

        else:
            print("Error Code : " + str(res.status_code) + " | " + res.text)
            break

    return None


############################################################################################################################################################


# 미국 지정가 주문하기!
def make_buy_limit_order_ori(stockcode, amt, price, market, adjustAmt=False):

    # 매수가능 수량으로 보정할지 여부
    if adjustAmt == True:
        try:
            # 가상 계좌는 미지원
            if common.get_now_dist() != EnvType.V:
                # 매수 가능한수량으로 보정
                amt = adjust_possible_amt(stockcode, amt)

        except Exception as e:
            print("Exception")

    time.sleep(0.2)

    TrId = "JTTT1002U"
    if common.get_now_dist() == EnvType.V:
        TrId = "VTTT1002U"

    PATH = "uapi/overseas-stock/v1/trading/order"
    URL = f"{common.get_url_base()}/{PATH}"
    data = {
        "CANO": common.get_account_no(),
        "ACNT_PRDT_CD": common.get_account_prd_no(),
        "OVRS_EXCG_CD": market.upper(),
        "PDNO": stockcode,
        "ORD_DVSN": "00",
        "ORD_QTY": str(int(amt)),
        "OVRS_ORD_UNPR": str(price_adjust(price)),
        "ORD_SVR_DVSN_CD": "0",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": common.get_app_key(),
        "appSecret": common.get_app_secret(),
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

    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None


# 미국 지정가 주문하기!
def make_sell_limit_order_ori(stockcode, amt, price, market):

    time.sleep(0.2)

    TrId = "JTTT1006U"
    if common.get_now_dist() == EnvType.V:
        TrId = "VTTT1001U"

    PATH = "uapi/overseas-stock/v1/trading/order"
    URL = f"{common.get_url_base()}/{PATH}"
    data = {
        "CANO": common.get_account_no(),
        "ACNT_PRDT_CD": common.get_account_prd_no(),
        "OVRS_EXCG_CD": market.upper(),
        "PDNO": stockcode,
        "ORD_DVSN": "00",
        "ORD_QTY": str(int(amt)),
        "OVRS_ORD_UNPR": str(price_adjust(price)),
        "ORD_SVR_DVSN_CD": "0",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": common.get_app_key(),
        "appSecret": common.get_app_secret(),
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

    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None


# 미국 지정가 주문하기! 마켓을 모를 경우 자동으로 뒤져서!
def make_buy_limit_order(stockcode, amt, price, adjustAmt=False):

    if adjustAmt == True:
        try:
            # 가상 계좌는 미지원
            if common.get_now_dist() != EnvType.V:
                # 매수 가능한수량으로 보정
                amt = adjust_possible_amt(stockcode, amt)

        except Exception as e:
            print("Exception")

    time.sleep(0.2)

    TrId = "JTTT1002U"
    if common.get_now_dist() == EnvType.V:
        TrId = "VTTT1002U"

    market = get_market_code_us(stockcode)

    PATH = "uapi/overseas-stock/v1/trading/order"
    URL = f"{common.get_url_base()}/{PATH}"
    data = {
        "CANO": common.get_account_no(),
        "ACNT_PRDT_CD": common.get_account_prd_no(),
        "OVRS_EXCG_CD": market,
        "PDNO": stockcode,
        "ORD_DVSN": "00",
        "ORD_QTY": str(int(amt)),
        "OVRS_ORD_UNPR": str(price_adjust(price)),
        "ORD_SVR_DVSN_CD": "0",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": common.get_app_key(),
        "appSecret": common.get_app_secret(),
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

    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return res.json()["msg_cd"]


# 미국 지정가 주문하기! 마켓을 모를 경우 자동으로 뒤져서!
def make_sell_limit_order(stockcode, amt, price):

    time.sleep(0.2)

    TrId = "JTTT1006U"
    if common.get_now_dist() == EnvType.V:
        TrId = "VTTT1001U"

    market = get_market_code_us(stockcode)

    PATH = "uapi/overseas-stock/v1/trading/order"
    URL = f"{common.get_url_base()}/{PATH}"
    data = {
        "CANO": common.get_account_no(),
        "ACNT_PRDT_CD": common.get_account_prd_no(),
        "OVRS_EXCG_CD": market,
        "PDNO": stockcode,
        "ORD_DVSN": "00",
        "ORD_QTY": str(int(amt)),
        "OVRS_ORD_UNPR": str(price_adjust(price)),
        "ORD_SVR_DVSN_CD": "0",
    }
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": common.get_app_key(),
        "appSecret": common.get_app_secret(),
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
    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None


# 미국의 나스닥,뉴욕거래소, 아멕스를 뒤져서 있는 해당 주식의 거래소 코드를 리턴합니다!!
def get_market_code_us(stock_code, return_ori_market=False):
    time.sleep(0.2)

    PATH = "uapi/overseas-price/v1/quotations/price"
    URL = f"{common.get_url_base()}/{PATH}"

    for i in range(1, 4):

        try_market = "NAS"

        if i == 2:
            try_market = "NYS"
        elif i == 3:
            try_market = "AMS"
        else:
            try_market = "NAS"

        # 헤더 설정
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {common.get_token()}",
            "appKey": common.get_app_key(),
            "appSecret": common.get_app_secret(),
            "tr_id": "HHDFS00000300",
        }

        params = {
            "AUTH": "",
            "EXCD": try_market,
            "SYMB": stock_code,
        }

        # 호출
        res = requests.get(URL, headers=headers, params=params)

        if res.status_code == 200 and res.json()["rt_cd"] == "0":

            if res.json()["output"]["last"] == "":
                # print(try_market, " is Failed.. Next market.. ")
                time.sleep(0.2)
                continue  # 다음 시도를 한다!
            else:
                # print(try_market, " is Succeed!! ")

                if return_ori_market == True:

                    return try_market

                else:

                    if try_market == "NYS":
                        return "NYSE"
                    elif try_market == "AMS":
                        return "AMEX"
                    else:
                        return "NASD"

        else:
            print("Error Code : " + str(res.status_code) + " | " + res.text)
            break

    return None


# 보유한 주식을 모두 매도하는 극단적 함수
def sell_all_stock():
    StockList = get_my_stock_list()

    # 시장가로 모두 매도 한다
    for stock_info in StockList:
        pprint.pprint(
            make_sell_limit_order(
                stock_info["stock_code"],
                stock_info["stock_amt"],
                stock_info["stock_avg_price"],
            )
        )


# 매수 가능한지 체크 하기!
def check_possible_buy_info(stockcode, price):

    time.sleep(0.2)

    PATH = "uapi/overseas-stock/v1/trading/inquire-psamount"
    URL = f"{common.get_url_base()}/{PATH}"

    TrId = "TTTS3007R"
    """
    if GetDayOrNight() == 'N':
        TrId = "TTTS3007R"
    """

    market = get_market_code_us(stockcode)

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": common.get_app_key(),
        "appSecret": common.get_app_secret(),
        "tr_id": TrId,
        "custtype": "P",
    }

    params = {
        "CANO": common.get_account_no(),
        "ACNT_PRDT_CD": common.get_account_prd_no(),
        "OVRS_EXCG_CD": market,
        "OVRS_ORD_UNPR": str(price_adjust(price)),
        "ITEM_CD": stockcode,
    }

    # 호출
    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        result = res.json()["output"]
        # pprint.pprint(result)

        CheckDict = dict()

        CheckDict["RemainMoney"] = result["ord_psbl_frcr_amt"]
        CheckDict["MaxAmt"] = result["max_ord_psbl_qty"]

        return CheckDict

    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return res.json()["msg_cd"]


# 매수 가능한수량으로 보정
def adjust_possible_amt(stockcode, amt):
    NowPrice = get_current_price(stockcode)

    data = check_possible_buy_info(stockcode, NowPrice)

    if str(data) == "MCA00124" or str(data) == "OPSQ0002":
        return int(amt)
    else:

        MaxAmt = int(data["MaxAmt"])

        if MaxAmt <= int(amt):
            print("!!!!!!!!!!!!MaxAmt Over!!!!!!!!!!!!!!!!!!")
            return MaxAmt
        else:
            print("!!!!!!!!!!!!Amt OK!!!!!!!!!!!!!!!!!!")
            return int(amt)


############################################################################################################################################################


# 주문 리스트를 얻어온다! 종목 코드, side는 ALL or BUY or SELL, 상태는 OPEN or CLOSE
def get_order_list(stockcode="", side="ALL", status="ALL", limit=5):

    time.sleep(0.2)

    TrId = "TTTS3035R"
    if common.get_now_dist() == EnvType.V:
        TrId = "VTTS3035R"  # VTTT3001R #야간은 미지원...으앙! 어쩌라공~~

    """
    if GetDayOrNight() == 'N':
        TrId = "TTTS3035R"
        if common.get_now_dist() == EnvType.V:
            TrId = "VTTS3035R"
    """

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

    PATH = "uapi/overseas-stock/v1/trading/inquire-ccnl"
    URL = f"{common.get_url_base()}/{PATH}"

    print("stockcode - >", stockcode)

    params = {
        "CANO": common.get_account_no(),
        "ACNT_PRDT_CD": common.get_account_prd_no(),
        "PDNO": stockcode,
        "ORD_STRT_DT": common.get_from_now_date_str("US", "NONE", -limit),
        "ORD_END_DT": common.get_now_date_str("US"),
        "SLL_BUY_DVSN": sell_buy_code,
        "CCLD_NCCS_DVSN": status_code,
        "OVRS_EXCG_CD": "",
        "SORT_SQN": "",
        "ORD_DT": "",
        "ORD_GNO_BRNO": "",
        "ODNO": "",
        "CTX_AREA_FK200": "",
        "CTX_AREA_NK200": "",
    }

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": common.get_app_key(),
        "appSecret": common.get_app_secret(),
        "tr_id": TrId,
        "custtype": "P",
        "hashkey": common.get_hash_key(params),
    }

    res = requests.get(URL, headers=headers, params=params)
    # pprint.pprint(res.json())

    if res.status_code == 200 and res.json()["rt_cd"] == "0":

        ResultList = res.json()["output"]

        OrderList = list()

        for order in ResultList:
            # 잔고 수량이 0 이상인것만

            OrderInfo = dict()

            OrderInfo["OrderStock"] = order["pdno"]
            OrderInfo["OrderStockName"] = order["prdt_name"]

            # 주문 구분
            OrderInfo["OrderType"] = "Limit"

            # 주문 사이드
            if order["sll_buy_dvsn_cd"] == "01":
                OrderInfo["OrderSide"] = "Sell"
            else:
                OrderInfo["OrderSide"] = "Buy"

            if (float(order["ft_ord_qty"]) - float(order["ft_ccld_qty"])) == 0 or order[
                "prcs_stat_name"
            ] == "완료":
                OrderInfo["OrderSatus"] = "Close"
            else:
                OrderInfo["OrderSatus"] = "Open"

            """
            #주문정보 날짜가 다르다.
            if common.get_now_date_str("KR") != order['ord_dt']: 
                #그런데 전날이다!
                if common.get_from_now_date_str("KR","NONE",-1) == order['ord_dt']:
                    if int(order['ord_tmd']) < 203000: #10시30분00초 보다 작다
                        OrderInfo["OrderSatus"] = "Close"     
                else:
                    OrderInfo["OrderSatus"] = "Close"   #전날도 아니면 무조건 취소가 되었을 터!
            """

            # 주문 수량~
            OrderInfo["OrderAmt"] = int(float(order["ft_ord_qty"]))

            # 주문 최종 수량~
            OrderInfo["OrderResultAmt"] = int(float(order["ft_ccld_qty"]))

            # 주문넘버..
            OrderInfo["OrderNum"] = order["ord_gno_brno"]
            OrderInfo["OrderNum2"] = order["odno"]

            # 아직 미체결 주문이라면 주문 단가를
            if OrderInfo["OrderSatus"] == "Open":

                OrderInfo["OrderAvgPrice"] = order["ft_ord_unpr3"]

            # 체결된 주문이면 평균체결금액을!
            else:
                if order["ft_ccld_qty"] == "0":
                    OrderInfo["OrderAvgPrice"] = order["ft_ord_unpr3"]
                else:
                    OrderInfo["OrderAvgPrice"] = order["ft_ccld_unpr3"]

            if order["rvse_cncl_dvsn"] == "02":

                OrderInfo["OrderIsCancel"] = "Y"
            else:

                OrderInfo["OrderIsCancel"] = "N"
            OrderInfo["OrderMarket"] = order[
                "ovrs_excg_cd"
            ]  # 마켓인데 미국과 통일성을 위해!

            OrderInfo["OrderDate"] = order["ord_dt"]
            OrderInfo["OrderTime"] = order["ord_tmd"]

            Is_Ok = False

            if status == "ALL":
                Is_Ok = True
            else:
                if status == OrderInfo["OrderSatus"].upper():
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

    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None


# 주문 취소하거나 종료하기
def cancel_modify_order(
    stockcode, order_num, order_amt, order_price, mode="CANCEL", Errlog="YES"
):

    time.sleep(0.2)

    TrId = "JTTT1004U"
    if common.get_now_dist() == EnvType.V:
        TrId = "VTTT1004U"

    mode_type = "02"
    if mode.upper() == "MODIFY":
        mode_type = "01"

    market = get_market_code_us(stockcode)

    PATH = "uapi/overseas-stock/v1/trading/order-rvsecncl"
    URL = f"{common.get_url_base()}/{PATH}"
    data = {
        "CANO": common.get_account_no(),
        "ACNT_PRDT_CD": common.get_account_prd_no(),
        "OVRS_EXCG_CD": market.upper(),
        "PDNO": stockcode,
        "ORGN_ODNO": str(order_num),
        "RVSE_CNCL_DVSN_CD": mode_type,
        "ORD_QTY": str(order_amt),
        "OVRS_ORD_UNPR": str(price_adjust(order_price)),
    }

    # pprint.pprint(data)

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": common.get_app_key(),
        "appSecret": common.get_app_secret(),
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
    else:
        if Errlog == "YES":
            print("Error Code : " + str(res.status_code) + " | " + res.text)
        return res.json()["msg_cd"]


def cancel_all_orders(stockcode="", side="ALL"):

    OrderList = get_order_list(stockcode, side, "OPEN")

    for order in OrderList:
        if order["OrderSatus"].upper() == "OPEN":
            pprint.pprint(
                cancel_modify_order(
                    order["OrderStock"],
                    str(int(order["OrderNum2"])),
                    int(order["OrderAmt"]),
                    order["OrderAvgPrice"],
                )
            )


############################################################################################################################################################


# p_code -> D:일, W:주, M:월
def get_ohlcv(stock_code, p_code, adj_ok="1"):

    time.sleep(0.2)

    PATH = "/uapi/overseas-price/v1/quotations/dailyprice"
    URL = f"{common.get_url_base()}/{PATH}"

    gubun = 0
    if p_code == "W":
        gubun = 1
    elif p_code == "M":
        gubun = 2

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {common.get_token()}",
        "appKey": common.get_app_key(),
        "appSecret": common.get_app_secret(),
        "tr_id": "HHDFS76240000",
    }

    date_str = common.get_now_date_str("US")

    params = {
        "AUTH": "",
        "EXCD": get_market_code_us(stock_code, True),
        "SYMB": stock_code,
        "GUBN": str(gubun),
        "BYMD": date_str,
        "MODP": adj_ok,
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
                    if ohlcv["open"] != "":

                        OhlcvData["Date"] = ohlcv["xymd"]
                        OhlcvData["open"] = float(ohlcv["open"])
                        OhlcvData["high"] = float(ohlcv["high"])
                        OhlcvData["low"] = float(ohlcv["low"])
                        OhlcvData["close"] = float(ohlcv["clos"])
                        OhlcvData["volume"] = float(ohlcv["tvol"])
                        OhlcvData["value"] = float(ohlcv["tamt"])

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

    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None


# 일봉 정보 여러개 가져오는 개선된 함수!
def get_ohlcv_new(stock_code, p_code, get_count, adj_ok="1"):
    PATH = "/uapi/overseas-price/v1/quotations/dailyprice"
    URL = f"{common.get_url_base()}/{PATH}"

    gubun = 0
    if p_code == "W":
        gubun = 1
    elif p_code == "M":
        gubun = 2

    OhlcvList = list()

    DataLoad = True

    tr_cont = ""

    count = 0
    request_count = 0

    date_str = common.get_now_date_str("US")

    while DataLoad:
        time.sleep(0.2)

        print("...Data.Length..", len(OhlcvList), "-->", get_count)
        if len(OhlcvList) >= get_count:
            DataLoad = False

        # 헤더 설정
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {common.get_token()}",
            "appKey": common.get_app_key(),
            "appSecret": common.get_app_secret(),
            "tr_id": "HHDFS76240000",
            "tr_cont": tr_cont,
        }
        print("...Get..Data...", tr_cont)

        # if request_count > 0:
        #    date_str = common.get_from_now_date_str("US","NONE",-150*request_count)

        params = {
            "AUTH": "",
            "EXCD": get_market_code_us(stock_code, True),
            "SYMB": stock_code,
            "GUBN": str(gubun),
            "BYMD": date_str,
            "MODP": adj_ok,
        }

        # 호출
        res = requests.get(URL, headers=headers, params=params)

        if res.headers["tr_cont"] == "M" or res.headers["tr_cont"] == "F":
            tr_cont = "N"
        else:
            tr_cont = ""

        if tr_cont == "":
            DataLoad = False

        if res.status_code == 200 and res.json()["rt_cd"] == "0":

            request_count += 1

            ResultList = res.json()["output2"]

            df = list()

            add_cnt = 0

            if len(pd.DataFrame(ResultList)) > 0:

                for ohlcv in ResultList:

                    if len(ohlcv) == 0:
                        continue

                    OhlcvData = dict()

                    if ohlcv["open"] != "":

                        OhlcvData["Date"] = ohlcv["xymd"]
                        OhlcvData["open"] = float(ohlcv["open"])
                        OhlcvData["high"] = float(ohlcv["high"])
                        OhlcvData["low"] = float(ohlcv["low"])
                        OhlcvData["close"] = float(ohlcv["clos"])
                        OhlcvData["volume"] = float(ohlcv["tvol"])
                        OhlcvData["value"] = float(ohlcv["tamt"])

                        Is_Duple = False

                        for exist_stock in OhlcvList:
                            if exist_stock["Date"] == OhlcvData["Date"]:
                                Is_Duple = True
                                break

                        if Is_Duple == False:
                            if len(OhlcvList) < get_count:
                                OhlcvList.append(OhlcvData)
                                add_cnt += 1

                                date_str = OhlcvData["Date"]

            if add_cnt == 0:
                DataLoad = False

        else:
            print("Error Code : " + str(res.status_code) + " | " + res.text)

            if res.json()["msg_cd"] == "EGW00123":
                DataLoad = False

            count += 1
            if count > 10:
                DataLoad = False

    if len(OhlcvList) > 0:

        # for exist_stock in OhlcvList:
        #    pprint.pprint(exist_stock['Date'])

        print("len(OhlcvList):", len(OhlcvList))

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
    else:
        return None
