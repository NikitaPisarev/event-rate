from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

from app.config import get_settings

settings = get_settings()

MONGO_DETAILS = (
    f"mongodb://{settings.database.MONGO_USER}:"
    f"{settings.database.MONGO_PASSWORD}@"
    f"{settings.database.MONGO_HOST}:"
    f"{settings.database.MONGO_PORT}/"
    f"{settings.database.MONGO_DB}?authSource=admin"
)

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client[settings.database.MONGO_DB]

event_collection = database.get_collection("events")


async def create_indexes():
    await event_collection.create_index([("event_id", ASCENDING)], unique=True)
