from .app import Application
from .routers import router
from .tasks import task

app = Application()
app.include_router(router)
app.include_task(task)

if __name__ == "__main__":
    app.run()
