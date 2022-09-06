import asyncio

from .app import BackgroundTasks


task = BackgroundTasks()


@task.add
async def sync_events(app):
    while True:
        await asyncio.sleep(300)
