import aiohttp
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from . import schemas, enums


class Indicator:
    def __init__(self, db) -> None:
        self.db = db.indicators

    async def fetch(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        countries: List[enums.Country] = []
    ) -> List[Dict[str, Any]]:
        indicators = []
        if not start:
            start = datetime.utcnow() - timedelta(days=1)
        if not end:
            end = datetime.utcnow() + timedelta(days=90)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://economic-calendar.tradingview.com/events",
                params={
                    "from": start.isoformat() + "Z",
                    "to": end.isoformat() + "Z",
                    "countries": ",".join(countries or [c.value for c in enums.Country])
                }
            ) as resp:
                res = await resp.json()
                if res["status"] == "ok" and res["result"]:
                    for result in res["result"]:
                        if result["date"]:
                            result["date"] = datetime.fromisoformat(result["date"].replace("Z", "+00:00"))
                        indicator = await self.add(schemas.Event(**result))
                        if indicator:
                            indicators.append(indicator)
        return indicators

    async def add(self, event: schemas.Event) -> Optional[Dict[str, Any]]:
        # skip certain events as they won't ever have valuable metrics
        if event.indicator in ["Calendar", "Holidays"] or "Meeting" in event.title or "Speech" in event.title:
            return None

        # prepare database record
        payload = {
            "$set": {
                "title": event.title,
                "indicator": event.indicator,
                "country": event.country,
                "currency": event.currency,
                "source": event.source,
                "importance": event.importance,
                "unit": event.unit,
                "scale": event.scale,
                "updated_at": datetime.now()
            },
            "$addToSet": {
                "data": {
                    "date": event.date,
                    "actual": event.actual,
                    "forecast": event.forecast,
                }
            },
        }
        # If we don't have an actual data then just update schedule info
        if not event.actual:
            del payload["$addToSet"]
            payload["$set"]["next"] = {
                "date": event.date,
                "period": event.period,
                "forecast": event.forecast,
            }

        code = self.get_code(event)

        res = await self.db.update_one({ "code": code }, payload, upsert=True)

        if not res.modified_count:
            return None

        return await self.db.find_one({"code": code})

    def get_code(self, event: schemas.Event) -> str:
        code = "_".join([event.country, " ".join(event.title.split())])
        return code.replace(" ", "_").replace("-", "_").upper()
