import os
from datetime import datetime, timedelta

from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import get_jwt_identity, jwt_required

from package.backend.auth_jwt.extensions import bcrypt, jwt, limiter
from package.backend.configuration.config import config_by_name

# Explicitly import models so they are registered with Base
from package.backend.databases.Inventory.models_inv.user_model import User
from package.backend.db_conn.aws_mysql import Base, Session, engine, get_session
from package.backend.db_conn.mongodb import init_mongo
from package.backend.middlewares.error_handler import register_error_handlers
from package.backend.middlewares.logging_middleware import setup_logging_middleware
from package.backend.routing.jwt_route import jwtbp
from package.backend.routing.prod_meta_route import product_meta_bp
from package.backend.routing.product_route import product_bp
from package.frontend import frontend_bp
from package.home.home import home_bp
from package.inventory import inventory_bp
from package.utils.filters import time_ago


# Creating the Flask app
def create_app(config_name="dev"):
    # initializing flask app
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    app.jinja_env.filters["time_ago"] = time_ago

    CORS(app, supports_credentials=True, origins=["http://localhost:8080"])

    # CONFIGURATION FOR JWT
    app.config["JWT_SECRET_KEY"] = os.environ.get(
        "JWT_SECRET_KEY", "super-secret"
    )  # override in production
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/token/refresh"
    app.config["JWT_COOKIE_SECURE"] = False  # TRUE for only over HTTPS in production
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # enable in production
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"

    bcrypt.__init__(app)
    jwt.__init__(app)
    limiter.__init__(app)

    # MongoDB initialization
    init_mongo()

    # Setup DB + migrations
    try:
        with app.app_context():
            Base.metadata.create_all(bind=engine)
            print("Tables Created Successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

    # Registering blueprints for routes
    app.register_blueprint(home_bp)
    app.register_blueprint(frontend_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(product_meta_bp)
    app.register_blueprint(jwtbp)

    # Middlewares
    # Logging
    setup_logging_middleware(app)

    # Error handling
    register_error_handlers(app)

    # @app.context_processor
    # @jwt_required(optional=True)
    # def inject_user():
    #     identity = get_jwt_identity()
    #     user = None
    #     user_role = None

    #     if identity:
    #         db = next(get_session())  # get SQLAlchemy session
    #         user = db.query(User).filter_by(user_id=identity).first()
    #         if user:
    #             user_role = user.role

    #     return dict(user=user, user_role=user_role)

    @app.template_filter("datetimeformat")
    def datetimeformat(value, format="%Y-%m-%d"):
        if isinstance(value, datetime):
            return value.strftime(format)
        return value  # fallback if value is already string

    # SQLAlchemy session handling per request
    @app.before_request
    def create_session():
        request.db_session = Session()

    @app.teardown_request
    def remove_session(exception=None):
        db_session = getattr(request, "db_session", None)
        if db_session:
            if exception:
                db_session.rollback()
            else:
                db_session.commit()
            db_session.close()
            Session.remove()

    return app
