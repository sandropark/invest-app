from abc import ABC, abstractmethod
from domain.helper import KIS_API_Helper_KR as KisKR
from domain.helper import KIS_API_Helper_US as KisUS
from domain.type import Market


class KisUtil(ABC):
    @abstractmethod
    def get_balnce(self):
        pass

    @abstractmethod
    def is_market_open(self):
        pass

    @abstractmethod
    def get_my_stock_list(self):
        pass

    @abstractmethod
    def get_current_price(self):
        pass

    @abstractmethod
    def make_sell_limit_order(self, stock_code: str, amt: int, price: int):
        pass

    @abstractmethod
    def make_buy_limit_order(self, stock_code: str, amt: int, price: int):
        pass

    @abstractmethod
    def get_stock_name(self, stock_code: str):
        pass

    @abstractmethod
    def make_sell_market_order(self, stock_code: str, amt: int):
        pass

    @abstractmethod
    def make_buy_market_order(self, stock_code: str, amt: int):
        pass


class KrKisUtil(KisUtil):
    def get_balance(self):
        return KisKR.GetBalance()

    def is_market_open(self):
        return KisKR.is_market_open()

    def get_my_stock_list(self):
        return KisKR.GetMyStockList()

    def get_current_price(self, stock_code: str):
        return KisKR.GetCurrentPrice(stock_code)

    def make_sell_limit_order(self, stock_code: str, amt: int, price: int):
        return KisKR.MakeSellLimitOrder(stock_code, amt, price)

    def make_buy_limit_order(self, stock_code: str, amt: int, price: int):
        return KisKR.MakeBuyLimitOrder(stock_code, amt, price)

    def get_stock_name(self, stock_code: str):
        return KisKR.GetStockName(stock_code)

    def make_sell_market_order(self, stock_code: str, amt: int):
        return KisKR.MakeSellMarketOrder(stock_code, amt)

    def make_buy_market_order(self, stock_code: str, amt: int):
        return KisKR.MakeBuyMarketOrder(stock_code, amt)


class UsKisUtil(KisUtil):
    def get_balance(self):
        return KisUS.GetBalance()

    def is_market_open(self):
        return KisUS.is_market_open()

    def get_my_stock_list(self):
        return KisUS.GetMyStockList()

    def get_current_price(self, stock_code: str):
        return KisUS.GetCurrentPrice(stock_code)

    def make_sell_limit_order(self, stock_code: str, amt: int, price: int):
        return KisUS.MakeSellLimitOrder(stock_code, amt, price)

    def make_buy_limit_order(self, stock_code: str, amt: int, price: int):
        return KisUS.MakeBuyLimitOrder(stock_code, amt, price)

    def get_stock_name(self, stock_code: str):
        pass

    def make_sell_market_order(self, stock_code: str, amt: int):
        pass

    def make_buy_market_order(self, stock_code: str, amt: int):
        pass


us_kis_util: KisUtil = UsKisUtil()
kr_kis_util: KisUtil = KrKisUtil()
kis_util: KisUtil = kr_kis_util


def set_market(market: Market):
    if market == None:
        return

    global kis_util
    kis_util = kr_kis_util if market == Market.KR else us_kis_util


def get_balance():
    return kis_util.get_balance()


def is_market_kr():
    return kis_util == kr_kis_util


def is_market_open():
    return kis_util.is_market_open()


def get_my_stock_list():
    return kis_util.get_my_stock_list()


def get_current_price(stock_code: str):
    return kis_util.get_current_price(stock_code)


def make_sell_limit_order(stock_code: str, amt: int, price: int):
    return kis_util.make_sell_limit_order(stock_code, amt, price)


def make_buy_limit_order(stock_code: str, amt: int, price: int):
    return kis_util.make_buy_limit_order(stock_code, amt, price)


def get_stock_name(stock_code: str):
    return kis_util.get_stock_name(stock_code)


def make_sell_market_order(stock_code: str, amt: int):
    return kis_util.make_sell_market_order(stock_code, amt)


def make_buy_market_order(stock_code: str, amt: int):
    return kis_util.make_buy_market_order(stock_code, amt)
