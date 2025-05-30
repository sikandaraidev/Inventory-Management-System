from package.backend.databases.product_log.models_prod_log.prod_meta_model import (
    ProductMetadataModel,
)
from package.backend.databases.product_log.schema_prod_log.prod_meta_schema import (
    ProductMetadataSchema,
)


def create_product_metadata(product_obj):
    meta_data = ProductMetadataSchema.from_sql_product(product_obj)
    meta = ProductMetadataModel(**meta_data.model_dump())
    meta.save()
    print("Saved successfully:", meta.to_json())  # Optional for confirmation
    return meta


def get_product_metadata(product_id: int):
    return ProductMetadataModel.objects(product_id=product_id).first()


def update_product_metadata(product_id: int, updates: dict):
    return ProductMetadataModel.objects(product_id=product_id).modify(
        new=True, upsert=False, **{"set__" + k: v for k, v in updates.items()}
    )


def delete_product_metadata(product_id: int):
    return ProductMetadataModel.objects(product_id=product_id).delete()
