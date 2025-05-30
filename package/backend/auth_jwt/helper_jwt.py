from sqlalchemy.orm import Session

from package.backend.auth_jwt.extensions import jwt, redis_blocklist
from package.backend.databases.Inventory.models_inv.user_model import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def is_token_revoked(decoded_token):
    jti = decoded_token["jti"]
    key = f"blocklist:{jti}"
    return redis_blocklist.get(key) is not None


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return redis_blocklist.get(f"blocklist:{jti}") is not None
