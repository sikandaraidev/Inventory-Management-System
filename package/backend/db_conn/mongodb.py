from mongoengine import connect

from package.backend.configuration.config import CATALOG_DB_URI

db = None


def init_mongo():
    global db
    db = connect(host=CATALOG_DB_URI, db="catalog", alias="default")


def get_db():
    if db is None:
        raise Exception("Database not initialized. Call init_db() first.")
    return db
