import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
client = AsyncIOMotorClient(MONGODB_URI)
db = client.get_default_database()

uploads_collection = db.get_collection('uploads')
