from pymongo import MongoClient
from redis import Redis
from setup import DevelopmentConfig, ProductionConfig
import os

if os.environ.get("mode", "development") == "production":
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

db_client = MongoClient(config.MONGO_URI)
db_name = db_client[config.MONGO_DBNAME]
session = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
