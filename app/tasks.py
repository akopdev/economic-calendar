import asyncio

from app.api import Indicator

from .app import BackgroundTasks


task = BackgroundTasks()


@task.add
async def sync_events(app):
    indicator = Indicator(app['db'])
    while True:
        await indicator.fetch()
        await asyncio.sleep(300)
