import asyncio
from .app import BackgroundTasks


task = BackgroundTasks()


@task.add
async def sync_events(app):
    while True:
        print("Fetch new events")
        await asyncio.sleep(3)
