from enum import Enum, auto


class TriggerType(Enum):
    CRON = "cron"
    INTERVAL = "interval"
    DATE = "date"


class EnvType(Enum):
    REAL = "REAL"
    VIRTUAL = "VIRTUAL"


class Market(Enum):
    KR = auto()
    US = auto()


class TimeUnit(Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


class BrokerType(Enum):
    KIS_R = "KIS_R"  # 한국투자증권 실제
    KIS_V = "KIS_V"  # 한국투자증권 가상
    UPBIT_R = "UPBIT_R"  # 업비트 실제
    UPBIT_V = "UPBIT_V"  # 업비트 가상
