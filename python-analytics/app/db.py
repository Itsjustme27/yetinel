from pymongo import MongoClient
from .config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_logs_collection():
    return db["logs"]


def get_alerts_collection():
    return db["alerts"]
