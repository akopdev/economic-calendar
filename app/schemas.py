from dataclasses import dataclass, field, fields, InitVar
from typing import List, Optional
from datetime import datetime
from bson.objectid import ObjectId

from .enums import Country, Currency, Importance

@dataclass
class Event:
    id: int
    title: str
    country: Country
    currency: Currency
    indicator: str
    period: str
    source: str
    importance: Importance
    date: datetime
    ticker: Optional[str] = None
    comment: Optional[str] = None
    actual: Optional[float] = None
    previous: Optional[float] = None
    forecast: Optional[float] = None
    unit: Optional[str] = None
    scale: Optional[str] = None
