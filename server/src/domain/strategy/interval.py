from dataclasses import dataclass
from typing import List

from src.domain.common.type import TimeUnit


@dataclass
class Interval:
    time_unit: TimeUnit
    value: List[int]

    def to_dict(self):
        return {
            "time_unit": self.time_unit.value,
            "value": self.value,
        }

    def is_month(self):
        return self.time_unit == TimeUnit.MONTH
