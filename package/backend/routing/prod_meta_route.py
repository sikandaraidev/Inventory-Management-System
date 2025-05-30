from flask import Blueprint

from package.backend.controller import prod_meta_controller

product_meta_bp = Blueprint("product_meta", __name__, url_prefix="/api/metadata")

product_meta_bp.post("/")(prod_meta_controller.create_product_meta_controller)
product_meta_bp.get("/<int:product_id>")(prod_meta_controller.get_metadata_controller)
product_meta_bp.put("/<int:product_id>")(
    prod_meta_controller.update_metadata_controller
)
product_meta_bp.delete("/<int:product_id>")(
    prod_meta_controller.delete_metadata_controller
)
