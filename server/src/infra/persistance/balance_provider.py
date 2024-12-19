from abc import ABC, abstractmethod


class BalanceProvider(ABC):
    @abstractmethod
    def get_balance(self) -> dict:
        pass


class KISBalanceProvider(BalanceProvider):
    def get_balance(self) -> dict:
        # 한투 API를 사용하여 잔고 조회 구현
        pass


class UpbitBalanceProvider(BalanceProvider):
    def get_balance(self) -> dict:
        # 업비트 API를 사용하여 잔고 조회 구현
        pass
