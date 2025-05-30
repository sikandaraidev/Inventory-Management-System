import logging

from flask import request


def setup_logging_middleware(app):
    logging.basicConfig(level=logging.INFO)

    @app.before_request
    def log_request_info():
        app.logger.info(
            f"Request: {request.method} {request.path} by IP: {request.remote_addr}"
        )

    @app.after_request
    def log_response_info(response):
        app.logger.info(
            f"Response: {response.status} {request.path} IP: {request.remote_addr}"
        )
        return response
