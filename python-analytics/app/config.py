import os

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://admin:admin123@mongo:27017"
)

DB_NAME = "yetinel"
