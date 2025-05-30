import os
from os import environ

# import pymysql
# import mysql.connector
from dotenv import load_dotenv

load_dotenv()


# For AWS SQL RDS DB connection
host = os.environ.get("HOST")
username = os.environ.get("USERNAME")
password = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
port = os.environ.get("DB_PORT")

INVENTORY_DB_URL = (
    f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{db_name}"
)


# For MongoDB connection
CATALOG_DB_URI = os.environ.get("DB_URI")


class Config:
    # App secret key
    SECRET_KEY = environ.get("SECRET_KEY", "dev-key")
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = True


config_by_name = {"dev": DevelopmentConfig, "prod": ProductionConfig}
