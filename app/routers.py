from .app import APIRouter
from .api import Indicator


router = APIRouter()


@router.get(url="/history")
async def history(request):
    indicator = Indicator(request.app['db'])
    return await indicator.find()

