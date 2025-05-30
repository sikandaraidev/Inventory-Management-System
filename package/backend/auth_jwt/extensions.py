import os

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

host = os.environ.get("REDIS_HOST")
port = os.environ.get("REDIS_PORT")

bcrypt = Bcrypt()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
redis_blocklist = Redis(host="localhost", port=6379, decode_responses=True)
