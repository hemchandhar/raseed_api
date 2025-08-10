from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_DETAILS)
database = client.raseed

user_collection = database.get_collection("users")
receipt_collection = database.get_collection("receipts")
