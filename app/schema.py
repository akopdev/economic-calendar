from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from .enum import Country, Currency

@dataclass
class Event:
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
