import pytest
from app import api, enum

@pytest.mark.asyncio
async def test_getting_list_of_events():
    result = await api.get_events()
    assert len(result)

@pytest.mark.asyncio
async def test_event_filter():
    us_only_data = await api.get_events(countries=[enum.Country.US])
    assert len(set([ e.country for e in us_only_data ])) == 1
