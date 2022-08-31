import aiohttp
from typing import List, Optional
from datetime import datetime, timedelta

from . import schema, enum

async def fetch_events(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    countries: List[enum.Country] = []
) -> Optional[List[schema.Event]]:
    events = []
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
                "countries": ",".join(countries or [c.value for c in enum.Country])
            }
        ) as resp:
            res = await resp.json()
            if res["status"] == "ok" and res["result"]:
                events = [schema.Event(**e) for e in res["result"]]
    return events

