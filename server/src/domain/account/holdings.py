from dataclasses import dataclass


@dataclass
class HoldingsInfo:
    name: str  # 종목명
    quantity: float  # 보유수량
    avg_price: float  # 평단가
    eval_amt: float  # 평가금액
