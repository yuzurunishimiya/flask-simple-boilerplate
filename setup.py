import os

class Config():
    ENV = "development"
    DEBUG = False
    TESTING = False
    SECRET_KEY = "5a4404f8-c239-4e6b-8a7d-aca5fd655a4b"

    MONGO_URI = "mongodb://127.0.0.1:27017/"
    MONGO_DBNAME = "development"
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    UPLOADS = "/src/upload/"


class ProductionConfig(Config):
    MONGO_URI = os.environ.get("MONGO_URI")

    # optional
    MONGO_DBNAME = os.environ.get("DB_NAME")
    REDIS_HOST = os.environ.get("REDIS_HOST", Config.REDIS_HOST)
    REDIS_PORT = os.environ.get("REDIS_PORT", Config.REDIS_PORT)

    UPLOADS = os.environ.get("UPLOADS_DIR")
    ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True
    pass


class TestingConfig(Config):
    pass
