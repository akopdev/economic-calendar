from typing import Any, Callable, List, Tuple
import asyncio


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



