import json
import requests
from domain.exception import InvestAppException
from infra.kis.dto import BalanceResponse, KisInfo


def make_token(info: KisInfo) -> str:
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": info.app_key,
        "appsecret": info.secret_key,
    }

    URL = f"{info.url_base}/oauth2/tokenP"
    res = requests.post(URL, headers=headers, data=json.dumps(body))

    if res.status_code == 200:
        return res.json()["access_token"]

    raise InvestAppException("토큰 생성 실패. {}", 400, res.text)


def get_balance(info: KisInfo) -> BalanceResponse:
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
        return BalanceResponse.of(res.json()["output2"][0])

    raise InvestAppException("잔고 조회 실패. {}", 500, res.text)
