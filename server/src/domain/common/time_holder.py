from datetime import datetime
from src.domain.common.port import TimeHolder


class TimeHolderImpl(TimeHolder):
    def get_now(self) -> datetime:
        return datetime.now()
