from abc import ABC, abstractmethod
from dataclasses import dataclass, field


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


@dataclass
class MyKisBalance(Balance):
    stock_money: float  # 주식 총 평가 금액
    stock_revenue: float  # 평가 손익 금액
    total_money: float  # 총 평가 금액
    remain_money: float = field(init=False)  # 총 예수금 (주문 가능 현금)

    def __post_init__(self):
        self.remain_money = self.total_money - self.stock_money

    @classmethod
    def of(res: dict) -> "Balance":
        return MyKisBalance(
            stock_money=float(res["scts_evlu_amt"]),
            stock_revenue=float(res["evlu_pfls_smtl_amt"]),
            total_money=float(res["tot_evlu_amt"]),
        )
