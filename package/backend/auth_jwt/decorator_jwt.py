from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required

# from package.databases.Inventory.models_inv.user_model import User
# from package.db_conn.aws_mysql import get_session


def role_required(allowed_roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            role = get_jwt().get("role")
            if role not in allowed_roles:
                return jsonify(msg="Access forbidden: insufficient privileges"), 403
            return fn(*args, **kwargs)

        return decorated_function

    return wrapper
