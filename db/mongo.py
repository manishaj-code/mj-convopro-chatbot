from pymongo import MongoClient
from config.settings import get_settings

settings = get_settings

try:
    _client = MongoClient(settings.MONGO_DB_URL, tz_aware=True, serverSelectionTimeoutMS=5000)
    _db = _client[settings.MONGO_DB_NAME]
    # Test connection
    _db.command('ping')
except Exception as e:
    print(f"⚠️ MongoDB connection warning: {e}")
    _client = None
    _db = None

def get_collection(name: str):
    """Get MongoDB collection"""
    if _db is None:
        raise Exception("MongoDB not connected")
    return _db[name]