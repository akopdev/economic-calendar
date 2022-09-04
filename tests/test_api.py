import pytest
from app import api, enums


@pytest.mark.asyncio
async def test_getting_list_of_events():
    event = api.Event()
    result = await event.fetch()
    assert len(result) > 0


@pytest.mark.asyncio
async def test_event_filter():
    event = api.Event()
    us_only_data = await event.fetch(countries=[enums.Country.US])
    assert len(set([e.country for e in us_only_data])) == 1
