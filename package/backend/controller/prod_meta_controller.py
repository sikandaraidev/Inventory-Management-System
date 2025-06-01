from flask import abort, jsonify, request

from package.backend.auth_jwt.decorator_jwt import role_required
from package.backend.databases.product_log.models_prod_log.prod_meta_model import (
    ProductMetadataModel,
)
from package.backend.databases.product_log.schema_prod_log.prod_meta_schema import (
    ProductMetadataSchema,
)
from package.backend.databases.product_log.service_prod_log import prod_meta_service


@role_required(["admin"])
def create_product_meta_controller():
    try:
        data = ProductMetadataSchema.model_validate(request.json)
        result = prod_meta_service.create_product_metadata(data)
        return jsonify(result.to_mongo()), 201
    except Exception as e:
        abort(400, description=str(e))


@role_required(["admin", "staff"])
def get_metadata_controller(product_id):
    meta = prod_meta_service.get_product_metadata(product_id)
    if not meta:
        return jsonify({"error": "Not found"}), 404
    return jsonify(meta.to_mongo()), 200


# @role_required(["admin"])
# def update_metadata_controller(product_id):
#     updates = request.json
#     meta = prod_meta_service.update_product_metadata(product_id, updates)
#     if not meta:
#         return jsonify({"error": "Not found"}), 404
#     return jsonify(meta.to_mongo()), 200


@role_required(["admin"])
def update__metadata_controller(product_id: int, updates: dict):
    return ProductMetadataModel.objects(product_id=product_id).modify(
        new=True, upsert=False, **{f"set__{k}": v for k, v in updates.items()}
    )


@role_required(["admin"])
def delete_metadata_controller(product_id):
    result = prod_meta_service.delete_product_metadata(product_id)
    return jsonify({"deleted_count": result}), 200
