from .app import APIRouter
from .api import Event


router = APIRouter()


@router.get(url="/events")
async def events():
    event = Event()
    data = await event.fetch()
    return data
