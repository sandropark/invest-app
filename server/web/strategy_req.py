from typing import Optional
from pydantic import BaseModel


class StrategyReq(BaseModel):
    name: str
    description: Optional[str] = None
