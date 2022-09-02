import pytest
from app import api, enums


@pytest.mark.asyncio
async def test_getting_list_of_events():
    result = await api.fetch_events()
    assert len(result) > 0


@pytest.mark.asyncio
async def test_event_filter():
    us_only_data = await api.fetch_events(countries=[enums.Country.US])
    assert len(set([e.country for e in us_only_data])) == 1
