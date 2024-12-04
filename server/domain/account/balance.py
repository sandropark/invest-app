from abc import ABC, abstractmethod


class Balance(ABC):
    @abstractmethod
    def stock_money(self) -> float:
        pass

    @abstractmethod
    def stock_revenue(self) -> float:
        pass

    @abstractmethod
    def total_money(self) -> float:
        pass

    @abstractmethod
    def remain_money(self) -> float:
        pass

    @abstractmethod
    def of(res: dict) -> "Balance":
        pass


class MyKisBalance(Balance):
    def __init__(self, stock_money: float, stock_revenue: float, total_money: float):
        self.stock_money = stock_money  # 주식 총 평가 금액
        self.stock_revenue = stock_revenue  # 평가 손익 금액
        self.total_money = total_money  # 총 평가 금액
        self.remain_money = total_money - stock_money  # 총 예수금 (주문 가능 현금)

    def of(res: dict) -> Balance:
        return MyKisBalance(
            stock_money=float(res["scts_evlu_amt"]),
            stock_revenue=float(res["evlu_pfls_smtl_amt"]),
            total_money=float(res["tot_evlu_amt"]),
        )
