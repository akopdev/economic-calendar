import asyncio
from . import api, enum

async def main():
    data = await api.fetch_events()
    print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
