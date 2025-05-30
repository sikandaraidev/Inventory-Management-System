from flask import abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from package.backend.databases.Inventory.models_inv.category_model import Category
from package.backend.databases.Inventory.models_inv.product_model import Product
from package.backend.databases.Inventory.models_inv.supplier_model import Supplier
from package.backend.databases.Inventory.schema_inv.product_schema import ProductCreate
from package.backend.databases.product_log.service_prod_log import prod_meta_service

# def create_product(db: Session, product_data: ProductCreate):
#     product = Product(**product_data.dict())
#     db.add(product)
#     db.commit()
#     db.refresh(product)
#     return product


def create_product(db: Session, product_data: ProductCreate):
    try:
        # Validate foreign keys
        category = db.get(Category, product_data.category_id)
        if not category:
            abort(400, description="No category_id")

        supplier = db.get(Supplier, product_data.supplier_id)
        if not supplier:
            abort(400, description="No supplier_id")

        # Create product using Pydantic v2 .model_dump()
        product = Product(**product_data.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        prod_meta_service.create_product_metadata(product)
        return product

    except SQLAlchemyError as e:
        db.rollback()
        abort(500, description=f"Database error: {str(e)}")


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()
