from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

# from sqlalchemy.orm import relationship
# from package.databases.Inventory.models_inv.product_model import Product
# from package.databases.Inventory.models_inv.supplier_model import Supplier
from package.backend.db_conn.aws_mysql import Base


class PurchaseStock(Base):
    __tablename__ = "purchase_stock"

    purchase_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier.supplier_id"))
    purchase_date: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[int] = mapped_column(Integer)
    cost_price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # product: Mapped["Product"] = relationship(
    #     "Product", back_populates="purchase_stocks"
    # )
    # supplier: Mapped["Supplier"] = relationship(
    #     "Supplier", back_populates="purchase_stocks"
    # )

    def __repr__(self) -> str:
        return f"<PurchaseStock(id={self.purchase_id}, product_id={self.product_id}, quantity={self.quantity})>"
