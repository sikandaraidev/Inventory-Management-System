from flask import Blueprint, jsonify, make_response, redirect, request, url_for
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
)
from pydantic import ValidationError

from package.backend.auth_jwt.extensions import bcrypt, limiter
from package.backend.auth_jwt.helper_jwt import get_user_by_email
from package.backend.databases.Inventory.models_inv.user_model import User
from package.backend.databases.Inventory.schema_inv.user_schema import UserCreate
from package.backend.db_conn.aws_mysql import get_session

jwtbp = Blueprint("jwt_route", __name__)


@jwtbp.route("/auth/signup", methods=["POST"])
def signup():
    db = next(get_session())
    data = request.get_json()

    if get_user_by_email(db, data["email"]):
        return jsonify(msg="User already exists"), 400

    # Hash password
    data["password_hash"] = bcrypt.generate_password_hash(
        data["password_hash"]
    ).decode()

    # Validate data using Pydantic
    try:
        validated_data = UserCreate(**data)
    except ValidationError as e:
        return jsonify(msg="Validation error", errors=e.errors()), 422

    # Create SQLAlchemy model instance
    new_user = User(**validated_data.model_dump())

    # Add and commit to DB
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        return jsonify(msg="Signup failed", error=str(e)), 500

    return jsonify(msg="User created successfully"), 201


@jwtbp.route("/auth/login", methods=["POST"])
@limiter.limit("5/minute")
def login():
    db = next(get_session())
    data = request.get_json()
    user = get_user_by_email(db, data["email"])
    if not user or not bcrypt.check_password_hash(
        user.password_hash, data["password_hash"]
    ):
        return jsonify(msg="Bad credentials"), 401

    # Access-Refresh tokens
    access_token = create_access_token(
        identity=str(user.user_id), additional_claims={"role": user.role}
    )
    refresh_token = create_refresh_token(identity=str(user.user_id))

    # Set both correctly
    response = jsonify({"msg": "Login successful"})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@jwtbp.route("/auth/me", methods=["GET"])
@jwt_required()
def get_current_user():
    identity = get_jwt_identity()
    claims = get_jwt()

    return jsonify({"user_id": identity, "role": claims.get("role")}), 200


@jwtbp.route("/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    resp = make_response(redirect(url_for("auth_bp.login")))
    # Clear JWT cookies (example using Flask-JWT-Extended)
    resp.delete_cookie("access_token_cookie")
    resp.delete_cookie("refresh_token_cookie")
    return resp


@jwtbp.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    response = jsonify(msg="Token refreshed")
    set_access_cookies(response, access_token)
    return response
