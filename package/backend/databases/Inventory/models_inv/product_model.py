from __future__ import annotations

from datetime import datetime, timezone

# from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from package.backend.databases.Inventory.models_inv.category_model import Category
from package.backend.databases.Inventory.models_inv.supplier_model import Supplier
from package.backend.db_conn.aws_mysql import Base

#     from package.databases.Inventory.models_inv.inventory_alert_model import (
#         InventoryAlert,
#     )
#     from package.databases.Inventory.models_inv.purchase_stock_model import (
#         PurchaseStock,
#     )
#     from package.databases.Inventory.models_inv.sales_stock_model import SalesStock


class Product(Base):
    __tablename__ = "product"

    product_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id"))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier.supplier_id"))
    cost_price: Mapped[float] = mapped_column(Float, nullable=False)
    selling_price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity_in_stock: Mapped[int] = mapped_column(Integer, default=0)
    expiry_date: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="products")

    def __repr__(self) -> str:
        return f"<Product(id={self.product_id}, name={self.name!r}, sku={self.sku!r})>"
