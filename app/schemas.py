from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

from .enums import Country, Currency


class BaseSchema():
    def dict(self):
        return asdict(self)


@dataclass
class Event(BaseSchema):
    id: int
    title: str
    country: Country
    currency: Currency
    indicator: str
    period: str
    source: str
    importance: int
    date: datetime
    ticker: Optional[str] = None
    comment: Optional[str] = None
    actual: Optional[float] = None
    previous: Optional[float] = None
    forecast: Optional[float] = None
    unit: Optional[str] = None
    scale: Optional[str] = None
