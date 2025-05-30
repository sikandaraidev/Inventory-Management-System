from flask import jsonify, request
from flask_jwt_extended import jwt_required

from package.backend.auth_jwt.decorator_jwt import role_required
from package.backend.databases.Inventory.schema_inv.product_schema import ProductCreate
from package.backend.databases.Inventory.service_inv import product_service
from package.backend.db_conn.aws_mysql import get_session


@jwt_required()
@role_required(["admin"])
def create_product_controller():
    db = next(get_session())
    data = request.get_json()
    product_schema = ProductCreate(**data)
    product = product_service.create_product(db, product_schema)
    return jsonify({"success": True, "data": product.product_id}), 201


@jwt_required()
@role_required(["admin", "staff"])
def get_products_controller():
    db = next(get_session())
    products = product_service.get_all_products(db)
    return jsonify(
        [
            {
                "id": p.product_id,
                "name": p.name,
                "price": p.selling_price,
                "category_id": p.category_id,
            }
            for p in products
        ]
    )
