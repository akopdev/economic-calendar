from typing import Any, Callable, List, Tuple
from aiohttp import web
import json
import asyncio


class APIRouter:
    def __init__(self) -> None:
        self.routers = [
            web.get("/health", self._health)
        ]

    def get(self, _func=None, *, url: str) -> Callable:
        def decorator(func) -> None:
            async def custom_func(*args, **kwargs) -> web.Response:
                if func.__code__.co_argcount:
                    data = await func(*args, **kwargs)
                else:
                    data = await func()
                return self._response(data)
            self.routers.append(web.get(url, custom_func))
        return decorator

    def _response(self, data: Any) -> web.Response:
        return web.Response(
            content_type="application/json",
            text=json.dumps(data, default=lambda o: o.dict())
        )

    async def _health(self, *args) -> web.Response:
        return self._response("OK")


class BackgroundTasks:
    def __init__(self) -> None:
        self.tasks: List[Tuple[str, Callable]] = []

    def add(self, func) -> None:
        async def custom_func(*args, **kwargs) -> Any:
            if func.__code__.co_argcount:
                data = await func(*args, **kwargs)
            else:
                data = await func()
            return data
        self.tasks.append((func.__name__, custom_func,))

    async def __call__(self, app) -> Any:
        for task in self.tasks:
            app[task[0]] = asyncio.create_task(task[1](app))


class Application(web.Application):
    def include_router(self, router: APIRouter):
        self.add_routes(router.routers)

    def include_task(self, tasks: BackgroundTasks):
        self.on_startup.append(tasks)

    def run(self):
        web.run_app(self)
