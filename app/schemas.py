from dataclasses import dataclass, field, InitVar
from typing import List, Optional
from datetime import datetime
from bson.objectid import ObjectId

from .enums import Country, Currency
from .app import BaseSchema

class IndicatorData(BaseSchema):
    date: datetime
    period: str
    actual: Optional[float] = None
    forecast: Optional[float] = None

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

@dataclass
class Indicator(BaseSchema):
    title: str
    country: Country
    currency: Currency
    indicator: str
    source: str
    importance: int
    id: str = ""
    _id: InitVar[ObjectId] = None
    ticker: Optional[str] = None
    comment: Optional[str] = None
    previous: Optional[float] = None
    unit: Optional[str] = None
    scale: Optional[str] = None
    data: List[IndicatorData] = field(default_factory=list)

    def __post_init__(self, _id: ObjectId):
        if _id:
            self.id = str(_id)
