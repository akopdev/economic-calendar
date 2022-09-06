from .app import Application
from .routers import router
from .tasks import task
from .database import db

app = Application()
app.include_router(router)
app.include_task(task)
app["db"] = db

if __name__ == "__main__":
    app.run()
