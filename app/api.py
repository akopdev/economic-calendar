import aiohttp
from typing import List, Optional
from datetime import datetime, timedelta

from . import schemas, enums


async def fetch_events(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    countries: List[enums.Country] = []
) -> List[schemas.Event]:
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
                "countries": ",".join(countries or [c.value for c in enums.Country])
            }
        ) as resp:
            res = await resp.json()
            if res["status"] == "ok" and res["result"]:
                events = [schemas.Event(**e) for e in res["result"]]
    return events
