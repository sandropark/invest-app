from dataclasses import dataclass


@dataclass
class KisInfo:
    token: str
    app_key: str
    secret_key: str
    url_base: str
    account_number: str
    product_code: str
    is_real: bool


class BalanceResponse:
    def __init__(self, res: dict):
        self.total_money = float(res["tot_evlu_amt"])
        self.stock_money = float(res["scts_evlu_amt"])
        self.stock_revenue = float(res["evlu_pfls_smtl_amt"])

        # 예수금이 아예 0이거나 총평가금액이랑 주식평가금액이 같은 상황일때는.. 좀 이상한 특이사항이다 풀매수하더라도 1원이라도 남을 테니깐
        # 퇴직연금 계좌에서 tot_evlu_amt가 제대로 반영이 안되는 경우가 있는데..이때는 전일 총평가금액을 가져오도록 한다!

        # dnca_tot_amt = 예수금총금액
        if float(res["dnca_tot_amt"]) == 0 or self.total_money == self.stock_money:
            self.total_money = float(
                res["bfdy_tot_asst_evlu_amt"]
            )  # 전일 총자산평가금액

        # 예수금 총금액 (즉 주문가능현금)
        self.remain_money = max(
            float(self.total_money) - float(self.stock_money),
            float(res["dnca_tot_amt"]),
        )

    @staticmethod
    def of(res: dict) -> "BalanceResponse":
        return BalanceResponse(res)
