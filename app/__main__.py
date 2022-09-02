import json
from . import api
from aiohttp import web
import asyncio


async def events(request):
    data = await api.fetch_events()
    return web.Response(
        content_type="application/json",
        text=json.dumps(data, default=lambda o: o.dict())
    )


async def sync_events(app):
    while True:
        print("Fetch new events")
        await asyncio.sleep(3)


async def start_background_tasks(app):
    app['sync_events'] = asyncio.create_task(sync_events(app))


async def cleanup_background_tasks(app):
    app['sync_events'].cancel()
    await app['sync_events']


app = web.Application()
app.add_routes([web.get('/events', events)])
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
web.run_app(app)
