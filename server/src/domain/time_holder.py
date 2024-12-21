from datetime import datetime
from src.domain.port import TimeHolder


class TimeHolderImpl(TimeHolder):
    def get_now(self) -> datetime:
        return datetime.now()
