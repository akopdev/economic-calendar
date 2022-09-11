from aiohttp.web import RouteTableDef, HTTPBadRequest, HTTPNotFound, json_response
from datetime import datetime, timedelta
from bson import ObjectId


router = RouteTableDef()

@router.get("/health")
async def health(request):
    return json_response("OK")


@router.get("/events/upcoming")
async def get_upcoming_events(request):
    """
    Provide list of upcoming events
    """
    try:
        days = int(request.rel_url.query.get("days", 7))
    except ValueError:
        raise HTTPBadRequest(reason="Not valid amount of days")

    db = request.app['db']
    indicators = db.indicators.find({
        "next.date": {
            "$gt": datetime.utcnow(),
            "$lt": datetime.utcnow() + timedelta(days=days)
        }
    }).sort("next.date", 1)
    events = []
    for i in await indicators.to_list(length=None):
        events.append({
           "id": str(i["_id"]),
           "title": i["title"],
           "country": i["country"],
           "currency": i["currency"],
           "indicator": i["indicator"],
           "comment": i.get("comment"),
           "date": i["next"]["date"].isoformat(),
           "forecast": i["next"]["forecast"],
           "period": i["next"]["period"],
        })
    return json_response(events)


@router.get("/indicator/{id}")
async def get_indicators(request):
    """
    Get historical data for single event
    """
    id = request.match_info.get("id")
    if not id:
        raise HTTPBadRequest(reason="Event id is not provided")
    db = request.app['db']
    event  = await db.indicators.find_one({"_id": ObjectId(id)})
    if not event:
        raise HTTPNotFound(reason="Event not found")
    indicators = []
    for d in event.get("data", []):
        print(d)
        indicators.append({
            "date": d["date"].isoformat(),
            "period": d["period"],
            "actual": d["actual"],
            "forecast": d["forecast"]
        })
    return json_response(indicators)
