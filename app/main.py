from aiohttp import web
from .routers import router
from .tasks import task
from .database import db

@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
        message = ex.reason
    return web.json_response({'error': message})


app = web.Application(middlewares=[error_middleware])
app.router.add_routes(router)
app.on_startup.append(task)
app["db"] = db

if __name__ == "__main__":
    web.run_app(app)
