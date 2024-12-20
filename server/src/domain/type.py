from enum import Enum


class TriggerType(Enum):
    CRON = "cron"
    INTERVAL = "interval"
    DATE = "date"


class EnvType(Enum):
    REAL = "REAL"
    VIRTUAL = "VIRTUAL"


class Market(Enum):
    KR = "KR"
    US = "US"


class TimeUnit(Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


class BrokerType(Enum):
    KIS = "KIS"
    UPBIT = "UPBIT"

    def is_hantu(self):
        return self == BrokerType.KIS
