import asyncio
from datetime import datetime, timedelta

from aiohttp.web import (
    HTTPNotFound
)
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from .api import Indicator
from .gds.gds import GrafanaDatasource
from .settings import settings
from .settings import settings

client = AsyncIOMotorClient(settings.DATABASE_DSL)

app = GrafanaDatasource(client=client, db=client[settings.DATABASE_NAME])


@app.metric()
async def upcoming_events(db: AsyncIOMotorClient, start: datetime, end: datetime):
    """
    Provide a list of upcoming events
    """
    indicators = db.indicators.find({
        "next.date": {
            "$gt": start,
            "$lt": end
        }
    }).sort("next.date", 1)
    events = []
    for i in await indicators.to_list(length=None):
        events.append({
           "code": i["code"],
           "title": i["title"],
           "country": i["country"],
           "currency": i["currency"],
           "indicator": i["indicator"],
           "date": i["next"]["date"].isoformat(),
           "forecast": i["next"]["forecast"],
        })
    return events


@app.metric()
async def actual(db: AsyncIOMotorClient, code: str):
    """
    Get actual indicator value for single event
    """
    event  = await db.indicators.find_one({"code": code})
    if event:
        return [(d["actual"], d["date"].isoformat(),) for d in event.get("data", [])]


@app.metric()
async def forecast(db: AsyncIOMotorClient, code: str):
    """
    Get market forecast for single event
    """
    event  = await db.indicators.find_one({"code": code})
    if event:
        return [(d["forecast"], d["date"].isoformat(),) for d in event.get("data", [])]


# @app.task
# async def sync_events(app):
#     indicator = Indicator(app['db'])
#     while True:
#         await indicator.fetch()
#         await asyncio.sleep(3000)

@app.task
async def import_historical_data(app):
    return False
    indicator = Indicator(app['db'])
    start = datetime.utcnow() - timedelta(days=365*5)
    while start < datetime.utcnow():
        end = start + timedelta(days=30)
        print(f"Importing data for period {start} - {end}")
        await indicator.fetch(start=start, end=end)
        start = end
        await asyncio.sleep(10)

if __name__ == "__main__":
    app.run()

