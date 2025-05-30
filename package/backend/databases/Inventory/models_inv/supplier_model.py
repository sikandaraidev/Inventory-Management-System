from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from package.databases.Inventory.models_inv.product_model import Product
from package.backend.db_conn.aws_mysql import Base

if TYPE_CHECKING:
    from package.backend.databases.Inventory.models_inv.product_model import Product


class Supplier(Base):
    __tablename__ = "supplier"

    supplier_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    contact_name: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # One-to-many: a supplier can have multiple products
    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="supplier"
    )

    def __repr__(self) -> str:
        return f"<Supplier(id={self.supplier_id}, name={self.name!r})>"
