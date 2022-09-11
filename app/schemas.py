from dataclasses import dataclass, field, fields, InitVar
from typing import List, Optional
from datetime import datetime
from bson.objectid import ObjectId

from .enums import Country, Currency, Importance

@dataclass
class IndicatorData:
    date: datetime
    period: str
    actual: Optional[float] = None
    forecast: Optional[float] = None

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

@dataclass
class Indicator:
    title: str
    country: Country
    currency: Currency
    indicator: str
    source: str
    importance: Importance
    updated_at: datetime
    id: str = ""
    _id: InitVar[ObjectId] = None
    next: Optional[IndicatorData] = None
    ticker: Optional[str] = ""
    comment: Optional[str] = ""
    unit: Optional[str] = ""
    scale: Optional[str] = ""
    data: List[IndicatorData] = field(default_factory=list)

    def __post_init__(self, _id: ObjectId):
        if _id:
            self.id = str(_id)

