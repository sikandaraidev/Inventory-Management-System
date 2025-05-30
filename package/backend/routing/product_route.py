from flask import Blueprint

from package.backend.controller import product_controller

product_bp = Blueprint("product", __name__, url_prefix="/api/products")


product_bp.post("")(product_controller.create_product_controller)
product_bp.get("")(product_controller.get_products_controller)
