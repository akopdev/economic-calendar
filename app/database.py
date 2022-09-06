from motor.motor_asyncio import AsyncIOMotorClient
from .settings import settings

db = AsyncIOMotorClient(settings.DATABASE_DSL)[settings.DATABASE_NAME]
